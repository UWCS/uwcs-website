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
    from uwcs.website.memberinfo.models import Term
    return Term.objects.filter(start_date__lte=datetime.today(),start_number=1).latest('start_date').start_date.year

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

def cast_to_submodel(instance, subclass, **extra):
    """
    Casts an instance of a model Base to an instance of a model Derived.
    Does not commit anything, you need to do this yourself.

    You can pass in extra arguments for the derived model as keyword args.
    """
    superclass = instance.__class__
    superclass_fields = superclass.objects.filter(id=instance.id).values()[0]
    superclass_fields.update(extra);

    subclass_instance = subclass(**superclass_fields);
    ancestor_link_name = subclass_instance._meta.get_ancestor_link(superclass).name
    setattr(subclass_instance, ancestor_link_name, instance)
    return subclass_instance
