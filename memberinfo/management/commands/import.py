import xml.dom.minidom
from xml.dom.minidom import Node
from urllib import urlopen
import settings
from django.core.management.base import NoArgsCommand
from settings import UNION_API_KEY
from django.contrib.auth.models import User
from compsoc.memberinfo.models import *
from compsoc.comms.models import *
from os import listdir
from datetime import datetime
import MySQLdb
import sys

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Imports old database information"
    requires_model_validation = True

    MINUTES_DIR = "/home/webmaster/UWCS/root/cps/society/minutes"

    def handle_noargs(self, **options):
        '''
        Import database information from old website to new one
        '''
        conn = MySQLdb.connect (host = "localhost", user = "webmaster", passwd = "Faeng1go", db = "uwcs", use_unicode=1)
        cursor = conn.cursor ()

        # News Items
        cursor.execute ("select date,title,text from newsitems")
        for (date,title,text) in cursor.fetchall():
            Communication.objects.create(date=date,title=title,text=text,type='N')

        # Minutes
        for name in listdir(self.MINUTES_DIR):
            try:
                file = open(self.MINUTES_DIR+"/"+name,"r")
                minutes = unicode(file.read(),'latin-1')
                when = datetime.strptime(name.split('.')[0],"%Y%m%d").date()
                title = "\n".join(minutes.split("\n")[:2])
                minutes = "\n".join(minutes.split("\n")[2:])
                Communication.objects.create(date=when,title=title,text=minutes,type='M')
            except IOError, e:
                if e.errno != 21:
                    print file
                    print e
            finally:
                file.close()
        
        # Import Users
        cursor.execute("select uni_code,first_name,surname,email from members where not (uni_code is null or uni_code = 0) and (suspended = 0)")
        used_codes = set()
        for (uni_code,first_name,surname,email) in cursor.fetchall():
            if len(str(uni_code)) >= 6:
                if uni_code in used_codes:
                    print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code for %s %s " % (uni_code,first_name,surname)
                else:
                    used_codes.add(uni_code)
                    User.objects.create(username=uni_code,first_name=first_name,last_name=surname,email=email,is_staff=False,is_superuser=False)
            else:
                print "Unknown or invalid university code for: %s %s - perhaps they are a guest?" % (first_name,surname)

        #Import nicknames
        cursor.execute("select uni_code,nickname from members where guest = 0 and not (nickname is NULL or uni_code is NULL)")
        used_codes = set()
        for (uni_code,nickname) in cursor.fetchall():
            if uni_code in used_codes:
                print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code for %s " % (uni_code,nickname)
            else:
                try:
                    u = User.objects.get(username=uni_code)
                    used_codes.add(uni_code)
                    NicknameDetails.objects.create(user=u,nickname=nickname)
                except User.DoesNotExist:
                    print "%i, %s has a nickname, but no user entry - maybe a guest?" % (uni_code,nickname)

        cursor.execute('select uni_code,website_url,website_title from members where not (uni_code is null or uni_code = 0 or website_url is null or website_title is null or website_url = "" or guest = 1);')
        used_codes = set()
        for (uni_code,website_url,website_title) in cursor.fetchall():
            if uni_code in used_codes:
                print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code for %s %s" % (uni_code,website_url,website_title)
            else:
                try:
                    u = User.objects.get(username=uni_code)
                    used_codes.add(uni_code)
                    WebsiteDetails.objects.create(user=u,websiteUrl=website_url,websiteTitle=website_title)
                except User.DoesNotExist:
                    print "%i - no user entry - maybe a guest?" % (uni_code)

        cursor.execute('select uni_code,join_year from memberjoin,members where id = member_id')
        used_codes = set()
        for (uni_code,join_year) in cursor.fetchall():
            if (uni_code,join_year) in used_codes:
                print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code" % uni_code
            else:
                try:
                    u = User.objects.get(username=uni_code)
                    used_codes.add((uni_code,join_year))
                    MemberJoin.objects.create(user=u,year=join_year)
                except User.DoesNotExist:
                    print "%s - no user entry - maybe a guest?" % str(uni_code)
        
        cursor.execute("select uni_code,data,status from members,services where member_id = id and service = 'TOVACCT' and (status = 'PRESENT' or status = 'NO_TOS')")
        used_codes = set()
        for (uni_code,data,status) in cursor.fetchall():
            if not uni_code:
                print "Whose Shell account is: %s?" % data
            elif uni_code in used_codes:
                print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code" % uni_code
            else:
                try:
                    u = User.objects.get(username=uni_code)
                    used_codes.add(uni_code)
                    if status == 'PRESENT':
                        s = 'DD'
                    elif status == 'NO_TOS':
                        s = 'PR'
                    else:
                        continue
                    ShellAccount.objects.create(user=u,name=data,status=s)
                except User.DoesNotExist:
                    print "%i - no user entry - maybe a guest?" % (uni_code)

        cursor.execute("select uni_code,data from members,services where member_id = id and service = 'MYSQL'")
        used_codes = set()
        for (uni_code,data) in cursor.fetchall():
            if not uni_code:
                print "Whose Database account is: %s?" % data
            elif uni_code in used_codes:
                print "THIS DATABASE IS EPIC FAIL %i is a duplicate university code" % uni_code
            else:
                try:
                    u = User.objects.get(username=uni_code)
                    used_codes.add(uni_code)
                    DatabaseAccount.objects.create(user=u,name=data,status='PR')
                except User.DoesNotExist:
                    print "%i - no user entry - maybe a guest?" % (uni_code)



        cursor.close()
        conn.close()
