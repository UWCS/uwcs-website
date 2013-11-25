from django.conf.urls.defaults import patterns

urlpatterns = patterns('uwcs_website.tracker.views',
    (r'^$','index'),
    (r'^new/$','new_ticket'),
    (r'^detail/(?P<object_id>\d+)/$','details'),
)
