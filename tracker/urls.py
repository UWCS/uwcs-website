from django.conf.urls.defaults import *
from compsoc.tracker.models import Ticket

urlpatterns = patterns('compsoc.tracker.views',
    (r'^$','index'),
    (r'^new/$','new_ticket'),
    (r'^detail/(?P<object_id>\d+)/$','details'),
)
