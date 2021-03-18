.. contents::

Deprecation
===========

.. warning::
    ⚠️🚨 This is not the current website at uwcs.co.uk🚨⚠️

    There has since been a rewrite - https://github.com/davidjrichardson/uwcs-zarya. Since then there has been a fork https://github.com/UWCS/uwcs-dextre.

Virtualenv
==========
All the 3rd party dependencies for the website are maintained in a file called ``requirements.txt``. It's best to install these into a isolated Python environment, use the following to set this up::

    virtualenv --no-site-packages ~/website-env

To install the dependencies, activate the environment and use ``pip`` to install them::

    source ~/website-env/bin/activate
    pip install -r requirements.txt

The WSGI script that apache uses modifies ``sys.path`` to include the libraries in this virtualenv::

    sys.path.insert(0, '/home/webmaster/website-env/lib/python2.6/site-packages')

Management commands
===================
There are a bunch of utility commands that can be run from the root of the website like so::

    ~/compsoc $ ./manage.py update

``update``
    pulls in members from the union's membership API, and ensures they have an
    account active on the website (creating if necessary). Also expires any website
    accounts for people who are no longer members according to the union, with
    exceptions for guest accounts and people marked as ex-exec.

    .. note:: There's also a 3 week grace period so that members from last year can
       log into the website (e.g. to signup for events)

    .. note:: Requires UNION_API_KEY to be set in settings.py.

``populate``
    Populates the database with fixtures (mostly useful for local testing).

``add_active_members_to_list``
    This 'subscribes' all the accounts currently active on the website to the mailing
    list named, e.g. ``manage.py add_active_members_to_list compsoc-announce`` ensures
    every active user on the website is subscribed to the compsoc-announce entry in
    the django database.

``steam``
    Fetches steam events from all the SteamEventFeeds in the database and creates
    Events for them on our site.

``newsitem``
    This prints out the latest news item - used for the IRCd message of the day.

Interaction with Mailman
========================
The website pushes changes in it's database to mailman (no syncing occurs the other way currently). Mailing lists are modelled in the website database with the ``MailingList`` class, each of which correspond to some Mailman mailing list and have numerous ``User`` objects which correspond to subscriptions to the list. The following describes when these pushes occur:

1. Whenever a ``MailingList`` object gets a subscription or unsubscription, a subscribe/unsubscribe operation is carried out on the Mailman list using the email address stored in the website database.

2. Whenever the details for a website user are changed, the website unsubscribes them with their old address and resubscribes them with their new address. Whenever 


Apache
======

modwsgi
-------
We're using Apache and modwsgi. WSGI is just a standard for web applications written in Python - a valid WSGI application is just a Python file with something called ``application``, which has the right interface. Any Django application can be made into a WSGI app by using something like::

    os.environ['DJANGO_SETTINGS_MODULE'] = 'compsoc.settings'
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

Which just says our application uses Django and sets up an environment variable to say what Django settings file to use for it (this is also exactly what we do). We have a virtualhost hooked up to our WSGI script::

    WSGIDaemonProcess site-1 user=webmaster group=webmaster threads=5
    WSGIProcessGroup site-1
    WSGIScriptAlias / "/home/webmaster/reinhardt/compsoc/apache/compsoc.wsgi"

Apache watches for changes to compsoc.wsgi and will reload the site if any occur. So after changing any Python code
you can force the whole website application to reload using just ``touch apache/compsoc.wsgi``. More information can be found on the `official Django documentation on deploying with modwsgi <https://docs.djangoproject.com/en/1.3/howto/deployment/modwsgi/>`_.

Static content
--------------
To have static content served by Apache, rather than going through the Django app, you can have your virtualhost do some URL matching for requests for static content::

    Alias /static/ "/home/webmaster/reinhardt/compsoc/static/"
    <Directory "/home/webmaster/reinhardt/compsoc/static">
        Order allow,deny
        Options Indexes
        Allow from all
        IndexOptions FancyIndexing
    </Directory>

Django admin static content
---------------------------
The same goes for serving static content (stylesheets, images, scripts) for the Django admin interface::

    Alias /media/ "/usr/share/pyshared/django/contrib/admin/media/"
    <Directory "/usr/share/pyshared/django/contrib/admin/media/">
        Order allow,deny
        Options Indexes FollowSymLinks
        Allow from all
        IndexOptions FancyIndexing
    </Directory>

Currently this is served up from the system installed Django, we should actually move this to being served from Django installed in a virtualenv.

CMS Attachments
---------------
In order to have files attached to CMS pages served up by Apache, you can use the following rule::

    AliasMatch ^(/cms/.*/attachment/[^/]+)$ /home/webmaster/reinhardt/compsoc/static$1

Cronjobs that we use
====================

Syncing with the union database
-------------------------------
There is a cronjob on codd which runs (as webmaster) ``contrib/update.sh``. This runs ``manage.py
update`` which syncs the website accounts with members according the union's database.

Subscription of active members to compsoc-announce
--------------------------------------------------
``contrib/update.sh`` also runs ``./manage.py add_active_members_to_list
compsoc-announce``. This ensures all active members have subscriptions to
compsoc-announce (in the django-database, which pushes changes to mailman).
It does mean that anyone we unsubscribe that is still active on the website
will later be re-subscribed, which might be undesirable.


Deployment on Codd
==================

Install fabric
--------------
Install into your virtualenv using pip::

    ~/reinhardt/compsoc $ pip install fabric

Setup ssh-key based access
--------------------------
Add a line to ``~webmaster/.ssh/authorized_keys`` on codd with your public key.

Fabric commands
---------------
The included fabfile has a ``deploy`` command that updates the website over
ssh, pulls down dependencies and does syncdb::

    ~/reinhardt/compsoc $ fab deploy --hosts webmaster@uwcs.co.uk

Database Configuration
======================
To document

Testing
=======

Functional Tests
----------------
Trying out lettuce for writing high level tests for the website. To run them,
just use the included ``lettuce_tests.sh`` script::

    ./lettuce_tests.sh

All the functional tests are stored in a ``features`` folder per app::

    compsoc/
        events/
            features/
                index.feature
                index-steps.py
        memberinfo/
            features/
                index.feature
                index-steps.py

Unit Tests
----------
Any unit tests are executed using the ``test`` management command::

    python manage.py test

Error Reporting
===============
If any 500 errors occur in the website, any ADMINS (specified in settings.py)
are notified of it by email with information about the problem. See https://docs.djangoproject.com/en/dev/howto/error-reporting/.
