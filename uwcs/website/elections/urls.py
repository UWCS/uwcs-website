from django.forms import ModelForm
from django.conf.urls.defaults import *

import views
from models import *

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ('candidate', 'preference')

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset':Election.objects.all(),
    }),
    #(r'^details/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {
        #'queryset':Election.objects.all(),
    #}),
    (r'^details/(?P<object_id>[^/]+)/$', views.details),
    (r'^summary/(?P<object_id>[^/]+)/$', views.summary),
    (r'^checklist/(?P<object_id>[^/]+)/$', views.checklist_page),
    (r'^ballotform/(?P<object_id>[^/]+)/$', views.printable_ballot_form),
)
