from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/', 'haystack.views.basic_search', {'template': 'djangopypi/search_results.html',}, name='haystack_search'),
    url(r'', include("djangopypi.urls")),

    # To test the error pages uncomment these lines:
    #(r'^404/$', 'django.views.defaults.page_not_found'),
    #(r'^500/$', 'django.views.defaults.server_error'),
)
