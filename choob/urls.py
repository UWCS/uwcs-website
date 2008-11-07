from django.conf.urls.defaults import *

urlpatterns = patterns('compsoc.choob.views',
    (r'^$','quotes_page'),
    (r'^all_quotes','all_quotes'),
    (r'^quotes_from','quotes_from'),
    (r'^quotes_by','quotes_by'),
    (r'^quotes_with','quotes_with'),
)

