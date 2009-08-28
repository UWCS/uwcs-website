from compsoc.games.models import *
from django.contrib import admin
from django import forms

'''
class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event

    def clean(self):
        data = self.cleaned_data
        start = data.get('start')
        finish = data.get('finish')
        display_from = data.get('displayFrom')
        if finish < start:
            raise forms.ValidationError('Event must finish after its started')
        if start < display_from:
            raise forms.ValidationError('Event must be displayed before it starts')

        return data
'''

class GamesAdmin(admin.ModelAdmin):
#    form = EventAdminForm
    list_display = ('name', 'version', 'description')
    ordering = ('name',)

admin.site.register(Game,GamesAdmin)

