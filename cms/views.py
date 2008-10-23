from django.shortcuts import render_to_response
from Compsoc.cms.models import *

def handle(request,url):
    page = Page.objects.get(slug=url)
    data = page.get_data()
    peers = []
    for p in page.get_peers():
        if p != page:
            peers.append((p.slug,p.get_data().title))

    dict = {
        'title':data.title,
        'text':data.text,
        'peers':peers,
    }
    return render_to_response('cms/page.html',dict)
