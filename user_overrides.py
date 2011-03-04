# django's built in auth doesn't allow for customization so
# here we do a simple override on the default string representation
# and ordering
from django.contrib.auth.models import User

def full_name_with_user(self):
    return "%s (%s)" % (self.get_full_name(), self.username)

User.__unicode__ = full_name_with_user
User._meta.ordering = ['first_name','last_name']
