from django.conf.urls.defaults import patterns

from uwcs_website.memberinfo.models import Society

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset':Society.objects.all(),
        'paginate_by':10,
    }),
    (r'^details/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {
        'queryset':Society.objects.all(),
    }),
)
