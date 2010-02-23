from compsoc.tracker.models import *
from datetime import datetime
from collections import defaultdict

from django.contrib.auth.models import User, Group
from django import forms
from django.shortcuts import render_to_response
from compsoc.shortcuts import path_processor
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import AdminSplitDateTime
from compsoc.memberinfo.forms import UserModelChoiceField

from django.shortcuts import get_object_or_404
from django.contrib.admin.models import LogEntry,ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType

COMPLETED_CHOICES = (
    ('C','Completed'),
    ('O','Open'),
    ('A','All'),
)

COMPARATORS = (
    ('A','After'),
    ('B','Before'),
    ('O','On'),
)

class DateTimeQueryWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        super(DateTimeQueryWidget,self).__init__(*args, **kwargs)

    def decompress(self, value):
        if value == None:
            return [None,None]
        else:
            return [value[0],value[1]]

class DateTimeQueryField(forms.MultiValueField):
    def __init__(self, future=True, *args, **kwargs):
        dt = forms.SplitDateTimeField(initial=datetime.now())
        comp = forms.ChoiceField(
            choices=COMPARATORS,
            initial=('A' if future else 'B'),
        )
        super(DateTimeQueryField,self).__init__(
            fields=(comp,dt),
            widget=DateTimeQueryWidget((
                comp.widget,
                AdminSplitDateTime(),
            )),
            *args,
            **kwargs
        )

    def compress(self,data_list):
            return (data_list[0],data_list[1])

class TicketSearchForm(forms.Form):
    '''
    Search limited by conjunction of restrictions present
    in this form.
    '''
    title = forms.CharField(max_length=20,required=False)
    description = forms.CharField(required=False)
    submitter = UserModelChoiceField(queryset=User.objects.all(),required=False)
    submitter_group = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    assignee = UserModelChoiceField(queryset=User.objects.all(),required=False)
    assignee_group = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    goal = forms.ModelChoiceField(queryset=Goal.objects.all(),required=False)
    submitted = DateTimeQueryField(future=False)
    deadline = DateTimeQueryField()
    completed = forms.ChoiceField(choices=COMPLETED_CHOICES)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title','description','goal')

@login_required
def new_ticket(request):
    '''
    New ticket submission externally
    '''
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.submitter = request.user
            ticket.started = datetime.now()
            ticket.completed = False
            ticket.save()
            #print "logging! %s" % ticket.id
            LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(ticket).pk,
                object_id       = ticket.pk,
                object_repr     = ticket.__unicode__(), 
                action_flag     = ADDITION,
            )
            return HttpResponseRedirect('/tickets/')
    else:
        form = TicketForm()

    return render_to_response('tracker/new_ticket.html', {
        'breadcrumbs': [('/','home'),('/tickets','tickets'),('/tickets/new/','new')],
        'form': form,
    },context_instance=RequestContext(request,{},[path_processor]))

common = [
    ('completed','O'),
    ('submitted_0','A'),
    ('deadline_0','A'),
] 
DF = '%Y-%m-%d'
TF = '%H:%M:%S'

@login_required
def details(request,object_id):
    return render_to_response('tracker/details.html',{
        'object':get_object_or_404(Ticket,pk=object_id),
    },context_instance=RequestContext(request,{},[path_processor]))

@login_required
def index(request):
    '''
    Offers a search form, and/or results for said search
    '''
    if request.method == 'POST':
        form = TicketSearchForm(request.POST)

        if form.is_valid():
            sub = form.cleaned_data['submitter']
            assign = form.cleaned_data['assignee']
            agroup = form.cleaned_data['assignee_group']
            sgroup = form.cleaned_data['submitter_group']

            results = Ticket.objects.by_completed(
                form.cleaned_data['completed']
            ).filter(
                title__contains=form.cleaned_data['title'],
                description__contains=form.cleaned_data['description']
            )
            if sub:
                results = results.filter(submitter=sub)
            if assign:
                results = results.filter(assignee=assign)
            if agroup:
                results.filter(assignee__in=agroup.user_set.all())
            if sgroup:
                results.filter(submitter__in=sgroup.user_set.all())

        else:
            results = Ticket.objects.none()

    else:
        form = TicketSearchForm()
        results = Ticket.objects.by_completed('O')

    my_id = request.user.id
    n = datetime.now()
    shorts = [
        ('Tickets for me',common + [('assignee',my_id)]),
        ('Tickets from me',common + [('submitter',my_id)]),
        ('Overdue',common + [
            ('deadline_1_0',n.strftime(DF)),
            ('deadline_1_1',n.strftime(TF)),
        ]),
        ('Exec Tickets',common + [('assignee_group',1)]),
        ('All Tickets', [
            ('completed','A'),
            ('submitted_0','A'),
            ('deadline_0','A'),
        ]),
    ]

    #group results by goal
    by_goal = defaultdict(lambda: [])
    for ticket in results.order_by('goal').order_by('completed'):
        by_goal[ticket.goal.name].append(ticket)

    return render_to_response('tracker/search.html', {
        'breadcrumbs': [('/','home'),('/tickets','tickets')],
        'form': form,
        'shorts':shorts,
        'results':by_goal.iteritems(),
    },context_instance=RequestContext(request,{},[path_processor]))

