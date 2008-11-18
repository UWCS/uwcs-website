from django.conf.urls.defaults import *

urlpatterns = patterns('compsoc.choob.views',
    (r'^$','quotes_page'),
    (r'^all_quotes/(?P<page_num>\d+)/$','all_quotes'),
    (r'^quotes_from/(?P<page>\d+)/$','quotes_from'),
    (r'^quotes_by/(?P<page>\d+)/$','quotes_by'),
    (r'^quotes_with/(?P<page>\d+)/$','quotes_with'),
)

