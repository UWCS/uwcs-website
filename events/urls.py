from django.conf.urls.defaults import *
from compsoc.comms.models import Communication

urlpatterns = patterns('compsoc.events.views',
    (r'^$','events_list'),
    (r'^calendar/$','calendar_index'),
    (r'^calendar/(?P<delta>-?\d+)/$','calendar'),
    (r'^details/(?P<event_id>\d+)/$','details'),
    (r'^signup/(?P<event_id>\d+)/$','do_signup'),
    (r'^unsignup/(?P<event_id>\d+)/$','do_unsignup'),
    (r'^ical/$','ical_feed'),
    (r'^seating/(?P<event_id>\d+)/$', 'seating'),
    (r'^seating/(?P<event_id>\d+)/(?P<revision_no>\d+)/$', 'seating'),
)

