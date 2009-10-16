from tournaments.models import *
from django.shortcuts import *
from django.template import RequestContext
from compsoc.shortcuts import begin_week,path_processor

def tournament_list(request):
    tournaments = get_list_or_404(Tournament)
    return render_to_response('tournaments/list.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'list':tournaments,
    },context_instance=RequestContext(request,{},[path_processor]))
    
def tournament_detail(request,id):
    tournament = get_object_or_404(Tournament,pk=id)
    return render_to_response('tournaments/detail.html', {
        'breadcrumbs': [('/','home'),('/tournament/','tournament list')],
        'tournament':tournament,
    },context_instance=RequestContext(request,{},[path_processor]))
