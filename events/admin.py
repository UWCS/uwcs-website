from compsoc.events.models import *
from django.contrib import admin
from django import forms

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

class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup

    def clean(self):
        data = self.cleaned_data
        close = data.get('close')
        if close < data.get('open'):
            raise forms.ValidationError('Signups must close after they start')
        if close < data.get('fresher_open'):
            raise forms.ValidationError('Fresher Signups must close after they start')
        if close < data.get('guest_open'):
            raise forms.ValidationError('Guest Signups must close after they start')
        
        return data

class EventSignupInline(admin.StackedInline):
    model = EventSignup
    max_num = 1
    form = EventSignupForm

class EventAdmin(admin.ModelAdmin):
    inlines = [ EventSignupInline, ]
    form = EventAdminForm

admin.site.register(EventType)
admin.site.register(Event,EventAdmin)
admin.site.register(Signup)
admin.site.register(Seating)
admin.site.register(SeatingRoom)
admin.site.register(SeatingRevision)

