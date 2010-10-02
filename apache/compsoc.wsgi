import os, sys

CUSTOM_DJANGO_PATH = None

# Calculate the path based on the location of the WSGI script.
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 
sys.path.append(project) 

# wanted to reflect that we probably
# want to use a django install in the website
# users home (this way the webmaster doesn't need
# root to update django)
if CUSTOM_DJANGO_PATH is not None:
    sys.path.insert(0,CUSTOM_DJANGO_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'compsoc.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
