from django.db import models
from django.contrib.auth.models import User
from math import log
from django.db.models.signals import post_delete

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

TOURNAMENT_TYPES = (
    ('S','Single Elimination Cup'),
    ('LE','League'),
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
        return not bool(self.match_set.filter(round=log(self.tree_size(),2)))

    def in_play(self):
        return self.allocation_set.exclude(losses__tournament=self)

    def is_not_full(self):
        return self.allocation_set.count() <= 32
   
    def is_elim_cup(self):
        return self.type == 'S'

    def __unicode__(self):
        return self.name

class Allocation(models.Model):
    '''
    A user is allocated a position within a tournament
    '''
    tournament = models.ForeignKey(Tournament)
    index = models.IntegerField()
    user = models.ManyToManyField(User)

#    class Meta:
#        unique_together = (('tournament','user'),)

    def user_str(self):
        return reduce(lambda acc,u: acc+" "+u.member.name(),self.user.all(),"")

    def __unicode__(self):
        return self.user_str() + u' in ' + self.tournament.__unicode__()

    def partner_index(self):
        return self.index - 1 if self.index % 2 == 0 else self.index + 1

    def win(self):
        '''
        Creates the match object when this Player has won
        '''
        try:
            # if you've already won a game
            round = self.wins.latest('round').round + 1
            mid,up = pow(2,round-1)+1,pow(2,round)+1
            opponent = self.tournament.in_play().get(index__in=range(mid,up) if self.index < mid else range(1,mid))
            self.wins.create(round=round,looser=opponent,tournament=self.tournament)
        except Match.DoesNotExist:
            try:
                other = self.tournament.allocation_set.get(index=self.partner_index())
            except:
                other = None
            # first game
            self.wins.create(
                round=1,
                looser=other,
                tournament=self.tournament,
            )

def del_handler(sender, instance, **kwargs):
    for alloc in instance.tournament.allocation_set.filter(index__gt=instance.index).order_by('index'):
        alloc.index -= 1
        alloc.save()

post_delete.connect(del_handler,sender=Allocation)

class Match(models.Model):
    tournament = models.ForeignKey(Tournament)
    round = models.IntegerField()
    winner = models.ForeignKey(Allocation, related_name="wins")
    looser = models.ForeignKey(Allocation, related_name="losses", blank=True, null=True)

    def __unicode__(self):
        return "%s beat %s in %i" % (self.winner,self.looser,self.round)


