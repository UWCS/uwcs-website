from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta,datetime
from compsoc import config

TARGETS = (
    ('ACA', 'Academic'),
    ('GAM', 'Gaming'),
    ('SCL', 'Social'),
    ('SCT', 'Society'),
)

class EventType(models.Model):
    name = models.CharField(max_length=20)
    info = models.TextField()
    target = models.CharField(max_length=3, choices=TARGETS)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    type = models.ForeignKey(EventType)
    shortDescription = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    longDescription = models.TextField()
    signupsRequired = models.BooleanField()
    start = models.DateTimeField()
    finish = models.DateTimeField()
    displayFrom = models.DateTimeField()

    def days(self):
        days = []
        i = self.start.date()
        end = self.finish.date()
        day = timedelta(days=1)
        while i <= end:
            days.append(i)
            i += day
        return days

    def time_string(self):
        return self.start.strftime(config.DATE_FORMAT_STRING)+" - "+self.finish.strftime(config.DATE_FORMAT_STRING)

    def __unicode__(self):
        return self.type.name + " @ " + self.time_string()

    def is_in_future(self):
        return datetime.now() < self.start

    def has_signups(self):
        try:
            self.eventsignup
            return True
        except EventSignup.DoesNotExist:
            return False
    
    def signup_total(self):
        return self.eventsignup.signupsLimit

    def signup_tally(self):
        return self.signup_set.count
    
# Signup Options seperated from Event to normalise and avoid nullable.
class EventSignup(models.Model):
    event = models.OneToOneField(Event)
    signupsLimit = models.IntegerField()
    open = models.DateTimeField()
    close = models.DateTimeField()
    fresher_open = models.DateTimeField()
    guest_open = models.DateTimeField()

    def __unicode__(self):
        return self.event.__unicode__()

class Signup(models.Model):
    event = models.ForeignKey(Event)
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    comment = models.TextField()

    class Meta:
        ordering = ["time"]

    def __unicode__(self):
        return self.user.username

    def time_form(self):
        return self.time.strftime(config.DATE_FORMAT_STRING)

class Seating(models.Model):
    '''Information about a seat at a revision'''
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    revision = models.IntegerField()
    col = models.IntegerField()
    row = models.IntegerField()
    #dirty = models.BooleanField()
    
class SeatingRevision(models.Model):
    '''Information about a single seating plan revision'''
    event = models.ForeignKey(Event)
    creator = models.ForeignKey(User)
    revision = models.IntegerField()
    comment = models.CharField(max_length=30)

