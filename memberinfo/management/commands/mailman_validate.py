from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Validates that the data within the website database is the same as the mailman database"
    requires_model_validation = True

    def handle_noargs(self, **options):
        '''
            see compsoc.memberinfo.mailman.validate_lists
        '''

        print "Validating Mailman lists ..."
        try:
            from compsoc.memberinfo.mailman import validate_lists
            validate_lists()
        except ImportError:
            print "You don't appear to have mailman installed"
        except IOError:
            print "Insufficient priviledges to run this command"

