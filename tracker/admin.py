from compsoc.tracker.models import *
from django.contrib import admin
from django.forms import ModelForm
from compsoc.memberinfo.forms import UserModelChoiceField
from memberinfo.models import Member
from django import forms

class GoalAdminForm(ModelForm):
    supervisor = forms.ModelChoiceField(queryset=Member.objects.order_by('user__first_name','user__last_name').select_related())
    #supervisor = forms.ModelChoiceField(queryset=User.objects.order_by('first_name','last_name').select_related('member'))
    #supervisor = forms.ModelChoiceField(queryset=User.objects.all().select_related('member')[:10],required=True)
    def clean(self, *args, **kwargs):
        super(GoalAdminForm, self).clean(*args, **kwargs)
        self.cleaned_data['supervisor'] = User.objects.get(member=self.cleaned_data['supervisor'])
        return self.cleaned_data
    class Meta:
        model = Goal

class GoalAdmin(admin.ModelAdmin):
    list_display = ('name','completed',)
    ordering = ('completed','name')
    form = GoalAdminForm

admin.site.register(Goal,GoalAdmin)

class TicketAdminForm(ModelForm):
    #submitter = UserModelChoiceField(queryset=User.objects.all(),required=True)
    #assignee = UserModelChoiceField(queryset=User.objects.all(),required=False)
    class Meta:
        model = Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','started','submitter','goal','completed')
    form = TicketAdminForm

admin.site.register(Ticket,TicketAdmin)
