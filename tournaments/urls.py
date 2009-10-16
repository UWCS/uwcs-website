from django.conf.urls.defaults import *

urlpatterns = patterns('tournaments.views',
    (r'^$','tournament_list'),
    (r'^detail/(?P<id>\d+)/$','tournament_detail'),
)

