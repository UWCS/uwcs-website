from compsoc.comms.models import Communication
from django.contrib import admin

class CommunicationAdmin(admin.ModelAdmin):
    fields = ('type', 'date', 'text')
    list_display = ('type', 'title')

admin.site.register(Communication, CommunicationAdmin)

