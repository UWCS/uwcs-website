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
        if data.get('signupsLimit') < 0:
            raise forms.ValidationError('The signup limit must be positive')

        seating = data.get('seating')
        if seating:
            e = Event.objects.get(eventsignup__pk=data.get('id'))
            (rows,cols) = Seating.objects.maximums(e)
            if rows > seating.max_rows - 1  or cols > seating.max_cols - 1:
                raise forms.ValidationError(u'This seating room is used by is required to be wider or taller than it currently is.')
        
        return data

class EventSignupInline(admin.StackedInline):
    model = EventSignup
    max_num = 1
    form = EventSignupForm

#class SignupInline(admin.TabularInline):
#   model = Signup
#    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [ EventSignupInline ] #, SignupInline]
    form = EventAdminForm
    list_display = ('type', 'location', 'start')
    ordering = ('-start',)

class SeatingRoomForm(forms.ModelForm):
    class Meta:
        model = EventSignup

    def clean(self):
        data = self.cleaned_data
        max_cols,max_rows = data.get('max_cols')-1,data.get('max_rows')-1
        for e in Event.objects.filter(eventsignup__seating__pk=data.get('id')):
            (rows,cols) = Seating.objects.maximums(e)
            if rows > max_rows or cols > max_cols:
                raise forms.ValidationError(u'This seating room is used by %s, which requires it to be wider or taller than you have set it.'%e)
        return data

class SeatingRoomInline(admin.StackedInline):
    model = SeatingRoom
    form = SeatingRoomForm

class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = [SeatingRoomInline]

class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['target']

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event,EventAdmin)
#admin.site.register(Signup)
#admin.site.register(Seating)
#admin.site.register(SeatingRoom)
#admin.site.register(SeatingRevision)

