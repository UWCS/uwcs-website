from compsoc.tournaments.models import *
from django.shortcuts import *
from django.template import RequestContext
from compsoc.shortcuts import begin_week,path_processor
from django import forms
from django.contrib.auth.models import User
from memberinfo.forms import UserModelChoiceField
from tournaments.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def tournament_list(request):
    tournaments = get_list_or_404(Tournament)
    return render_to_response('tournaments/list.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'list':tournaments,
    },context_instance=RequestContext(request,{},[path_processor]))

class WinnerForm(forms.Form):
    winner = forms.ModelChoiceField(queryset=Allocation.objects.all())

class PlayerForm(forms.Form):
    player = UserModelChoiceField(queryset=User.objects.all())

def add_player_to_tournament(request,id):
    tournament = get_object_or_404(Tournament,pk=id)
    if request.method == 'POST':
        play_form = PlayerForm(request.POST)
        if play_form.is_valid():
            user = play_form.cleaned_data['player']
            tournament.allocation_set.create(tournament=tournament,user=user,index=tournament.allocation_set.count() + 1)

    return HttpResponseRedirect(reverse('tournaments.views.tournament_detail', args=[id]))

def tournament_detail(request,id):
    tournament = get_object_or_404(Tournament,pk=id)
    if request.method == 'POST':
        win_form = WinnerForm(request.POST)
        if win_form.is_valid():
            win_form.cleaned_data['winner'].win()

    else:
        win_form = WinnerForm()

    return _render_detail(request,tournament,win_form,PlayerForm())

def _render_detail(request,tournament,win_form,play_form):
    win_form.fields['winner'].queryset=tournament.in_play()
    play_form.fields['player'].queryset=User.objects.exclude(allocation__tournament=tournament)

    return render_to_response('tournaments/detail.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'tournament':tournament,
        'win_form':win_form,
        'play_form':play_form,
    },context_instance=RequestContext(request,{},[path_processor]))
