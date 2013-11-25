from django.core.management.base import BaseCommand
from uwcs_website.memberinfo.models import MailingList
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<list_name>'
    help = "Adds all active members to a given list"

    def handle(self, *args, **options):
        """
        Adds all active members to a given list
        """
        if len(args) < 1: raise CommandError("arguments: <list_name>")

        list_name = args[0]
        try:
            list = MailingList.objects.get(list=list_name)
        except MailingList.DoesNotExist:
            raise CommandError("Mailing List %s does not exist in the reinhardt database" % list_name)

        list.users.add(*User.objects.filter(is_active=True).values_list('id',flat=True))
