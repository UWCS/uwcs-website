from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

TOURNAMENT_TYPES = (
    ('S','Single Elimination Cup'),
)

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=1, choices=TOURNAMENT_TYPES)
    game = models.ForeignKey(Game)
    started = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Allocation(models.Model):
    tournament = models.ForeignKey(Tournament)
    index = models.IntegerField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.member.name() + " in " + self.tournament

class Match(models.Model):
    tournament = models.ForeignKey(Tournament)
    round = models.IntegerField()
    winner = models.ForeignKey(Allocation, related_name="wins")
    looser = models.ForeignKey(Allocation, related_name="losses")

    def __unicode__(self):
        return "%s beat %s in %i" % (self.winner,self.looser,self.round)


