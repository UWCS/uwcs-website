from compsoc.comms.models import Communication
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from tinymce.widgets import TinyMCE

class CommunicationAdminForm(ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols':80,'rows':30}))

    class Meta:
        model = Communication

class CommunicationAdmin(admin.ModelAdmin):
    form = CommunicationAdminForm
    fields = ('type', 'title', 'date', 'text')
    list_display = ('title', 'type', 'date')
    list_filter = ('type',)
    search_fields = ('title',)
    ordering = ('-date',)

admin.site.register(Communication, CommunicationAdmin)
