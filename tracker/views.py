from compsoc.tracker.models import *
from datetime import datetime
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

COMPLETED_CHOICES = (
    ('C','Completed'),
    ('O','Open'),
    ('A','All'),
)

class TicketSearchForm(forms.Form):
    '''
    Search limited by conjunction of restrictions present
    in this form.
    '''
    name = forms.CharField(max_length=20,required=False)
    description = forms.CharField(required=False)
    submitter = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    assignee = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    goal = forms.ModelChoiceField(queryset=Goal.objects.all(),required=False)
    completed = forms.ChoiceField(choices=COMPLETED_CHOICES)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name','description','goal')

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
            return HttpResponseRedirect('/tickets/')
    else:
        form = TicketForm()

    return render_to_response('tracker/new_ticket.html', {
        'user': request.user,
        'form': form,
    })
 

def index(request):
    '''
    Offers a search form, and/or results for said search
    '''
    if request.method == 'POST':
        form = TicketSearchForm(request.POST)

        if form.is_valid():
            sub = form.cleaned_data['submitter']
            assign = form.cleaned_data['assignee']
            results = Ticket.objects.by_completed(
                form.cleaned_data['completed']
            ).filter(
                name__contains=form.cleaned_data['name'],
                description__contains=form.cleaned_data['description']
            )
            if sub: results = results.filter(submitter=sub)
            if assign: results = results.filter(assignee=assign)

    else:
        form = TicketSearchForm()
        results = Ticket.objects.by_completed('A')

    my_id = request.user.id
    shorts = [
        ('Tickets for me',[('assignee',my_id),('completed','O')]),
        ('Tickets from me',[('submitter',my_id),('completed','O')]),
    ]

    return render_to_response('tracker/search.html', {
        'form': form,
        'shorts':shorts,
        'results':results.order_by('goal').order_by('completed'),
        'user': request.user,
    })

