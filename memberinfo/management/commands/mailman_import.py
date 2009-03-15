from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Updates the models from the union database"
    requires_model_validation = True

    def handle_noargs(self, **options):
        '''
        '''

        print "importing from the mailman lists with the prefix 'compsoc'"

        try:
            from compsoc.memberinfo.mailman import import_lists
            import_lists('compsoc')
        except ImportError:
            print "You don't appear to have mailman installed"
        except IOError:
            print "Insufficient priviledges to check list membership"
