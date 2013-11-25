from django.conf.urls.defaults import patterns
from django.forms import ModelForm

from uwcs_website.elections import models

class VoteForm(ModelForm):
    class Meta:
        model = models.Vote
        fields = ('candidate', 'preference')

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': models.Election.objects.all(),
    }),
    #(r'^details/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {
        #'queryset':Election.objects.all(),
    #}),
    (r'^details/(?P<object_id>[^/]+)/$', 'uwcs_website.elections.views.details'),
    (r'^summary/(?P<object_id>[^/]+)/$', 'uwcs_website.elections.views.summary'),
    (r'^checklist/(?P<object_id>[^/]+)/$', 'uwcs_website.elections.views.checklist_page'),
    (r'^ballotform/(?P<object_id>[^/]+)/$', 'uwcs_website.elections.views.printable_ballot_form'),
)
