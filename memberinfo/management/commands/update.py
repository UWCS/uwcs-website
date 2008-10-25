import xml.dom.minidom
from xml.dom.minidom import Node
from urllib import urlopen
import settings
from django.core.management.base import NoArgsCommand
from settings import UNION_API_KEY
from django.contrib.auth.models import User
from compsoc.memberinfo.models import *

PREFIX = 'http://www.sunion.warwick.ac.uk/portal/membershipapi/listMembers/'
 
def get(node):
    return node.firstChild.nodeValue

def to_camel(unicode):
    return unicode[0].upper()+unicode[1:].lower()

def get_data():
    '''
    Obtains name/id/email for members from the student's union database.
    Relies on their web service
    PRECOND: compsoc.settings.UNION_API_KEY is set
    '''
    content = urlopen(PREFIX+UNION_API_KEY+'/').read()
    doc = xml.dom.minidom.parseString(content)
    lookup = {}
    for node in doc.getElementsByTagName('Member'):
        prop = node.childNodes
        first = to_camel(get(prop[0]))
        last = to_camel(get(prop[1]))
        user = get(prop[2]) if prop[2].firstChild else first+last
        email = get(prop[3])
        lookup[user] = (first,last,email)
    return lookup

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Updates the models from the union database"
    requires_model_validation = True

    def handle_noargs(self, **options):
        '''
        Runs main update for Compsoc membership details.  The update satisfies the
        following conditions:
        1. Internal Consistency of compsoc models
            user.is_active iff there is a join entry for the current year
        2. Equivalence between compsoc and union models
            user.is_active iff the user is a current member of compsoc or a guest
        3. User information
            compsoc members who have just had an account created, should be emailed
        '''
        from compsoc.shortcuts import current_year

        #1. get data from the union
        union_lookup = get_data()

        #2. soundness: if your account is active then you must be a union member
        for user in User.objects.all():
            if user.is_active:
                if union_lookup.has_key(user.username):
                    del union_lookup[user.username]
                else:
                    user.is_active = False

        #3. completeness: if you are a union member, then you must have a compsoc account
        #4. TODO: information: emails people who have just had their accounts added
        #5. consistency: ensure there exist current join years for members
        y = current_year()
        for (id,(first,last,email)) in union_lookup.iteritems():
            password = User.objects.make_random_password()
            user = User.objects.create_user(id,email,password)
            user.first_name = first
            user.last_name = last 
            user.save()
            member = Member(user=user,showDetails=False,guest=False)
            member.save()
            user.memberjoin_set.create(year=y)

