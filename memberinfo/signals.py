from django.contrib.auth.models import User
from models import MailingList
from django.db.models.signals import post_save,post_delete,m2m_changed,pre_save

def sync_email_with_mailman_database(sender, instance, **kwargs):
    """
    Used to ensure that the mailman database stays faithful to
    the reinhardt one when an email address is updated

    Intended to be triggered pre_save, and act when a user changes
    their email address
    """
    try:
        old_user = User.objects.get(id=instance.id)
    except User.DoesNotExist:
        old_user = instance

    lists = MailingList.objects.filter(users=instance)

    # silently update mailman list subscriptions
    # not sure what to do on mailman throwing an error here yet
    for l in lists:
        try:
            unsubscribe_member(old_user, l)
        except MailmanError: pass
        try:
            subscribe_member(instance, l)
        except MailmanError: pass

def mailing_list_users_changed(sender, instance, action, **kwargs):
    """
    Acts as a callback when the many2many relation
    containing users for this list is updated.

    Attempts to commit to mailman before the
    reinhardt database is updated.
    """
    if action == "pre_add":
        users = User.objects.filter(id__in=kwargs['pk_set'])
        try:
            for user in users:
                subscribe_member(user, instance)
        # XXX: need to move away from wrapping the different types of
        # exception all in MailmanError
        #
        # preferably here we would check if we can commit all of the users
        # to the mailman database before trying to
        #
        # in the next version. :P -- monk
        except MailmanError: pass
    elif action == "pre_remove":
        users = User.objects.filter(id__in=kwargs['pk_set'])
        try:
            for user in users:
                unsubscribe_member(user, instance)
        except MailmanError: pass

pre_save.connect(sync_email_with_mailman_database, sender=User)
m2m_changed.connect(mailing_list_users_changed, sender=MailingList.users.through)
