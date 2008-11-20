from django.db import models
from django.contrib.auth.models import User
from compsoc.settings import DATE_FORMAT_STRING
from compsoc.shortcuts import *
from datetime import datetime, timedelta

# All information about a member, that isn't stored by auth...User, and isn't optional
class Member(models.Model):
    user = models.OneToOneField(User)
    showDetails = models.BooleanField()
    guest = models.BooleanField()

    def is_fresher(self):
        return self.user.username.startswith("%02d" % (date.today().year-2000))

    def name(self):
        try:
            return self.user.nicknamedetails.nickname
        except NicknameDetails.DoesNotExist:
            return self.user.get_full_name()

    def all_name(self):
        try:
            return self.user.nicknamedetails.nickname+" ("+self.user.get_full_name()+")"
        except NicknameDetails.DoesNotExist:
            return self.user.get_full_name()
    
    def get_nick(self):
        try:
            return self.user.nicknamedetails.nickname
        except NicknameDetails.DoesNotExist:
            return ""

    def __unicode__(self):
        return self.name()

# Optional info about one's website
class WebsiteDetails(models.Model):
    user = models.OneToOneField(User)
    websiteUrl = models.CharField(max_length=50)
    websiteTitle = models.CharField(max_length=50)

class NicknameDetails(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20)

class MemberJoin(models.Model):
    '''Stores history of membership'''
    user = models.ForeignKey(User)
    year = models.IntegerField()

    def __unicode__(self):
        return "%s joined in %i" % (self.user.username,self.year)

TERMS = (
    ('AU','Autumn'),
    ('SP','Spring'),
    ('SU','Summer'),
)

class Term(models.Model):
    '''Stores date information about terms'''
    start_date = models.DateTimeField()
    start_number = models.IntegerField()
    length = models.IntegerField()
    which = models.CharField(max_length=2,choices=TERMS)

    def __unicode__(self):
        return "%s term %i" % (self.get_which_display(), self.start_date.year)

def term_for(date):
    candidate = Term.objects.filter(start_date__lte=(date-timedelta(days=-7))).latest('start_date')
    within = timedelta(days=(candidate.length-1)*7)
    if date < (candidate.start_date + within):
        return candidate
    else:
        raise Term.DoesNotExist

def term_week_for(date):
    term = term_for(date)
    return ((date - term.start_date).days / 7) + 1

def warwick_week_for(date):
    term = term_for(date)
    return ((date - term.start_date).days / 7) + term.start_number + 1

STATUS = (
    ('RE','Requested'),
    ('PR','Present'),
    ('DD','Disabled'),
)

    # The user has stated that he/she/undefined wants quota
    # the user has paid, but the account hasn't been changed
    # the change has been made
QUOTA_STATUS = (
    ('RE','Requested'),
    ('AU','Authorised'),
    ('PR','Present'),
)

class ShellAccount(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=2,choices=STATUS)
    
    def isPresent(self):
        return self.status == 'PR'

    def isDisabled(self):
        return self.status == 'DD'
    
    def __unicode__(self):
        return self.name

class DatabaseAccount(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=2,choices=STATUS)
    
    def isPresent(self):
        return self.status == 'PR'
    
    def isDisabled(self):
        return self.status == 'DD'

    def __unicode__(self):
        return self.name

class Quota(models.Model):
    user = models.ForeignKey(User)
    quantity = models.IntegerField()
    status = models.CharField(max_length=2,choices=QUOTA_STATUS)
    date = models.DateTimeField()
    
    def __unicode__(self):
        return str(self.quantity) + " for " + self.user.username + ", currently " + self.status

class MailingList(models.Model):
    users = models.ManyToManyField(User)
    list = models.CharField(max_length=30)

    def __unicode__(self):
        return self.list

