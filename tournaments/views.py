from tournaments.models import *
from django.shortcuts import *
from django.template import RequestContext
from compsoc.shortcuts import begin_week,path_processor
from django import forms

def tournament_list(request):
    tournaments = get_list_or_404(Tournament)
    return render_to_response('tournaments/list.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'list':tournaments,
    },context_instance=RequestContext(request,{},[path_processor]))

class WinnerForm(forms.Form):
    # TODO: validation
    winner = forms.ModelChoiceField(queryset=Allocation.objects.all())

def tournament_detail(request,id):
    tournament = get_object_or_404(Tournament,pk=id)
    if request.method == 'POST':
        form = WinnerForm(request.POST)
        if form.is_valid():
            form.cleaned_data['winner'].win()

    else:
        form = WinnerForm()
        form.fields['winner'].queryset=tournament.in_play()

    return render_to_response('tournaments/detail.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'tournament':tournament,
        'form':form,
    },context_instance=RequestContext(request,{},[path_processor]))
