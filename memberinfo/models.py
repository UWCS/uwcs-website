from django.db import models
from django.contrib.auth.models import User
from compsoc.config import *
from compsoc.shortcuts import *

# All information about a member, that isn't stored by auth...User, and isn't optional
class Member(models.Model):
    user = models.OneToOneField(User)
    showDetails = models.BooleanField()
    guest = models.BooleanField()

    def is_fresher(self):
        joins = self.user.memberjoin_set.all()
        if joins.count() == 1:
            return joins[0].year == current_year()
        else:
            return False

    def name(self):
        try:
            return self.user.nicknamedetails.nickname
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
    start_date = models.DateField()
    start_number = models.IntegerField()
    length = models.IntegerField()
    which = models.CharField(max_length=2,choices=TERMS)

    def __unicode__(self):
        return "%s term %i" % (self.get_which_display(), self.start_date.year)

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

    def __unicode__(self):
        return self.name

class DatabaseAccount(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=2,choices=STATUS)
    
    def isPresent(self):
        return self.status == 'PR'
    
    def __unicode__(self):
        return self.name

class Quota(models.Model):
    user = models.ForeignKey(User)
    quantity = models.IntegerField()
    status = models.CharField(max_length=2,choices=QUOTA_STATUS)
    
    def __unicode__(self):
        return str(self.quantity) + " for " + self.user.username + ", currently " + self.status

class MailingList(models.Model):
    users = models.ManyToManyField(User)
    list = models.CharField(max_length=30)

    def __unicode__(self):
        return self.list

