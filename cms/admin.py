from compsoc.cms.models import Page,PageRevision,Game
from django.contrib import admin


class RevisionInline(admin.StackedInline):
    model = PageRevision
    extra = 1

class PageAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    inlines = [RevisionInline]

admin.site.register(Page,PageAdmin)
admin.site.register(Game)
