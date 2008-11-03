from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from compsoc.search import search_for_string

def search(request):
    if request.method == "POST":
        try:
            search_string = request.POST['searchBox']
        except AttributeError:
            pass
        else:
            search_results = search_for_string(search_string)
            return render_to_response('search.html',
                                      {'results':search_results,'user':request.user})
    return HttpResponseRedirect('/')
