from django.conf.urls.defaults import *
from Compsoc.comms.models import Communication

urlpatterns = patterns('Compsoc.events.views',
    (r'^$','calendar_index'),
    (r'^calendar/$','calendar_index'),
    (r'^calendar/(?P<delta>-?\d+)/$','calendar'),
    (r'^details/(?P<event_id>\d+)/$','details'),
    (r'^signup/(?P<event_id>\d+)/$','do_signup'),
    (r'^unsignup/(?P<event_id>\d+)/$','do_unsignup'),
    (r'^ical/$','ical_feed'),
)

