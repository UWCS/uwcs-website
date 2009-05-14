from django.db import models
from django.contrib.auth.models import User
from compsoc.tracker.signals import *

class Goal(models.Model):
    name = models.CharField(max_length=20,unique=True)
    supervisor = models.ForeignKey(User)
    description = models.TextField()
    completed = models.BooleanField()

    def __unicode__(self):
        return self.name

class TicketManager(models.Manager):
    def by_completed(self,choice):
        if choice == 'A':
            return self.all()
        else:
            return self.filter(completed=(choice == 'C'))

class Ticket(models.Model):
    '''
    Represents an atomic unit of work within the tracker.
    '''
    title = models.CharField(max_length=60)
    started = models.DateTimeField()
    due_date = models.DateTimeField(blank=True,null=True)
    description = models.TextField()
    submitter = models.ForeignKey(User,related_name='submitted')
    assignee = models.ForeignKey(User,blank=True,null=True,related_name='assigned')
    goal = models.ForeignKey(Goal)
    completed = models.BooleanField()

    objects = TicketManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/tickets/detail/%i/" % self.id

#pre_save.connect(goal_email, sender=Goal)
#pre_save.connect(ticket_email, sender=Goal)
