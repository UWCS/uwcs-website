import settings
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from compsoc.memberinfo.models import *
from compsoc.events.models import *
from datetime import date

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Populates some simple data into the database"
    requires_model_validation = True

    def handle_noargs(self, **options):
        '''
        Inserts the following data into the database:
            Terms
            sample member object
            mailing lists
        Assumes:
            syncdb has been run, and there is a user
        '''
        u = User.objects.all()[0]
        try:
            mem = Member(user=u,showDetails=True,guest=False)
            mem.save()
        except: pass #user already has member object 
       
        lists = ['announce','discuss','exec','gaming','jobs','socials','techteam']
        for suffix in lists:
            u.mailinglist_set.create(list='compsoc-'+suffix+'@uwcs.co.uk')

        terms = [
            ('AU',1,date(2008,9,29)),
            ('SP',11,date(2009,1,5)),
            ('SU',21,date(2009,4,20)),
            ('AU',1,date(2007,10,01)),
            ('SP',11,date(2008,1,07)),
            ('SU',21,date(2008,4,21)),
        ]
        for (t,num,d) in terms:
            term = Term(start_date=d,start_number=num,length=10,which=t)
            term.save()

        for yr in range(2001,2009):
            u.memberjoin_set.create(year=yr)

        #is this necessary?
        u.save()
