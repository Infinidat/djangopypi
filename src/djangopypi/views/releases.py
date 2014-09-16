from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package, Release, Distribution
from djangopypi.forms import ReleaseForm, DistributionUploadForm



class IndexView(ListView):

    def get_queryset(self):
        return Release.objects.filter(hidden=False)

index = IndexView.as_view()


def details(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)

    if not release:
        raise Http404('Version %s does not exist for %s' % (version,
                                                            package,))

    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('template_name','djangopypi/release_detail.html')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)

    kwargs['extra_context'][kwargs['template_object_name']] = release

    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

def doap(request, package, version, **kwargs):
    kwargs.setdefault('template_name','djangopypi/release_doap.xml')
    kwargs.setdefault('mimetype', 'text/xml')
    return details(request, package, version, **kwargs)


class Manage(UpdateView):

    form_class = ReleaseForm
    template_name = 'djangopypi/release_manage.html'

    def get_object(self, queryset=None):
        return Release.objects.get(pk=self.kwargs['object_id'])

@user_maintains_package()
def manage(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)
    if not release:
        raise Http404('Version %s does not exist for %s' % (version, package))
    return Manage.as_view()(request, object_id=release.pk)

@user_maintains_package()
def manage_metadata(request, package, version, **kwargs):
    kwargs.setdefault('template_name', 'djangopypi/release_manage.html')
    kwargs.setdefault('template_object_name', 'release')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)

    release = get_object_or_404(Package, name=package).get_release(version)

    if not release:
        raise Http404('Version %s does not exist for %s' % (version,
                                                            package,))

    if not release.metadata_version in settings.DJANGOPYPI_METADATA_FORMS:
        #TODO: Need to change this to a more meaningful error
        raise Http404()

    kwargs['extra_context'][kwargs['template_object_name']] = release

    form_class = settings.DJANGOPYPI_METADATA_FORMS.get(release.metadata_version)

    initial = {}
    multivalue = ('classifier',)

    for key, values in release.package_info.iterlists():
        if key in multivalue:
            initial[key] = values
        else:
            initial[key] = '\n'.join(values)

    if request.method == 'POST':
        form = form_class(data=request.POST, initial=initial)

        if form.is_valid():
            for key, value in form.cleaned_data.iteritems():
                if isinstance(value, basestring):
                    release.package_info[key] = value
                elif hasattr(value, '__iter__'):
                    release.package_info.setlist(key, list(value))

            release.save()
            return HttpResponseRedirect(release.get_absolute_url())
    else:
        form = form_class(initial=initial)

    kwargs['extra_context']['form'] = form

    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

@user_maintains_package()
def manage_files(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)

    if not release:
        raise Http404('Version %s does not exist for %s' % (version,
                                                            package,))

    kwargs.setdefault('formset_factory_kwargs',{})
    kwargs['formset_factory_kwargs'].setdefault('fields', ('comment',))
    kwargs['formset_factory_kwargs']['extra'] = 0

    kwargs.setdefault('formset_factory', inlineformset_factory(Release, Distribution, **kwargs['formset_factory_kwargs']))
    kwargs.setdefault('template_name', 'djangopypi/release_manage_files.html')
    kwargs.setdefault('template_object_name', 'release')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    kwargs['extra_context'][kwargs['template_object_name']] = release
    kwargs.setdefault('formset_kwargs',{})
    kwargs['formset_kwargs']['instance'] = release
    kwargs.setdefault('upload_form_factory', DistributionUploadForm)

    if request.method == 'POST':
        formset = kwargs['formset_factory'](data=request.POST,
                                            files=request.FILES,
                                            **kwargs['formset_kwargs'])
        if formset.is_valid():
            formset.save()
            formset = kwargs['formset_factory'](**kwargs['formset_kwargs'])
    else:
        formset = kwargs['formset_factory'](**kwargs['formset_kwargs'])

    kwargs['extra_context']['formset'] = formset
    kwargs['extra_context'].setdefault('upload_form',
                                       kwargs['upload_form_factory']())

    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

@user_maintains_package()
def upload_file(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)

    if not release:
        raise Http404('Version %s does not exist for %s' % (version,
                                                            package,))

    kwargs.setdefault('form_factory', DistributionUploadForm)
    kwargs.setdefault('post_save_redirect', reverse('djangopypi-release-manage-files',
                                                    kwargs={'package': package,
                                                            'version': version}))
    kwargs.setdefault('template_name', 'djangopypi/release_upload_file.html')
    kwargs.setdefault('template_object_name', 'release')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    kwargs['extra_context'][kwargs['template_object_name']] = release

    if request.method == 'POST':
        form = kwargs['form_factory'](data=request.POST, files=request.FILES)
        if form.is_valid():
            dist = form.save(commit=False)
            dist.release = release
            dist.uploader = request.user
            dist.save()

            return RedirectView.as_view(kwargs.get('post_save_redirect'), release)
    else:
        form = kwargs['form_factory']()

    kwargs['extra_context']['form'] = form

    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])
