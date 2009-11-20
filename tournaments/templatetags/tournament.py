from django import template
from math import log
from django.utils.safestring import mark_safe
from compsoc.tournaments.models import *

register = template.Library()

@register.filter
def tournament_divs(tournament):
    # TODO: make this work when tree not entirely full
    rounds = int(log(tournament.tree_size(),2))
    _,s = recurs(tournament,rounds,1)
#    print s
    return mark_safe(s)

def disp(alloc):
    return alloc.user_str()

def row(alloc,round,pos):
    return '<div class="round%i-%s">%s</div>' % (round,pos,alloc)

def outer(winner,round,pos):
    return '<div class="round%i-%swrap">\n<div class="round%i-%s">%s</div>\n' % (round,pos,round,pos,winner)

def recurs(tournament,round,index):
    pos = 'top' if (index % 2) != 0 else 'bottom'
    if round == 0:
        try:
            alloc = tournament.allocation_set.get(index=index)
            return (alloc,row(disp(alloc),round+1,pos))
        except Allocation.DoesNotExist:
            return (None,row("No one",round+1,pos))
    else:
        final = log(tournament.tree_size(),2) == round

        def inner(n):
            return recurs(tournament,round-1,n)

        # fail lack of maybe monad
        def match(w,l,f):
            try:
                return tournament.match_set.get(winner=w,looser=l)
            except:
                return f()

        (lalloc,lstr),(ralloc,rstr) = inner(2*index-1),inner(2*index)
        current_match = match(lalloc,ralloc,lambda:match(ralloc,lalloc,lambda:None))
        round += 1
        name,win = (disp(current_match.winner),current_match.winner) if current_match else ("unknown",None)
        if final:
            s = '<div class="round%i-top winner%i">%s</div>' % (round,round,name) + lstr + rstr
        else:
            s = '<div class="round%i-%swrap">\n<div class="round%i-%s">%s</div>\n' % (round,pos,round,pos,name) + lstr + rstr + '\n</div'
        return (win,s)

@register.filter
def tournament_league(tournament):
    '''
    Generates a league table
    '''
    return mark_safe("")
