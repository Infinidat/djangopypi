import os,re
from logging import getLogger

from django.conf import settings
from django.db import transaction
from django.http import *
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import login

from djangopypi.decorators import basic_auth
from djangopypi.forms import PackageForm, ReleaseForm
from djangopypi.models import Package, Release, Distribution, Classifier, normalize_name

from django.utils.text import force_text, allow_lazy, six
from django.core.files.storage import FileSystemStorage

log = getLogger('djangopypi.views.distutils')

ALREADY_EXISTS_FMT = _(
    "A file named '%s' already exists for %s. Please create a new release.")

@basic_auth
def register_or_upload(request):
    if request.method != 'POST':
        transaction.rollback()
        msg = 'Only post requests are supported'
        return HttpResponseBadRequest(msg, reason=msg)

    name = request.POST.get('name',None).strip()

    if not name:
        transaction.rollback()
        msg = 'No package name specified'
        return HttpResponseBadRequest(msg, reason=msg)

    try:
        package = Package.objects.get(normalized_name=normalize_name(name))
    except Package.DoesNotExist:
        package = Package.objects.create(name=name)
        package.owners.add(request.user)

    if (request.user not in package.owners.all() and
        request.user not in package.maintainers.all()):

        transaction.rollback()
        msg = 'You are not an owner/maintainer of %s' % (package.name,)
        return HttpResponseForbidden(msg, reason=msg)

    version = request.POST.get('version',None).strip()
    metadata_version = request.POST.get('metadata_version', None).strip()

    if not version or not metadata_version:
        transaction.rollback()
        msg = 'Release version and metadata version must be specified'
        return HttpResponseBadRequest(msg, reason=msg)

    if not metadata_version in settings.DJANGOPYPI_METADATA_FIELDS:
        transaction.rollback()
        msg = 'Metadata version must be one of: %s' % (', '.join(settings.DJANGOPYPI_METADATA_FIELDS.keys()),)
        return HttpResponseBadRequest(msg, reason=msg)

    release, created = Release.objects.get_or_create(package=package,
                                                     version=version)

    if (('classifiers' in request.POST or 'download_url' in request.POST) and
        metadata_version == '1.0'):
        metadata_version = '1.1'

    release.metadata_version = metadata_version

    fields = settings.DJANGOPYPI_METADATA_FIELDS[metadata_version]

    if 'classifiers' in request.POST:
        request.POST.setlist('classifier',request.POST.getlist('classifiers'))

    release.package_info = MultiValueDict(dict(filter(lambda t: t[0] in fields,
                                                      request.POST.iterlists())))

    for key, value in release.package_info.iterlists():
        release.package_info.setlist(key,
                                     filter(lambda v: v != 'UNKNOWN', value))

    release.save()
    if not 'content' in request.FILES:
        transaction.commit()
        return HttpResponse('release registered')

    uploaded = request.FILES.get('content')

    for dist in release.distributions.all():
        if os.path.basename(dist.content.name) == uploaded.name:
            """ Need to add handling optionally deleting old and putting up new """
            transaction.rollback()
            msg = 'That file has already been uploaded...'
            return HttpResponseBadRequest(msg, reason=msg)

    md5_digest = request.POST.get('md5_digest','')

    try:
        new_file = Distribution.objects.create(release=release,
                                               content=uploaded,
                                               filetype=request.POST.get('filetype','sdist'),
                                               pyversion=request.POST.get('pyversion',''),
                                               uploader=request.user,
                                               comment=request.POST.get('comment',''),
                                               signature=request.POST.get('gpg_signature',''),
                                               md5_digest=md5_digest)
    except Exception, e:
        transaction.rollback()
        log.exception('Failure when storing upload')
        msg = 'Failure when storing upload'
        return HttpResponseServerError(msg, reason=msg)

    transaction.commit()

    return HttpResponse('upload accepted')

def list_classifiers(request, mimetype='text/plain'):
    response = HttpResponse(mimetype=mimetype)
    response.write(u'\n'.join(map(lambda c: c.name,Classifier.objects.all())))
    return response

def get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = force_text(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.\+]', '', s)

get_valid_filename = allow_lazy(get_valid_filename, six.text_type)

class FileSystemStorage_PEP440(FileSystemStorage):
    def get_valid_name(self, name):
        """
        Returns a filename, based on the provided filename, that's suitable for
        use in the target storage system.
        """
        return get_valid_filename(name)
