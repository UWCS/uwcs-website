from django.core.mail import send_mail
from django.template import loader, Context
from datetime import *

def template_mail(title,template,context,addr_from,addr_to,fail_silently=False):
    template = loader.get_template(template)
    context = Context(context)
    send_mail(
        title,
        template.render(context),
        addr_from,
        addr_to,
        fail_silently=fail_silently)

def pair_map(f,list):
    vals = []
    for item in list:
        vals.append((item,f(item)))
    return vals

def current_year():
    from compsoc.memberinfo.models import Term
    return Term.objects.filter(start_number=1).order_by('start_date').reverse()[0].start_date.year

def get(tuples,key):
    for (s,l) in tuples:
        if s == key:
            return l
    raise ValueError

notime = time(0,0,0)

def begin_week(of):
    try:
        return datetime.combine((of - timedelta(days=of.weekday())).date(),notime)
    except AttributeError:
        return of - timedelta(days=of.weekday())

def flatten(list):
    return map(lambda (x,):x,list)

def path_processor(request):
    return {'path': request.path}
