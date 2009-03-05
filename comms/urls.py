from time import strftime

from django.conf.urls.defaults import *

from compsoc.comms.models import Communication,COMMS_TYPE
from compsoc.shortcuts import current_year,get
from compsoc.events.models import future_events

def from_date(date):
    return (date.year,strftime("%b",(0,date.month,0,0,0,0,0,0,0)))

def lookup(item_type):
    data = Communication.objects.filter(type=item_type).order_by('-date')
    store = {}
    for comm in data:
        store[from_date(comm.date)] = True
    return store.keys()

def get_dict(item_type,paginate=True,intro=False):
    data = Communication.objects.filter(type=item_type).order_by('-date')
    info_dict = {
        'queryset':data,
        'template_name':'comms/list.html',
        'extra_context':{
            'type':get(COMMS_TYPE,item_type).lower(),
            'dates':lambda: lookup(item_type),
            'future':lambda: future_events(),
            'intro':intro,
        },
    }
    if paginate:    info_dict['paginate_by'] = 10
    else:           info_dict['date_field'] = 'date'
    return info_dict

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$','object_list',get_dict('N', intro=True)),
    (r'^news/(?P<page>[0-9]+)/$','object_list',get_dict('N')),
    (r'^minutes/(?P<page>[0-9]+)/$','object_list',get_dict('M')),
    (r'^newsletters/(?P<page>[0-9]+)/$','object_list',get_dict('NL')),
    (r'^details/(?P<object_id>\d+)/$', 'object_detail',{
        'queryset':Communication.objects.all(),
        'extra_context':{
            'future':lambda: future_events(),
        },
    }),

) + patterns('django.views.generic.date_based',
    (r'^monthnews-items/(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/$','archive_month',get_dict('N',False)),
    (r'^monthminutes/(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/$','archive_month',get_dict('M',False)),
    (r'^monthnewsletters/(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/$','archive_month',get_dict('NL',False)),
)
