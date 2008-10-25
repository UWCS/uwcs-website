from django.conf.urls.defaults import *
from compsoc.comms.models import Communication

urlpatterns = patterns('compsoc.memberinfo.views',
    (r'^$','index'),
    (r'^shell/$','shell'),
    (r'^database/$','database'),
    (r'^quota/$','quota'),
    (r'^lists/$','lists'),
    (r'^details/$','details'),
    (r'^list/$','member_list'),
    (r'^reset/$','reset_password'),
    (r'^reset/(?P<account>.*)/$$','reset_account'),
)

