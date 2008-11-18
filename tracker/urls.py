from django.conf.urls.defaults import *
from compsoc.tracker.models import Ticket

urlpatterns = patterns('compsoc.tracker.views',
    (r'^$','index'),
    (r'^new/$','new_ticket'),
)

info_dict = {
    'queryset': Ticket.objects.all(),
    'template_name':'tracker/details.html',
}

urlpatterns += patterns('django.views.generic',
    (r'^detail/(?P<object_id>\d+)/$', 'list_detail.object_detail',info_dict),
)
