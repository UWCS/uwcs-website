import new
from functools import partial

from django.conf.urls.defaults import *
from django.contrib.auth.models import User

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from uwcs.website.rest import *
from uwcs.website.cms.views import handle,list,games,attachments
from uwcs.website.search.views import search

from uwcs.website.memberinfo.models import ShellAccount,DatabaseAccount,Quota
from feeds import *

#import user_overrides
import settings

# inject extra context into the index method (WHY DOES IT HAVE THIS ARGUMENT IF IT DOESN'T LET YOU USE IT!?)
def create_index(index):
    def index_with_extra_context(*args, **kwargs):
        extra_context = {
            'guest_request_count':User.objects.filter(is_active=False,member__guest=True).count(),
            'shell_request_count':ShellAccount.objects.filter(status='RE').count(),
            'database_request_count':DatabaseAccount.objects.filter(status='RE').count(),
            'quota_request_count':Quota.objects.filter(status='RE').count(),
        }
        kwargs['extra_context'] = extra_context
        return index(*args, **kwargs)

    return index_with_extra_context

admin.site.index = create_index(admin.site.index)

# See feeds.py for details
feeds = {
    'news': LatestNews,
    'news/atom': LatestAtomNews,
    'events': NextEvents,
    'events/atom': NextAtomEvents,
    'signups': LatestSignups,
    'seating': LatestSeatingRevisions,
    'minutes': LatestMinutes,
    'minutes/atom': LatestAtomMinutes,
    'newsletters': LatestNewsletters,
    'newsletters/atom': LatestNewsletters,
    'tickets': LatestTicketChanges,
    'pagerevisions': LatestPageRevisions,
}

def throw_wrapper_because_lambdas_suck_ass():
    raise Exception("this is just here for testing the 500 page")

urlpatterns = patterns('',
    (r'^', include('uwcs.website.comms.urls')),
    (r'^elections/', include('elections.urls')),
    (r'^oops/', throw_wrapper_because_lambdas_suck_ass),
    (r'^member/', include('uwcs.website.memberinfo.urls')),
    (r'^events/', include('uwcs.website.events.urls')),
    (r'^tournaments/', include('uwcs.website.tournaments.urls')),
    #(r'^irc/', include('uwcs.website.choob.urls')),
    (r'^tickets/', include('uwcs.website.tracker.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^admin/cms/page/(?P<page_id>\d+)/$','uwcs.website.cms.admin_views.add_edit'),
    (r'^admin/cms/pagerevision/(?P<rev_id>\d+)/$','uwcs.website.cms.admin_views.revision'),
    (r'^admin/cms/page/add/$','uwcs.website.cms.admin_views.add_edit'),
    (r'^admin/cms/page/move/(?P<page_id>\d+)/$', 'uwcs.website.cms.admin_views.move'),
    (r'^admin/memberinfo/guests/$','uwcs.website.memberinfo.admin_views.guest_list'),
    (r'^admin/memberinfo/accounts/$','uwcs.website.memberinfo.admin_views.account_list'),
    (r'^admin/memberinfo/acceptguest/(?P<user_id>\d+)/$','uwcs.website.memberinfo.admin_views.accept_guest'),
    (r'^admin/memberinfo/rejectguest/(?P<user_id>\d+)/$','uwcs.website.memberinfo.admin_views.reject_guest'),
    (r'^admin/events/email/(?P<event_id>\d+)/$','uwcs.website.events.admin_views.email_signups'),
    (r'^admin/events/location/unify/(?P<location_id>\d+)/$','uwcs.website.events.admin_views.unify'),
    (r'^admin/(.*)', admin.site.root),

# django stuff for authentication
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^password/', 'django.contrib.auth.views.password_change', {'template_name':'password.html','post_change_redirect':'/'}),
# doesn't work for no reason
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^password_reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

    (r'^info_map/$',list),
    (r'^game_servers/$',games),
    (r'^search/$', search),

    #XML REST API
    url(r'^xml/user/(\d+)/$', xml_user),
    url(r'^xml/game/(.*?)/?$', xml_games),
    (r'^tinymce/', include('tinymce.urls')),
)

# Some legacy link compatibility. I hope this doesn't break anything

if settings.LEGACY_SITE:
    urlpatterns += patterns('',
    	(r'^society/events/', include('uwcs.website.events.urls')),
    	(r'^society/members/website', include('uwcs.website.memberinfo.urls')),
    	(r'^auth/logout', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    )
    urlpatterns += patterns('django.views.generic.simple',
        ('^services/codd/tos/?$', 'redirect_to', {'url': '/cms/about/services/codd/tos/'}),
        ('^society/events/rss2.0/$', 'redirect_to', {'url': '/feeds/events/'}),
        ('^society/news/rss2.0/$', 'redirect_to', {'url': '/feeds/news/'}),
        ('^society/minutes/rss2.0/$', 'redirect_to', {'url': '/feeds/minutes/'}),
        ('^society/events/ical/$', 'redirect_to', {'url': '/events/ical/'}),
        ('^society/contact/$', 'redirect_to', {'url': '/cms/contact/'}),
        ('^society/exec/$', 'redirect_to', {'url': '/cms/contact/'}),
        ('^society/newsletters/$', 'redirect_to', {'url': '/newsletters/1/'}),
        ('^society/minutes/$', 'redirect_to', {'url': '/minutes/1/'}),
        ('^society/news/$', 'redirect_to', {'url': '/news/1/'}),
        ('^society/members/$', 'redirect_to', {'url':'/member'}),
        ('^society/members/list/$', 'redirect_to', {'url': '/member/list/'}),
        ('^society/$', 'redirect_to', {'url': '/cms/about/'}),
        ('^gaming/$', 'redirect_to', {'url': '/cms/about/gaming/'}),
        ('^gaming/(?P<id>\d+)/$', 'redirect_to', {'url': '/cms/about/gaming/%(id)s/'}),
        ('^gaming/lans/(?P<id>\d+)/$', 'redirect_to', {'url': '/cms/about/gaming/lans/%(id)s/'}),
        ('^academic/$', 'redirect_to', {'url': '/cms/about/academic/'}),
        ('^academic/(?P<id>\d+)/$', 'redirect_to', {'url': '/cms/about/academic/%(id)s/'}),
        ('^socials/$', 'redirect_to', {'url': '/cms/about/socials/'}),
        ('^socials/(?P<id>\d+)/$', 'redirect_to', {'url': '/cms/about/socials/%(id)s/'}),
        ('^services/$', 'redirect_to', {'url': '/cms/about/services/'}),
        ('^services/(?P<id>\d+)/$', 'redirect_to', {'url': '/cms/about/services/%(id)s/'}),
    )   

# if we are debugging serve the static content locally
# when deployed we use an http server to do this
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),
        (r'^(?P<path>cms/.*/attachment/[^/]+)/$', 'django.views.static.serve', { 'document_root':settings.MEDIA_ROOT } ),
        (r'^ajax/lvsch/$','django.views.generic.simple.redirect_to',{'url':'http://search.warwick.ac.uk/'}),
        (r'^sitebuilder2$','django.views.generic.simple.redirect_to',{'url':'http://www2.warwick.ac.uk/sitebuilder2/'}),
    )

# this goes afterwards to make sure it doesn't catch urls of the form cms/.*/attachment/foo$  this currently has problems with cms/.*/attachment/crap/attachment/foo
urlpatterns += patterns('',
    (r'^cms/(?P<url>.*)/attachment/$', attachments),
    (r'^cms/(?P<url>.*)/$',handle),
)
