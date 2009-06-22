from compsoc.tracker.models import *
from django.contrib import admin
from django.forms import ModelForm
from compsoc.memberinfo.forms import UserModelChoiceField

class GoalAdminForm(ModelForm):
    supervisor = UserModelChoiceField(queryset=User.objects.select_related('member').all(),required=True)
    class Meta:
        model = Goal

class GoalAdmin(admin.ModelAdmin):
    list_display = ('name','completed',)
    ordering = ('completed','name')
    form = GoalAdminForm

admin.site.register(Goal,GoalAdmin)

class TicketAdminForm(ModelForm):
    submitter = UserModelChoiceField(queryset=User.objects.all(),required=True)
    assignee = UserModelChoiceField(queryset=User.objects.all(),required=False)
    class Meta:
        model = Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','started','submitter','goal','completed')
    form = TicketAdminForm

admin.site.register(Ticket,TicketAdmin)
