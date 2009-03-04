from compsoc.comms.models import Communication
from django.contrib import admin

class CommunicationAdmin(admin.ModelAdmin):
    fields = ('type', 'title', 'date', 'text')
    list_display = ('title', 'type')
    list_filter = ('type',)

admin.site.register(Communication, CommunicationAdmin)

