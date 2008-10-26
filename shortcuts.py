from django.core.mail import send_mail
from django.template import loader, Context
from datetime import timedelta

def template_mail(title,template,context,addr_from,addr_to,fail_silently=False):
    template = loader.get_template(template)
    context = Context(context)
    send_mail(
        title,
        template.render(context),
        addr_from,
        addr_to,
        fail_silently=fail_silently)

def current_year():
    from compsoc.memberinfo.models import Term
    return Term.objects.filter(start_number=1).order_by('start_date').reverse()[0].start_date.year

def get(tuples,key):
    for (s,l) in tuples:
        if s == key:
            return l
    raise ValueError

def begin_week(of): return of - timedelta(days=of.weekday())
