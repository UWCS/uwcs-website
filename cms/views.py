from django.shortcuts import render_to_response
from Compsoc.cms.models import *

def handle(request,url):
    page = Page.objects.get(slug=url)
    data = page.pagerevision_set.latest('date_written')

    dict = {
        'title':data.title,
        'text':data.text,
    }
    return render_to_response('cms/page.html',dict)
