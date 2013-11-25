from django.contrib import admin

from uwcs_website.cms.models import Attachment,Page,PageRevision,Game

class RevisionInline(admin.StackedInline):
    model = PageRevision
    extra = 1

class PageAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    ordering = ('slug',)
    inlines = [RevisionInline]

admin.site.register(Page,PageAdmin)
admin.site.register(Attachment)
admin.site.register(Game)
