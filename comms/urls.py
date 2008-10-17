from django.conf.urls.defaults import *
from Compsoc.comms.models import Communication

def get_dict(item_type):
    return {
        'queryset':Communication.objects.filter(type=item_type),
        'paginate_by':10,
        'extra_context':{'type':item_type,},
    }

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$','object_list',get_dict('N')),
    (r'^news/(?P<page>[0-9]+)/$','object_list',get_dict('N')),
    (r'^minutes/(?P<page>[0-9]+)/$','object_list',get_dict('M')),
    (r'^newsletters/(?P<page>[0-9]+)/$','object_list',get_dict('NL')),
    (r'^details/(?P<object_id>\d+)/$', 'object_detail',{'queryset':Communication.objects.all()}),
)

