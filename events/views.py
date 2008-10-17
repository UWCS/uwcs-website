from collections import defaultdict
from datetime import date,datetime,timedelta,time
from time import strftime

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

import vobject

from Compsoc.events.models import *
from Compsoc.config import DATE_FORMAT_STRING

def begin_week(of): return of - timedelta(days=of.weekday())

def calendar_index(request): return calendar(request,0)

def month(dat): return strftime("%b",(0,dat,0,0,0,0,0,0,0))

a_week = timedelta(days=7)

def calendar(request,delta):
    '''
    Main Calendar view for website
    presents a Table of events for the current week, and 4 successors
    '''
    offset = int(delta)
    begin = begin_week(datetime.today())+timedelta(days=7*offset)
    end = begin + timedelta(days=28)

    events = filter(lambda event: begin < event.start and event.finish < end,Event.objects.all())
    # lookup :: BEGIN_WEEK -> DAY -> EVENT
    lookup = defaultdict(lambda: defaultdict(lambda:[]))
    for event in events:
        for event_date in event.days():
            lookup[begin_week(event_date)][event_date.weekday()].append(event)
    
    begin,end = begin.date(),end.date()
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
        events.append((iter,week_vals))
        iter += a_week

    return render_to_response('events/calendar.html',{
        'events':events,
        'current':date.today(),
        'prev':offset-1,
        'next':offset+1,
        'user':request.user,
    })

def valid_signup(user,event):
    now = datetime.now()
    s = event.eventsignup
    if event.signupsRequired and user.is_authenticated():
        can_signup = now < s.close
        try:
            if user.member.is_fresher():
                can_signup &= s.fresher_open < now
            else:
                can_signup &= s.open < now
        # Guests have no 'member' object
        except Member.DoesNotExist:
            can_signup &= s.guest_open < now
    else:
        can_signup = False
    return can_signup
    
    
def details(request,event_id):
    event = Event.objects.get(id=event_id)
    signups = event.signup_set.all()
    
    dict = {
        'event':event,
        'signups':signups,
        'can_edit':request.user.is_staff if request.user else False,
    }

    try:
        s = event.eventsignup
        signed_up = event.signup_set.filter(user=request.user)
        dict.update({
            'open':s.open.strftime(DATE_FORMAT_STRING),
            'close':s.close.strftime(DATE_FORMAT_STRING),
            'fresher':s.fresher_open.strftime(DATE_FORMAT_STRING),
            'guest':s.guest_open.strftime(DATE_FORMAT_STRING),
            'limit':s.signupsLimit,
            'can_signup':valid_signup(request.user,event) and not signed_up,
            'signed_up':signed_up,
        })
    except EventSignup.DoesNotExist:
        dict.update({ 'can_signup':False })

    return render_to_response('events/details.html',dict)

@login_required
def do_signup(request,event_id):
    try:
        event = Event.objects.get(id=event_id)
        c = request.POST['comment']
        if event.signup_set.filter(user=request.user):
            return render_to_response('events/alreadysignedup.html',{'event':event})
        elif valid_signup(request.user,event):
            event.signup_set.create(time=datetime.now(),user=request.user,comment=c)
            event.save()
        else:
            return render_to_response('events/cantsignup.html',{'event':event})
    except Event.DoesNotExist:
        return render_to_response('events/nonevent.html')
    except MultiValueDictKeyError:
        return render_to_response('events/cantsignup.html',{'event':event})
    return render_to_response('events/signup.html',{'event_id':event_id})

@login_required
def do_unsignup(request,event_id):
    try:
        event = Event.objects.get(id=event_id)
        signup = event.signup_set.get(user=request.user)
        signup.delete()
    except Event.DoesNotExist:
        return render_to_response('events/nonevent.html')
    except Signup.DoesNotExist:
        return render_to_response('events/nonsignup.html',{'event':event})
    return render_to_response('events/unsignup.html',{'event_id':event_id})

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
        vevent.add('summary').value = event.type.name
        vevent.add('location').value = event.location
        vevent.add('dtstart').value = event.start
        vevent.add('dtend').value = event.finish
        vevent.add('dtstamp').value = event.start # again, for Outlook
        vevent.add('description').value = event.longDescription
        vevent.add('categories').value = event.type.get_target_display()
        url = "%s/events/details/%i/" % (Site.objects.get_current() , event.id)
        vevent.add('uid').value = url
        vevent.add('url').value = url
    print cal.serialize()
    response = HttpResponse(cal.serialize(), mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=filename.ics'
    return response