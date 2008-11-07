from django.conf.urls.defaults import *
from compsoc.feeds import *
from compsoc import settings
from compsoc.cms.views import handle
from compsoc.search.views import search
from django.contrib.auth.models import User

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
    (r'^', include('compsoc.comms.urls')),
    (r'^member/', include('compsoc.memberinfo.urls')),
    (r'^events/', include('compsoc.events.urls')),
    (r'^irc/', include('compsoc.choob.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^admin/cms/page/(?P<page_id>\d+)/$','compsoc.cms.admin_views.add_edit'),
    (r'^admin/cms/pagerevision/(?P<rev_id>\d+)/$','compsoc.cms.admin_views.revision'),
    (r'^admin/cms/page/add/$','compsoc.cms.admin_views.add_edit'),
    (r'^admin/memberinfo/guests/$','compsoc.memberinfo.admin_views.guest_list'),
    (r'^admin/memberinfo/acceptguest/(?P<user_id>\d+)/$','compsoc.memberinfo.admin_views.accept_guest'),
    (r'^admin/memberinfo/rejectguest/(?P<user_id>\d+)/$','compsoc.memberinfo.admin_views.reject_guest'),
    (r'^admin/events/email/(?P<event_id>\d+)/$','compsoc.events.admin_views.email_signups'),
    (r'^admin/(.*)', admin.site.root),

    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^password/', 'django.contrib.auth.views.password_change', {'template_name':'password.html','post_change_redirect':'/'}),

    (r'^cms/(?P<url>.*)',handle),

    (r'^search/$', search),

)

# if we are debugging serve the static content locally
# when deployed we use an http server to do this
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),
    )
