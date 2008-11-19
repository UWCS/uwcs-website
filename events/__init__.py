from compsoc.settings import CHOOB_FILE
from time import mktime
from datetime import datetime

def mapred(f1,f2,list):
    return reduce(f1,map(f2,list))

def write_file_callback(sender, **kwargs):
    from compsoc.events.models import Event
    choob_file = open(CHOOB_FILE,"w")
    events = filter(lambda e:e.is_in_future() or e.is_running(),Event.objects.all())
    print events
    if events:
        choob_file.write(mapred(lambda x,y: x+' '+y,lambda e:str(e.id),events)+'\n')
        for event in events:
            signups = event.signup_set.all()
            if signups:
                signups = mapred(lambda x,y:x+', '+y,lambda e:e.user.member.name(),signups)
            else:
                signups = ' '
            choob_file.write('%i "%s" %i %i %s %i %i "%s" "%s" "%s"\n' % (
                event.id,
                event.type.name,
                mktime(event.start.timetuple()),
                mktime(event.finish.timetuple()),
                make_signup_code(event),
                event.signup_total(),
                event.signup_count(),
                signups,
                event.shortDescription,
                event.location,
            ))
    choob_file.close()

def make_signup_code(event):
    if event.is_running():
        return 'R'
    elif event.has_signups():
        s = event.eventsignup
        if s.open < datetime.now():
            return 'SN'
        elif s.guest_open < datetime.now():
            return 'SO'
        else:
            return 'S'
    else:
        return '-'
