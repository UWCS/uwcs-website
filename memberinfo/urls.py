from django.conf.urls.defaults import *
from Compsoc.comms.models import Communication

urlpatterns = patterns('Compsoc.memberinfo.views',
    (r'^$','index'),
    (r'^shell/$','shell'),
    (r'^database/$','database'),
    (r'^quota/$','quota'),
    (r'^lists/$','lists'),
    (r'^details/$','details'),
    (r'^list/$','member_list'),
)

