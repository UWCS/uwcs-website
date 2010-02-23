from django.conf.urls.defaults import *
import settings
from models import Society

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset':Society.objects.all(),
        'paginate_by':10,
    }),
    (r'^details/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {
        'queryset':Society.objects.all(),
    }),
)
