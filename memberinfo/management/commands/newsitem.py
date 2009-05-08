import settings
from django.core.management.base import NoArgsCommand
from compsoc.comms.models import *
from textwrap import fill
from django.utils.encoding import smart_str, force_unicode
from textile import textile

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Prints the latest news item so it can be used in MotD"
    requires_model_validation = True

    def handle_noargs(self, **options):
        '''
        '''
        # latest newsitem
        item = Communication.objects.filter(type='N')[0]

        # textile
        split = ''.zfill(80).replace('0','-')
        
        print u' '+item.date.strftime(settings.DATE_FORMAT_STRING)+u'        '+item.title
        print split
        text = force_unicode(textile(smart_str(item.text), encoding='utf-8', output='utf-8'))
        print u'\n'.join(map(lambda x: fill(x,79),item.text.splitlines()))
        print split
