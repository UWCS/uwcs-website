from django.conf.urls.defaults import *
from compsoc.comms.models import Communication

urlpatterns = patterns('compsoc.memberinfo.views',
    (r'^$','index'),
    (r'^shell/$','shell'),
    (r'^database/$','database'),
    (r'^quota/$','quota'),
    (r'^lists/$','lists'),
    (r'^list/$','member_list'),
    (r'^reset/$','reset_password'),
    (r'^reset/(?P<account>.*)/$','reset_account'),
    url(r'^guest/$','create_guest',name='guest_account'),
    (r'^nickname/$','set_nickname'),
    (r'^website/$','set_website'),
    (r'^publish/$','set_publish'),
    (r'^gamingids/$','set_gameids'),
    (r'^profile/(?P<userid>\d+)/$','profiles'),
)

