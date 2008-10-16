from django.conf.urls.defaults import *
from Compsoc.comms.models import Communication

info_dict = {
    'queryset':Communication.objects.all(),
#    'date_field':'date',
}

urlpatterns = patterns('',
    (r'^$','django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',info_dict),
)

