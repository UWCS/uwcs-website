from django.conf.urls.defaults import patterns

urlpatterns = patterns('uwcs_website.tournaments.views',
    (r'^$','tournament_list'),
    (r'^detail/(?P<id>\d+)/$','tournament_detail'),
    (r'^add_player/(?P<id>\d+)/$','add_player_to_tournament'),
)

