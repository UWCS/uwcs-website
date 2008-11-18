from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    name = models.CharField(max_length=20)
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
    name = models.CharField(max_length=20)
    started = models.DateTimeField()
    due_date = models.DateTimeField(blank=True,null=True)
    description = models.TextField()
    submitter = models.ForeignKey(User,related_name='submitted')
    assignee = models.ForeignKey(User,blank=True,null=True,related_name='assigned')
    goal = models.ForeignKey(Goal)
    completed = models.BooleanField()

    objects = TicketManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/tickets/detail/%i/" % self.id
