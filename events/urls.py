from django.conf.urls.defaults import *
from compsoc.events.models import Location 

urlpatterns = patterns('compsoc.events.views',
    (r'^$','events_list'),
    (r'^calendar/$','calendar_index'),
    (r'^calendar/(?P<delta>-?\d+)/$','calendar'),
    (r'^details/(?P<event_id>\d+)/$','details'),
    (r'^signup/(?P<event_id>\d+)/$','do_signup'),
    (r'^unsignup/(?P<event_id>\d+)/$','do_unsignup'),
    (r'^ical/$','ical_feed'),
    (r'^ical2/$','ical_feed2'),
    (r'^seating/(?P<event_id>\d+)/$', 'seating'),
    (r'^seating/(?P<event_id>\d+)/(?P<revision_no>\d+)/$', 'seating'),
    (r'^location/(?P<object_id>\d+)/$','location'),
    (r'^friends/$','lan_friends'),
    (r'^activity/$','activity'),
)

