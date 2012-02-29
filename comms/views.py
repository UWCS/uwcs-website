from datetime import datetime, timedelta

from compsoc.events.models import Event
from django.views.generic.simple import direct_to_template

# Create your views here.

def generate_newsletter(request, delta=0):
    delta = int(delta)
    return direct_to_template(
        request,
        template='comms/newsletter.html',
        extra_context={
            'previous': '/newsletters/generate/%d' % (delta - 1),
            'next': '/newsletters/generate/%d' % (delta + 1),
            'events': Event.objects.for_week(datetime.now() + timedelta(weeks=delta))
        },
    )
