from collections import defaultdict
from datetime import date,datetime,timedelta,time
from time import strftime

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django import forms

import vobject
import re

from compsoc.events.models import *
from compsoc.settings import DATE_FORMAT_STRING,WEEK_FORMAT_STRING
from compsoc.memberinfo.models import warwick_week_for,Term
from compsoc.shortcuts import begin_week

def calendar_index(request): return calendar(request,0)

def month(dat): return strftime("%b",(0,dat,0,0,0,0,0,0,0))

a_week = timedelta(days=7)
    
def safe_week_for(date):
    dt = datetime(date.year,date.month,date.day)
    try:
        return str(warwick_week_for(dt))
    except Term.DoesNotExist:
        return ""

def get_events(offset,span):
    begin = begin_week(datetime.today())+timedelta(days=7*offset)
    end = begin + timedelta(days=7*span)
    events = Event.objects.order_by('start').filter(finish__gte=begin)

def get_listable_events(offset,span):
    begin = begin_week(datetime.today())+timedelta(days=7*offset)
    end = begin + timedelta(days=7*span)
    events = Event.objects.order_by('start').filter(finish__gte=begin).exclude(displayFrom__gte=datetime.now())
    return (begin.date(),end.date(),events)

class Week:
    '''
    Abstract a week, so the template doesn't require any lookup logic
    '''
    def __init__(self,begin):
        self.begin = begin
        self.end = begin + timedelta(days=6)
        self.week_number = safe_week_for(begin)
    def __str__(self):
        return self.begin.strftime(WEEK_FORMAT_STRING)+" - "+self.end.strftime(WEEK_FORMAT_STRING)

def events_list(request):
    begin,end,events = get_listable_events(0,10)
    lookup = defaultdict(lambda: [])
    for event in events:
       lookup[begin_week(event.start)].append(event)

    lookup = map(lambda (begin,events): (Week(begin),events),sorted(lookup.items()))
    return render_to_response('events/list.html', {
        'breadcrumbs': [('/','home'),('/events/','events')],
        'user':request.user,
        'events':lookup,
        'future':future_events()
    })

def calendar(request,delta):
    '''
    Main Calendar view for website
    presents a Table of events for the current week, and 4 successors
    '''
    offset = int(delta)
    begin,end,events = get_events(offset,4)
    # lookup :: BEGIN_WEEK -> DAY -> EVENT
    lookup = defaultdict(lambda: defaultdict(lambda:[]))
    for event in events:
        for event_date in event.days():
            lookup[begin_week(event_date)][event_date.weekday()].append(event)

    # tidy information
    iter,events = begin,[]
    while iter <= end:
        week = lookup[iter]
        week_vals = []
        for i in range(0,7):
            iter_date = iter+timedelta(i)
            if (iter==begin and i==0) or iter_date.day==1:
                val = month(iter_date.month)
            else:
                val = ""
            week_vals.append((val+" "+str(iter_date.day),lookup[iter][i]))
        events.append((safe_week_for(iter),week_vals))
        iter += a_week

    return render_to_response('events/calendar.html',{
        'breadcrumbs': [('/','home'),('/events/','events'),('/events/calendar/','calendar')],
        'events':events,
        'current':date.today(),
        'prev':offset-1,
        'next':offset+1,
        'user':request.user,
        'future':future_events(),
    })

def valid_signup(user,event):
    now = datetime.now()
    s = event.eventsignup
    if event.has_signups() and user.is_authenticated():
        can_signup = now < s.close and not event.cancelled
        if user.member.is_fresher():
            can_signup &= s.fresher_open < now
        elif user.member.guest:
            can_signup &= s.guest_open < now
        else:
            can_signup &= s.open < now
    else:
        can_signup = False
    return can_signup
    
def details(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    signups = event.signup_set.order_by('time')
    max = event.signup_total()
    # 0 = inifnite signups
    if max:
        reserved = signups[max:]
        signups = signups[:max]
    else:
        reserved = []

    u = request.user
    
    dict = {
        'event':event,
        'signups':signups,
        'reserved':reserved,
        'can_edit':request.user.is_staff if request.user else False,
        'user':u,
        'future':future_events(),
        'is_displayed':event.is_displayed(),
    }

    try:
        s = event.eventsignup
        signed_up = u.is_authenticated() and event.signup_set.filter(user=request.user)
        dict.update({
            'open':s.open.strftime(DATE_FORMAT_STRING),
            'close':s.close.strftime(DATE_FORMAT_STRING),
            'fresher':s.fresher_open.strftime(DATE_FORMAT_STRING),
            'guest':s.guest_open.strftime(DATE_FORMAT_STRING),
            'limit':s.signupsLimit,
            'can_signup':valid_signup(u,event) and not signed_up,
            'signed_up':signed_up,
            'has_seating':s.seating,
        })
    except EventSignup.DoesNotExist, e:
        dict.update({ 'can_signup':False })

    return render_to_response('events/details.html',dict)

p = re.compile(r"col([0-5])\((.*),\)")

# assumes initial revision
def seating(request, event_id, revision_no=None):
    e = get_object_or_404(Event, id=event_id)
    dict = {
            'user':request.user,
            'event':e,
            'future':future_events(),
           }
    try:
        signup = e.eventsignup
        if signup.has_seating_plan():
            room = signup.seating
            closed = signup.close < datetime.now()

            if request.method == 'POST' and request.user.is_authenticated():
                if closed:
                    return render_to_response('events/plan_closed.html')
                order = request.POST['order']
                previous = SeatingRevision.objects.filter(event=e).order_by('-number')
                last_no = previous[0].number if previous else 0
                revision = e.seatingrevision_set.create(
                    creator=request.user,
                    comment=request.POST['comment'],
                    number=last_no+1
                )
                for col in order.split(';'):
                    m = p.match(col)
                    if m:
                        column = int(m.group(1))
                        for row,id_string in enumerate(m.group(2).split(',')):
                            try:
                                u = User.objects.get(id=int(id_string))
                                revision.seating_set.create(user=u,col=column,row=row)
                            except ValueError,User.DoesNotExist: pass
                revisions = SeatingRevision.objects.for_event(e)
            else:
                revisions = SeatingRevision.objects.for_event(e)
                if revisions:
                    revision = revisions[0] if revision_no==None else SeatingRevision.objects.get(number=revision_no,event=e)
            
            # create a seat lookup dict
            seat_dict = defaultdict(lambda: defaultdict(lambda: False))
            unass = set([s.user for s in e.signup_set.all()])
            if revisions:
                for seat in revision.seating_set.all():
                    seat_dict[seat.col][seat.row] = seat.user
                    unass.discard(seat.user)
                    #unass.remove(seat.user)

            # create nested lists for rows and columns
            cols = range(0,room.max_cols)
            max_rows = [ max([-1]+seat_dict[y].keys())+1 for y in cols]
            s = [[seat_dict[y][x] for x in range(0,max_rows[y])] for y in cols]
            
            dict.update({
                'room':room,
                'seating':s,
                'seating_revisions':revisions,
                'new_revision_no':revisions[0].number+1 if revisions else 0,
                'unassigned':unass,
                'notclosed':not closed,
                })
    except EventSignup.DoesNotExist: pass

    return render_to_response('events/seating.html', dict)

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=100)

@login_required
def do_signup(request,event_id):
    '''
    Post:
        If a user is signed up then change their comment
        otherwise add signup entry if its valid to
    Get:
        return a form, if they are signed up, it should have their contacts in
    '''
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['comment']
            try:
                e = event.signup_set.get(user=request.user)
                e.comment = c
                e.save()
            except Signup.DoesNotExist:
                if valid_signup(request.user,event):
                    event.signup_set.create(time=datetime.now(),user=request.user,comment=c)
                else:
                    return render_to_response('events/cantsignup.html',{'event':event})
                
# TODo: add to admin section
#                if event.signup_set.filter(user=request.user):
#                    return render_to_response('events/alreadysignedup.html',{'event':event})
        return render_to_response('events/signup.html',{'event_id':event_id, 'user':request.user})
    else:
        form = CommentForm()
        try:
            e = event.signup_set.get(user=request.user)
        except Signup.DoesNotExist: pass

    return render_to_response('events/edit_signup.html', {
        'form': form,
        'event_id': event_id,
        'user':request.user,
    })

@login_required
def do_unsignup(request,event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        signup = event.signup_set.get(user=request.user)
        signup.delete()
    except Signup.DoesNotExist:
        return render_to_response('events/nonsignup.html',{'event':event,'user':request.user})
    return render_to_response('events/unsignup.html',{'event_id':event_id,'user':request.user})

def ical_feed(request):
    '''
    Generates an ical sync of all events in the future
    '''
    cal = vobject.iCalendar()
    # IE/Outlook needs this:
    cal.add('method').value = 'PUBLISH'
    # Only publish events in the future
    for event in filter(lambda e: e.is_in_future(),Event.objects.order_by('start')):
        vevent = cal.add('vevent')
        vevent.add('summary').value = event.type.name + '; ' + event.shortDescription if event.shortDescription else event.type.name
        vevent.add('location').value = str(event.location)
        vevent.add('dtstart').value = event.start
        vevent.add('dtend').value = event.finish
        vevent.add('dtstamp').value = event.start # again, for Outlook
        vevent.add('description').value = event.longDescription
        vevent.add('categories').value = [event.type.get_target_display()]
        url = "http://%s/events/details/%i/" % (Site.objects.get_current() , event.id)
        vevent.add('uid').value = url
        vevent.add('url').value = url
    response = HttpResponse(cal.serialize(), mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=filename.ics'
    return response

def location(request,object_id):
    '''
    Location details page controller
    '''
    loc = Location.objects.get(pk=object_id)
    return render_to_response("events/location_detail.html", {
        'object':loc,
        'map_room':loc.map_loc,
        'user':request.user,
    })
