from compsoc.choob.models import *
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

def quotes_page(request):
    quoters = map(lambda q:q[0],QuoteObject.objects.all().values_list('quoter').distinct())
    quoted = map(lambda q:q[0],QuoteLine.objects.all().values_list('nick').distinct())
    
    return render_to_response('choob/quotes.html',{
        'breadcrumbs': [('/','home'),('/irc/','irc')],
        'user':request.user,
        'quoters':quoters,
        'quoted':quoted,
    })

PER_PAGE = 20

def quotes_f(request,page_num,url,f):
    '''
    Generic quotes controller for making lists of quotes
    type(f) = String -> [QuoteObject]
    '''
    if request.method == 'POST':
        val = request.POST['val']
        paginator = Paginator(f(val),PER_PAGE)
        return render_to_response('choob/quote_list.html',{
            'breadcrumbs': [('/','home'),('/irc/','irc')],
            'user':request.user,
            'page':paginator.page(page_num),
            'value':val,
            'url':url,
        })
    else:
        return HttpResponseRedirect('/irc/all_quotes/')

def all_quotes(request,page_num):
    paginator = Paginator(QuoteObject.objects.all(),PER_PAGE)
    return render_to_response('choob/quote_list.html',{
        'breadcrumbs': [('/','home'),('/irc/','irc'),('/irc/all_quotes/1/','all')],
        'user':request.user,
        'page':paginator.page(page_num),
    })

# this is clearly not idiomatic in languages without currying
# perhaps someone can suggest something else
def quotes_by(request,page):
    return quotes_f(request,page,'quotes_by',
        lambda n:QuoteObject.objects.filter(quoter__exact=n))

def quotes_from(request,page):
    return quotes_f(request,page,'quotes_from',
        lambda n:QuoteObject.objects.filter(quoteline__nick__exact=n))

def quotes_with(request,page):
    return quotes_f(request,page,'quotes_with',
        lambda v:QuoteObject.objects.filter(quoteline__message__contains=v))
    
