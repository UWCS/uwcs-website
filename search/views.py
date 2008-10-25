from django.shortcuts import render_to_response

def search(request):
    return render_to_response('search.html')
