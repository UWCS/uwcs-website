from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from compsoc.cms.models import *
    
def cleanse(l):
    return map(lambda p: (p.get_absolute_url(),p.get_data().title),l)

def lookup(l):
    breadcrumbs = [('/','home')]
    for url in l:
        try:
            page = Page.objects.get(slug=url)
            breadcrumbs.append(
                (page.get_absolute_url(),page.get_data().title))
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

    # find the siblings that go before and after
    sibs = sorted(page.get_siblings_and_self(), key=lambda x: x.title())
    i = [str(p) for p in sibs].index(prefix)
    pre_siblings = sibs[:i]
    post_siblings = sibs[i+1:]

    dict = {
        'page_id':page.id,
        'title':data.title,
        'text':data.text,
        'pre_siblings':cleanse(pre_siblings),
        'post_siblings':cleanse(post_siblings),
        'children':cleanse(page.get_children()),
        'user':request.user,
        'breadcrumbs':lookup(breadcrumbs),
        'slug': url,
    }
    return render_to_response('cms/page.html',dict)
