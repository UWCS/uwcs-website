from django import template
from math import log
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def tournament_divs(tournament):
    # TODO: make this work when tree not entirely full
    rounds = int(log(tournament.tree_size(),2))
    final = tournament.match_set.get(round=rounds)
    s = recursive_divs(final,rounds,'top',True)
    return mark_safe(s)

def disp(alloc):
    return alloc.user.member.name()

def row(alloc,round,pos):
    return '<div class="round%i-%s">%s</div>' % (round,pos,disp(alloc))

def outer(winner,round,pos):
    return '<div class="round%i-%swrap">\n<div class="round%i-%s">%s</div>\n' % (round,pos,round,pos,disp(winner))

def recursive_divs(match,round,pos,final):
    [l,r] = sorted([match.winner,match.looser],key=lambda x:x.index)
    next = round + 1
    if round == 1:
        return outer(match.winner,next,pos)+row(l,round,'top')+'\n'+row(r,round,'bottom')+'\n</div>\n'
    else:
        round = round - 1
        def bottom(alloc,pos):
            return recursive_divs(alloc.wins.get(round=round),round,pos,False)
        return '<div class="round%i-top %s">%s</div>' % (next,"winner%i" % next if final else '',disp(match.winner)) + bottom(l,'top') + bottom(r,'bottom')
