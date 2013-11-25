from models import *
from string import Template
from django.contrib import admin
from django import forms
from django.forms import widgets
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class SocietyLogEntryInline(admin.StackedInline):
    model = SocietyLogEntry
    extra = 1

class SocietyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'number')
    inlines = [SocietyLogEntryInline]

    def render_change_form(self, request, context, *args, **kwargs):
        extra = {
            #'society_contacts': SocietyContact.objects.filter(id=context['object_id']).select_related('user'),
#            'society_contacts': SocietyContact.objects.filter(id=context['object_id']),
        }

        context.update(extra)
        superclass = super(SocietyAdmin, self)
        return superclass.render_change_form(request, context, *args, **kwargs)

admin.site.register(Society, SocietyAdmin)
admin.site.register(SocietyContact)
