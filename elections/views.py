from django.forms import ModelForm
from models import Vote, Candidate, Election
from django.shortcuts import render_to_response,get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.widgets import HiddenInput, Widget, TextInput
from django import forms
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt, ErrorDict, ErrorList, ValidationError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from itertools import groupby
from datetime import datetime
from django.contrib.auth.models import User
# Create your views here.

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ('preference')

def validate_position(vote_forms):
    """
    Checks that:
    1) Each form has a preference of 1-len(candidates)
    2) No duplicate preferences
    """
    candidate_count = len(vote_forms)
    seen_already = []

    for form in vote_forms:
        if form.is_valid():
            p = form.cleaned_data['preference']

            if p < 1:
                form._errors['preference'] = ErrorList([u"Can't enter a preference above 1"])
                return False
            elif p > candidate_count:
                form._errors['preference'] = ErrorList([u"Can't enter a preference below the number of candidates (%s)" % candidate_count])
                return False
            elif p in seen_already:
                form._errors['preference'] = ErrorList([u"Can't enter duplicate preferences"])
                return False
            seen_already.append(p)
        else:
            # we take incomplete forms as no further preferences
            form._errors['preference'] = ErrorList([])
    return True

def validate_vote_forms(forms):
    """
    Breaks up into positions and validates each position
    """
    positions = groupby(forms, lambda f: f.instance.candidate.position)
    return all([validate_position(list(forms)) for position,forms in positions])

@login_required
def details(request, object_id):
    """
    Renders the online voting form for a specific election
    """
    election = get_object_or_404(Election, id=object_id)

    # guests can't vote
    if request.user.member.guest:
        return render_to_response('elections/noguest.html', {}, context_instance=RequestContext(request))

    # if proxy votes have closed
    if datetime.now() > election.close_date:
        return render_to_response('elections/closed.html', {
            'election':election,
        },context_instance=RequestContext(request))

    # if the user has already voted for this election
    if Vote.objects.filter(voter=request.user, candidate__position__election=election):
        return render_to_response('elections/thankyou.html', {
            'election':election,
        },context_instance=RequestContext(request))

    # I officially have no idea how to use formsets for this, sod it.
    if request.method == 'POST':
        candidates = Candidate.objects.filter(position__election=object_id)
        votes = [Vote(candidate=c, voter=request.user) for c in candidates]
        forms = [VoteForm(request.POST, prefix=str(v.candidate.id), instance=v) for v in votes]
        if validate_vote_forms(forms):
            for form in forms:
                if form.is_valid():
                    form.save()
            return render_to_response('elections/thankyou.html', {
                'election':election
            },context_instance=RequestContext(request))
        else:
            return render_to_response('elections/election_detail.html', {
                'election':election,
                'stuff':zip(candidates, forms),
            },context_instance=RequestContext(request))
    else:
        candidates = Candidate.objects.filter(position__election=object_id)
        votes = [Vote(candidate=c, voter=request.user) for c in candidates]
        forms = [VoteForm(instance=v, prefix=str(v.candidate.id)) for v in votes]
        # XXX: RequestContext
        return render_to_response('elections/election_detail.html', {
            'election':election,
            'stuff':zip(candidates, forms),
        },context_instance=RequestContext(request))

@staff_member_required
def summary(request, object_id):
    """
    Returns a set of ballots entered into the database.
    """
    election = get_object_or_404(Election, id=object_id)
    votes = Vote.objects.filter(candidate__position__election=object_id).order_by('voter','candidate__position')

    return render_to_response('elections/election_summary.html',{
        'election':election,
        'now':datetime.now(),
        'votes':votes,
    },context_instance=RequestContext(request))

def checklist(items1, items2):
    """
    Returns [(Bool, Item)], where each Item is from the second argument,
    and the Bool marks whether it existed in the first argument.
    """
    ret = [(False,x) for x in items2]
    for x in items1:
        try:
            i = items2.index(x)
            ret[i] = (True,ret[i][1])
        except ValueError:
            pass
    return ret

@staff_member_required
def checklist_page(request, object_id):
    """
    Renders a simple page with a checklist useful for AGM events
    """
    election = get_object_or_404(Election, id=object_id)

    active_users = User.objects.filter(is_active=True,member__guest=False).order_by('username')
    votes = Vote.objects.filter(candidate__position__election=object_id).order_by('voter')

    voter_usernames = [v.voter.username for v in votes]
    active_usernames = [u.username for u in active_users]

    return render_to_response('elections/checklist.html',{
        'checklist':checklist(voter_usernames, active_usernames)
    },context_instance=RequestContext(request))

@staff_member_required
def printable_ballot_form(request, object_id):
    """
    Renders a simple printable ballot form.
    """
    election = get_object_or_404(Election, id=object_id)

    return render_to_response('elections/ballot_form.html', {
        'election':election,
        'candidates':Candidate.objects.filter(position__election=object_id)
    },context_instance=RequestContext(request))



    active_users = User.objects.filter(is_active=True,member__guest=False).order_by('username')
    votes = Vote.objects.filter(candidate__position__election=object_id).order_by('voter')

    voter_usernames = [v.voter.username for v in votes]
    active_usernames = [u.username for u in active_users]

    return render_to_response('elections/checklist.html',{
        'checklist':checklist(voter_usernames, active_usernames)
    },context_instance=RequestContext(request))
