from Compsoc.cms.models import Page,PageRevision
from django.contrib import admin


class RevisionInline(admin.StackedInline):
    model = PageRevision
    extra = 1

class PageAdmin(admin.ModelAdmin):
    inlines = [RevisionInline]

admin.site.register(Page,PageAdmin)

