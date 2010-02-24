import xml.dom.minidom
from xml.dom.minidom import Node
from urllib import urlopen
import settings
from django.core.management.base import NoArgsCommand
from settings import UNION_API_KEY,EX_EXEC_GROUP_NAME
from django.contrib.auth.models import User,Group
from compsoc.memberinfo.models import *
from compsoc.shortcuts import *
from events.models import Event

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
        if prop[3].firstChild:
            email = get(prop[3])
        else:
            email = None
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

        #2. soundness: if your account is not a guest account and is active then you must be a union member
        # a) sync active members info
        # b) deactivate non union members
        #for user in User.objects.exclude(member__guest=True):
        y = current_year()
        for user in User.objects.filter(is_active=True, member__guest=False):
            if union_lookup.has_key(user.username):
                (first,last,email) = union_lookup[user.username]

                # sync information
                user.first_name = first
                user.last_name = last
                if email is not None:
                    user.email = email
                else:
                    user.email = ""
                    user.is_active = False
                user.save()

                # note that they have joined this year
                MemberJoin.objects.get_or_create(user=user,year=y)

                del union_lookup[user.username]
            # if they're not listed in the union's api, could be a special case
            elif not user.is_staff:
                # next two lines should be removed when historical exec data is added
                ex, created = Group.objects.get_or_create(name=EX_EXEC_GROUP_NAME)

                # if not on the exec at some point
                if not user.groups.filter(name=EX_EXEC_GROUP_NAME):
                    try:
                        week = warwick_week_for(datetime.now())
                    except Term.DoesNotExist:
                        week = settings.GRACE_PERIOD + 1 #assume outside of grace period

                    # if inside the grace period 
                    if week <= settings.GRACE_PERIOD:
                        # but not a member from last year
                        if not user.memberjoin_set.filter(year=current_year()-1):
                            user.is_active = False
                            user.save()
                    else:
                        user.is_active = False
                        user.save()

        #3. completeness: if you are a union member, then you must have a compsoc account
        #                 it is active iff you have a union email address
        #4. TODO: information: emails people who have just had their accounts added
        #5. consistency: ensure there exist current join years for members
        # a) create new accounts for those without
        # b) reactivate accounts for those already with inactive accounts
        for (id,(first,last,email)) in union_lookup.iteritems():

            active = True

            try:
                # find disabled accounts
                user = User.objects.get(username=id)
                print "reactivating %s" % id
                if email is None:
                    email = ""
                    active = False
                    print "cannot reactivate %s: no email address" % id
            except User.DoesNotExist:
                print "creating %s" % id
                if email is None:
                    email = ""
                    active = False
                    print "cannot activate %s: no email address" % id
                password = User.objects.make_random_password()
                user = User.objects.create_user(id,email,password)
                user.first_name = first
                user.last_name = last
                user.memberjoin_set.create(year=y)
                if not settings.DEBUG:
                    if user.email != "":
                        template_mail(
                            'Welcome to Compsoc',
                            'memberinfo/new_user_email',
                            {'first': user.first_name, 'last':user.last_name, 'username':user.username, 'password':password, 'events':Event.objects.in_future()[:5]},
                            settings.WEBMASTER_EMAIL,
                            [user.email])

            #sync info
            user.first_name = first
            user.last_name = last 
            user.is_active = active

            user.save()
            MemberJoin.objects.get_or_create(user=user,year=y)
