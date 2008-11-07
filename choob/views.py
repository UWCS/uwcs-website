from compsoc.choob.models import *
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect

def quotes_page(request):
    quoters = set()
    # one wonders how this performs
    for quote in QuoteObject.objects.all():
        quoters.add(quote.quoter)

    quoted = set()
    for quote_line in QuoteLine.objects.all():
        quoted.add(quote_line.nick)

    return render_to_response('choob/quotes.html',{
        'user':request.user,
        'quoters':quoters,
        'quoted':quoted,
    })

def quotes_f(request,f):
    '''
    Generic quotes controller for making lists of quotes
    type(f) = String -> [QuoteObject]
    '''
    if request.method == 'POST': 
        val = request.POST['val']
        return render_to_response('choob/quote_list.html',{
            'user':request.user,
            'objects':f(val),
        })
    else:
        return HttpResponseRedirect('/irc/all_quotes/')

def all_quotes(request):
    return render_to_response('choob/quote_list.html',{
        'user':request.user,
        'objects':QuoteObject.objects.all(),
    })
    

def quotes_by(request):
    return quotes_f(request,
        lambda n:QuoteObject.objects.filter(quoter__exact=n))

def quotes_from(request):
    return quotes_f(request,
        lambda n:QuoteObject.objects.filter(quoteline__nick__exact=n))

def quotes_with(request):
    return quotes_f(request,
        lambda v:QuoteObject.objects.filter(quoteline__message__contains=v))
    
