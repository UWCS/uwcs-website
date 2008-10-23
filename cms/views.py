from django.shortcuts import render_to_response
from Compsoc.cms.models import *
    
def cleanse(l):
    return map(lambda p: (p.slug,p.get_data().title),l)

def handle(request,url):
    page = Page.objects.get(slug=url)
    data = page.get_data()
    
    dict = {
        'title':data.title,
        'text':data.text,
        'peers':cleanse(page.get_peers()),
        'children':cleanse(page.get_children()),
    }
    return render_to_response('cms/page.html',dict)
