from django.conf.urls.defaults import *
from Compsoc.feeds import *
from Compsoc import settings
from Compsoc.cms.views import handle

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
    (r'^', include('Compsoc.comms.urls')),
    (r'^member/', include('Compsoc.memberinfo.urls')),
    (r'^events/', include('Compsoc.events.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^admin/cms/page/(?P<page_id>\d+)/$','Compsoc.cms.admin_views.add_edit'),
    (r'^admin/cms/page/add/$','Compsoc.cms.admin_views.add_edit'),
    (r'^admin/events/email/(?P<event_id>\d+)/$','Compsoc.events.admin_views.email_signups'),
    (r'^admin/(.*)', admin.site.root),

    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^password/', 'django.contrib.auth.views.password_change', {'template_name':'password.html','post_change_redirect':'/'}),

    (r'^cms/(?P<url>.*)',handle),

)

# if we are debugging serve the static content locally
# when deployed we use an http server to do this
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),
    )
