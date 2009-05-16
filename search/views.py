from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from compsoc.shortcuts import path_processor
from compsoc.search import search_for_string

def search(request):
    if request.method == "POST":
        try:
            search_string = request.POST['searchBox']
        except AttributeError:
            pass
        else:
            search_results = search_for_string(search_string)
            return render_to_response('search.html',{
                'results':search_results,
                'forwhat':search_string,
            },context_instance=RequestContext(request,{},[path_processor]))

    return HttpResponseRedirect('/')
