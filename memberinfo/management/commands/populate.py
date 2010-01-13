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
            Sample Event Types
            Sample Locations
            Sample Events
        Assumes:
            syncdb has been run, and there is a user
        '''
        #u = User.objects.all()[0]
        #try:
            #mem = Member(user=u,showDetails=True,guest=False)
            #mem.save()
        #except: pass #user already has member object 

        # sort of broken :p
        #lists = ['announce','discuss','exec','gaming','jobs','socials','techteam']
        #for suffix in lists:
            #u.mailinglist_set.create(list='compsoc-'+suffix+'@uwcs.co.uk')

        terms = [
            # from http://www2.warwick.ac.uk/study/termdates/
            # 2007/2008
            ('AU',1,date(2007,10,01)),
            ('SP',11,date(2008,1,07)),
            ('SU',21,date(2008,4,21)),

            # 2008/2009
            ('AU',1,date(2008,9,29)),
            ('SP',11,date(2009,1,5)),
            ('SU',21,date(2009,4,20)),

            # 2009/2010
            ('AU',1,date(2009,10,5)),
            ('SP',11,date(2010,1,11)),
            ('SU',21,date(2010,4,26)),

            # 2010/2011
            ('AU',1,date(2010,10,4)),
            ('SP',11,date(2011,1,10)),
            ('SU',21,date(2011,4,27)),

            # 2011/2012
            ('AU',1,date(2011,10,3)),
            ('SP',11,date(2012,1,9)),
            ('SU',21,date(2012,4,23)),

            # 2012/2013
            ('AU',1,date(2012,10,1)),
            ('SP',11,date(2013,1,7)),
            ('SU',21,date(2013,4,22)),

            # 2013/2014
            ('AU',1,date(2013,9,30)),
            ('SP',11,date(2014,1,6)),
            ('SU',21,date(2014,4,23)),
        ]
        for (t,num,d) in terms:
            term = Term(start_date=d,start_number=num,length=10,which=t)
            term.save()

        #for yr in range(2001,2009):
            #u.memberjoin_set.create(year=yr)

        #is this necessary?
        #u.save()

        # Event Types
        event_types = [
            {"name":"LAN Party", "info":"Weekend long sweat off.", "target":"GAM"},
            {"name":"Pub Social", "info":"Pub food with CompSoc.", "target":"SCL"},
            {"name":"Exec Meeting", "info":"Weekly meeting to discuss stuff.", "target":"SCT"},
        ]

        for et in event_types:
            EventType.objects.create(**et)

        # locations
        locations = [
            {"name":"Lib2", "description":"Next to the Cafe Library"},
            {"name":"The Phantom Coach", "description":"Up the road from tescos. Nice pub!"},
            {"name":"DCS Undergrad Labs", "description":"The building next to the Zeeman building."},
        ]

        for l in locations:
            Location.objects.create(**l)
