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

def bound(n):
    return filter(lambda x:x >= n,[pow(2,x) for x in range(0,10)])[0]

class Tournament(models.Model):
    '''
    Currently assumes allocations are only powers of 2
    '''
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=1, choices=TOURNAMENT_TYPES)
    game = models.ForeignKey(Game)
    started = models.DateTimeField(auto_now_add=True)

    def tree_size(self):
        return bound(self.allocation_set.count())

    def is_in_progress(self):
        return not bool(self.match_set.get(round=self.tree_size()))

    def in_play(self):
        return self.allocation_set.exclude(losses__tournament=self)

    def __unicode__(self):
        return self.name

class Allocation(models.Model):
    '''
    A user is allocated a position within a tournament
    '''
    tournament = models.ForeignKey(Tournament)
    index = models.IntegerField()
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (('tournament','user'),)

    def __unicode__(self):
        return self.user.member.name() + u' in ' + self.tournament.__unicode__()

    def win(self):
        '''
        Creates the match object when this Player has won
        '''
        round = self.wins.latest('round').round + 1
        mid,up = pow(2,round-1)+1,pow(2,round)+1
        opponent = self.tournament.in_play().get(index__in=range(mid,up) if self.index < mid else range(1,mid))
        self.wins.create(round=round,looser=opponent,tournament=self.tournament)

class Match(models.Model):
    tournament = models.ForeignKey(Tournament)
    round = models.IntegerField()
    winner = models.ForeignKey(Allocation, related_name="wins")
    looser = models.ForeignKey(Allocation, related_name="losses")

    def __unicode__(self):
        return "%s beat %s in %i" % (self.winner,self.looser,self.round)


