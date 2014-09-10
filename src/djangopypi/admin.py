from django.conf import settings
from django.contrib import admin

from djangopypi.models import *


class PackageAdmin(admin.ModelAdmin):

    list_display = ('name', 'latest', 'release_count')
    search_fields = ('name',)


class ReleaseAdmin(admin.ModelAdmin):

    list_display = ('package', 'version', 'created', 'distribution_count')
    search_fields = ('package__name', 'version')
    list_filter = ('created',)


class DistributionAdmin(admin.ModelAdmin):

    list_display = ('release', 'created', 'filetype', 'md5_digest')
    search_fields = ('release__package__name', 'release__version')
    list_filter = ('created', 'filetype')


admin.site.register(Package, PackageAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Classifier)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Review)

if getattr(settings,'DJANGOPYPI_MIRRORING', False):
    admin.site.register(MasterIndex)
    admin.site.register(MirrorLog)
