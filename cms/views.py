from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from compsoc.cms.models import *
    
def cleanse(l):
    return map(lambda p: (p.slug,p.get_data().title),l)

def lookup(l):
    breadcrumbs = [('../','home')]
    for url in l:
        try:
            abs_url = "/cms/%s" % (url,)
            breadcrumbs.append((abs_url,Page.objects.get(slug=url).get_data().title))
        # There may not be a parent, if so, we want
        except Page.DoesNotExist: pass
    return breadcrumbs

def handle(request,url):
    page = get_object_or_404(Page,slug=url)
    data = page.get_data()
   
    if data.login and not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    # breadcrumbs
    split = url.split('/')
    breadcrumbs,prefix = [],split[0]
    for item in split[1:]:
        breadcrumbs.append(prefix)
        prefix += '/' + item
    breadcrumbs.append(prefix)

    dict = {
        'page_id':page.id,
        'title':data.title,
        'text':data.text,
        'peers':cleanse(page.get_peers()),
        'children':cleanse(page.get_children()),
        'user':request.user,
        'breadcrumbs':lookup(breadcrumbs),
        'slug': url,
    }
    return render_to_response('cms/page.html',dict)
