from django.conf import settings
from django.db.models.query import Q
from django.http import Http404, HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package, Release, normalize_name
from djangopypi.forms import SimplePackageSearchForm, PackageForm


class IndexView(ListView):

    def get_queryset(self):
        return Package.objects.all()

index = IndexView.as_view()


class SimpleIndexView(IndexView):

    template_name = 'djangopypi/package_list_simple.html'

simple_index = SimpleIndexView.as_view()


def details(request, package, simple=False, template='djangopypi/package_detail.html', content_type='text/html', **kwargs):
    try:
        p = get_object_or_404(Package, normalized_name=normalize_name(package))
        return render(request, template, {'package': p}, content_type=content_type)
    except Http404, e:
        try:
            with open("/var/log/proxy.log", "a+") as fd:
                fd.write('proxying %s\n' % package)
        except (OSError, IOError) as e:
            pass
        if settings.DJANGOPYPI_PROXY_MISSING:
            proxy_folder = 'simple' if simple else 'pypi'
            return HttpResponseRedirect('%s/%s/%s/' %
                                        (settings.DJANGOPYPI_PROXY_BASE_URL.rstrip('/'),
                                         proxy_folder,
                                         package))
        raise Http404(u'%s is not a registered package' % (package,))

def simple_details(request, package, **kwargs):
    return details(request, package, simple=True, template='djangopypi/package_detail_simple.html', **kwargs)

def doap(request, package, **kwargs):
    return details(request, package, template='djangopypi/package_doap.xml', content_type='djangopypi/package_doap.xml', **kwargs)

def search(request, **kwargs):
    if request.method == 'POST':
        form = SimplePackageSearchForm(request.POST)
    else:
        form = SimplePackageSearchForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data['query']
        kwargs['queryset'] = Package.objects.filter(Q(name__contains=q) |
                                                    Q(releases__package_info__contains=q)).distinct()
    return index(request, **kwargs)


class Manage(UpdateView):

    form_class = PackageForm
    template_name = 'djangopypi/package_manage.html'

    def get_object(self, queryset=None):
        return Package.objects.get(pk=self.kwargs['package'])

@user_owns_package()
def manage(request, package, **kwargs):
    return Manage.as_view()(request, package=package)

@user_maintains_package()
def manage_versions(request, package, **kwargs):
    package = get_object_or_404(Package, name=package)
    kwargs.setdefault('formset_factory_kwargs', {})
    kwargs['formset_factory_kwargs'].setdefault('fields', ('hidden',))
    kwargs['formset_factory_kwargs']['extra'] = 0

    kwargs.setdefault('formset_factory', inlineformset_factory(Package, Release, **kwargs['formset_factory_kwargs']))
    kwargs.setdefault('template_name', 'djangopypi/package_manage_versions.html')
    kwargs.setdefault('template_object_name', 'package')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    kwargs['extra_context'][kwargs['template_object_name']] = package
    kwargs.setdefault('formset_kwargs',{})
    kwargs['formset_kwargs']['instance'] = package

    if request.method == 'POST':
        formset = kwargs['formset_factory'](data=request.POST, **kwargs['formset_kwargs'])
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(package.get_absolute_url())

    formset = kwargs['formset_factory'](**kwargs['formset_kwargs'])

    kwargs['extra_context']['formset'] = formset

    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])
