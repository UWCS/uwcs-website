from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from compsoc.cms.models import *
from collections import defaultdict
from django.template import RequestContext
from compsoc.shortcuts import *

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
    breadcrumbs.sort(key=lambda x:x.title())

    # find the siblings that go before and after
    sibs = sorted(page.get_siblings_and_self(), key=lambda x: x.title())

    dict = {
        'page_id':page.id,
        'title':data.title,
        'text':data.text,
        'siblings':[(p.get_absolute_url(),p.get_data().title,p.slug == prefix) for p in sibs],
        'children':cleanse(page.get_children()),
        'breadcrumbs':lookup(breadcrumbs),
        'slug': url,
    }
    return render_to_response('cms/page.html',dict,
        context_instance=RequestContext(request,{},[path_processor]))

def list(request):
    def rec(page):
        '''
            Recursively generates a list of pages for a site map
        '''
        # If anyone knows a way of using sane tags without shoving this
        # in the view, please rewrite
        val = '<a href="%s">%s</a>' % (page.get_absolute_url(),page.title())
        pages = reduce(lambda x,y: x+y,map(rec,page.get_children()),[])
        return [val,pages] if pages else [val]

    return render_to_response('cms/list.html',{
        'list':rec(get_object_or_404(Page,slug='about')) + rec(get_object_or_404(Page,slug='contact')),
    },context_instance=RequestContext(request,{},[path_processor]))

