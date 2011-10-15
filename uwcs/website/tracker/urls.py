from django.conf.urls.defaults import *
from uwcs.website.tracker.models import Ticket

urlpatterns = patterns('uwcs.website.tracker.views',
    (r'^$','index'),
    (r'^new/$','new_ticket'),
    (r'^detail/(?P<object_id>\d+)/$','details'),
)
