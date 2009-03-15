# Copyright (C) 1998-2007 by the Free Software Foundation, Inc.
# Much of this is based on /usr/lib/mailman/bin/paths.py and Fixes the path of the project in order to use mailman

# BEGIN MAILMAN PATH INCLUSION ---------------------------

import os
import sys 
from warnings import filterwarnings

# some scripts expect this attribute to be in this module
prefix = '/var/lib/mailman'
exec_prefix = '${prefix}'

# work around a bogus autoconf 2.12 bug
if exec_prefix == '${prefix}':
    exec_prefix = prefix

# Supress Python 2.5 warning about string exceptions.
filterwarnings('ignore', '.* string exception', DeprecationWarning)

# Hack the path to include the parent directory of the $prefix/Mailman package
# directory.
sys.path.insert(0, prefix)

# We also need the pythonlib directory on the path to pick up any overrides of
# standard modules and packages.  Note that these must go at the front of the
# path for this reason.
sys.path.insert(0, os.path.join(prefix, 'pythonlib'))

# Include Python's site-packages directory.
sitedir = os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3],'site-packages')
sys.path.append(sitedir)

# END MAILMAN PATH INCLUSION ---------------------------

from compsoc.memberinfo.models import MailingList
from Mailman import Utils
from Mailman import MailList
from django.contrib.auth.models import User
from Mailman import Errors

def validate_lists():
    '''
        Checks current data in the compsoc database corresponds to that in Mailman.
        Caveat: they have to be subscribed using the same email address they use for the compsoc website.
        This includes:
            Checking all lists in the MailingList model have a mailman equivalent
            Checking all signups to a list are subscribed to the mailman list
    '''
    for list in MailingList.objects.all():
        if not Utils.list_exists(list.list):
            print "%s doesn't exist on mailman" % list.list
        else:
            mailman_list = MailList.MailList(list.list, lock=False)
            members = mailman_list.getMemberCPAddresses(mailman_list.getRegularMemberKeys()+mailman_list.getDigestMemberKeys())
            for user in list.users.all():
                if not user.email in members:
                    print "The website thinks %s is subscribed to %s but he/she isn't" % (user.member.all_name(),list.list)

def import_lists(prefix):
    '''
        Imports lists named with the given prefix from mailman
        into the compsoc website.
        Caveat: they have to be subscribed using the same email
        address they use for the compsoc website.
    '''
    for list_name in Utils.list_names():
        if list_name.startswith(prefix):
            list,new = MailingList.objects.get_or_create(list=list_name)
            mailman_list = MailList.MailList(list_name, lock=False)
            members = mailman_list.getMemberCPAddresses(mailman_list.getRegularMemberKeys()+mailman_list.getDigestMemberKeys())
            for member in members:
                try:
                    list.users.add(User.objects.get(email=member))
                except User.DoesNotExist: pass

class UserDesc:
    def __init__(self,name,address):
        self.name = name
        self.address = address
        self.digest = False

class MailmanError(Exception):
    def __init__(self,msg):
        self.msg = msg

def subscribe_member(user,list):
    '''
        Adds a compsoc member to a mailing list
    '''
    try:
        mailman_list = MailList.MailList(list.list)
        try:
            # 1 = send welcome message
            mailman_list.ApprovedAddMember(UserDesc(user.member.all_name(),user.email), 1, 0)
            mailman_list.Save()
        except Errors.MMAlreadyAMember:
            raise MailmanError('User is already a member')
        except Errors.MembershipIsBanned, pattern:
            raise MailmanError("User's email is banned by pattern %s " % pattern)
        except Errors.MMBadEmailError:
            raise MailmanError("Mailman has rejected the user's email")
        except Errors.MMHostileAddress:
            raise MailmanError('User is considered hostile by mailman')
        finally:
            mailman_list.Unlock()
    except Errors.MMUnknownListError:
        raise MailmanError("This mailman list doesn't exist")

def unsubscribe_member(user,list):
    '''
        Removes a compsoc member from a mailing list
    '''
    try:
        mailman_list = MailList.MailList(list.list)
        try:
            if not mailman_list.isMember(user.email):
                raise MailmanError("User isn't subscribed to the list")
            #last 2 args: is admin notified, is user notified
            mailman_list.ApprovedDeleteMember(user.email, 'bin/remove_members',True,True)
            mailman_list.Save()
        finally:
            mailman_list.Unlock()
    except Errors.MMUnknownListError:
        raise MailmanError("This mailman list doesn't exist")

