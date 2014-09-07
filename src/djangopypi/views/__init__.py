from logging import getLogger

from django.conf import settings
from django.http import HttpResponseNotAllowed

from djangopypi.decorators import csrf_exempt
from djangopypi.http import parse_distutils_request
from djangopypi.models import Package, Release
from djangopypi.views.xmlrpc import parse_xmlrpc_request



log = getLogger('djangopypi.views')

@csrf_exempt
def root(request, fallback_view=None, **kwargs):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    if request.method == 'POST':
        if request.META['CONTENT_TYPE'] == 'text/xml':
            log.debug('XMLRPC request received')
            return parse_xmlrpc_request(request)
        log.debug('Distutils request received')
        parse_distutils_request(request)
        action = request.POST.get(':action','')
    else:
        action = request.GET.get(':action','')
    
    if not action:
        log.debug('No action in root view')
        if fallback_view is None:
            fallback_view = settings.DJANGOPYPI_FALLBACK_VIEW
        return fallback_view(request, **kwargs)
    
    if not action in settings.DJANGOPYPI_ACTION_VIEWS:
        log.error('Invalid action encountered: %s' % (action,))
        return HttpResponseNotAllowed(settings.DJANGOPYPI_ACTION_VIEW.keys())

    log.debug('Applying configured action view for %s' % (action,))
    return settings.DJANGOPYPI_ACTION_VIEWS[action](request, **kwargs)

