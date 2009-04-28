from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from compsoc.shortcuts import template_mail
from compsoc.settings import COMPSOC_TECHTEAM_EMAIL

class Command(BaseCommand):
    help = "emails password change to user"
    requires_model_validation = True

    def handle(self, *args, **options):
        '''
        '''
        for u in User.objects.all():
            password = User.objects.make_random_password()
	    u.set_password(password)
	    u.save()
            try:
	        template_mail(
	            'New Website Password',
		    'memberinfo/migration_email',
                    {'first': u.first_name, 'last':u.last_name, 'username':u.username, 'password':password},
	            COMPSOC_TECHTEAM_EMAIL,
	            [u.email])
            except Exception, e:
                print u.username
                print e
                

    def usage(self, subcommand): pass
