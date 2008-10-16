from django.conf.urls.defaults import *
from Compsoc.feeds import *
from Compsoc import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# See feeds.py for details
feeds = {
    'news': LatestNews,
    'news/atom': LatestAtomNews,
    'events': NextEvents,
    'events/atom': NextAtomEvents,
    'minutes': LatestMinutes,
    'minutes/atom': LatestAtomMinutes,
}

urlpatterns = patterns('',
    # The feeds section of the website corresponds to the comms app
    (r'^', include('Compsoc.comms.urls')),
    (r'^member/', include('Compsoc.memberinfo.urls')),
    (r'^events/', include('Compsoc.events.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)

# if we are debugging serve the static content locally
# when deployed we use an http server to do this
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),
    )
