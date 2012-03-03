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


Complete setup on Codd
======================

**Apache**
    We're using Apache and mod_wsgi. WSGI is just a standard for python web applications,
    our Apache config points at ``~/webmaster/reinhardt/compsoc/apache/compsoc.wsgi``. Apache watches
    for changes to compsoc.wsgi and will reload the site if any occur. So after changing any Python code
    you can force the whole website application to reload using just ``touch apache/compsoc.wsgi``.

**Installation directory**
     ``~webmaster/reinhardt/compsoc`` contains a checkout of this repository.

**Periodic syncing with the union database**
    There is a cronjob on codd which runs (as webmaster) ``contrib/update.sh``. This runs ``manage.py
    update`` which syncs the website accounts.

**Periodic subscription of active members to compsoc-announce**
    ``contrib/update.sh`` also runs ``./manage.py add_active_members_to_list
    compsoc-announce``. This ensures all active members are subscribed to
    compsoc-announce. It does mean that anyone we unsubscribe that is still active
    on the website gets re-subscribed, which might be undesirable.

Interaction with Mailman
========================
to document
