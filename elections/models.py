from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Election(models.Model):
    date = models.DateTimeField()
    close_date = models.DateTimeField()

    def __unicode__(self):
        return "Elections for %s" % self.date.year

class Position(models.Model):
    election = models.ForeignKey(Election)
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

#class AbstractCandidate(models.Model):
    #class Meta:
        #abstract = True

#class RealCandidate(AbstractCandidate):
    #user = models.ForeignKey(User)
    #manifesto = models.TextField(blank=True)

#class FakeCandidate(AbstractCandidate):
    #name = models.CharField(max_length=30)

class Candidate(models.Model):
    position = models.ForeignKey(Position)
    user = models.ForeignKey(User)
    manifesto = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.__unicode__()

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate)
    preference = models.IntegerField()
    voter = models.ForeignKey(User)
