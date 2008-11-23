'''
Emails for notifying people are all sent via signals
'''

from django.db.models.signals import pre_save
from compsoc.tracker.models import *  
from compsoc.settings import COMPSOC_EXEC_EMAIL
from compsoc.shortcuts import template_mail,pair_map

def diff(new,old,attr):
    nattr = getattr(new,attr)
    return nattr if nattr != getattr(old,attr) else False

def goal_email(sender, **kwargs):
    '''
    Emails supervisor of goal on any changes
    '''
    p = Goal.objects.get(pk=sender.id)
    email = diff(send,p,'supervisor')
    if email:
        template_mail(
            'Goal Ownership Changed',
            'tracker/goal_owner_email',
            {'from':sender.supervisor,'to':p.supervisor,'name':sender.name},
            COMPSOC_EXEC_EMAIL,
            [sender.supervisor.email,p.supervisor.email],
        )
    else:
        template_mail(
            'Goal Changed',
            'tracker/goal_change_email',
            {'attr':dict_map(lambda x:diff(sender,p,x),p.__dict__.keys()),'name':sender.name},
            COMPSOC_EXEC_EMAIL,
            [sender.supervisor.email],
        )

def ticket_email(sender, **kwargs):
    '''
    Emails appropriate people on ticket changes
    '''
    p = Ticket.objects.get(pk=sender.id)
    email_to = set()
    for ticket in [sender,p]:
        if ticket.assignee:
            email_to.add(ticket.assignee.email)
        email_to.add(ticket.submitter.email)
        email_to.add(ticket.goal.supervisor.email)
    template_mail(
        'Ticket Changed',
        'tracker/ticket_change_email',
        {'attr':dict_map(lambda x: diff(sender,p,x),p.__dict__.keys())},
        COMPSOC_EXEC_EMAIL,
        [x for x in email_to],
    )


