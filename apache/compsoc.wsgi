import os, sys

# Calculate the path based on the location of the WSGI script.
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 

# Add the path to 3rd party django application and to django itself.
sys.path.append('/home/new-website/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'compsoc.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
