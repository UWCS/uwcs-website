import re
from itertools import chain
import urllib2
from xml.dom.minidom import parseString
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from events.models import SteamEvent,SteamEventFeed
from django.core.management.base import NoArgsCommand

p_event_title = re.compile(r'<a class="headlineLink"[^>]+>([^<]+)</a>')
p_event_date = re.compile(r'<div class="eventDateBlock"><span[^>]+>([^<]+)</span>')
p_event_time = re.compile(r'<span class="eventDateTime">([^<]+)</span>')

def event_link(group, id):
    return "http://steamcommunity.com/groups/%s/events/%d" % (group, id)

def feed_link(group, month, year):
    return "http://steamcommunity.com/groups/%s/events?&action=eventFeed&month=%d&year=%d" % (group, month, year)

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Merges events from a steam group"
    requires_model_validation = True

    def handle_noargs(self, **options):
        """
        Should sync SteamEvents on the website and those on the steam community page.
        """
        begin = datetime.now()
        end = begin + relativedelta(months=1)

        for date in begin, end:
            month = date.month
            year = date.year

            for feed in SteamEventFeed.objects.all():
                headers = {'Cookie':'timezoneOffset=3600,0'}
                req = urllib2.Request(feed_link(feed.group_name, month, year), "", headers)
                data = urllib2.urlopen(req).read()
                doc = parseString(data)

                event_items = doc.firstChild.getElementsByTagName("event")
                expired_event_items = doc.firstChild.getElementsByTagName("expiredEvent")

                # completeness - every steam community event should be an active SteamEvent on our website
                # correctness - event info should be kept up to date
                for i,event in enumerate(event_items):
                    event_id = event.attributes.get('eventID').nodeValue
                    event_data = event.firstChild.nodeValue

                    # probably more sensible to have this in one regex
                    event_title = p_event_title.search(event_data).group(1)
                    event_time = p_event_time.search(event_data).group(1)
                    event_date = p_event_date.search(event_data).group(1)

                    event_datetime_string = "%s %s %d %d" % (event_time, event_date, month, year)
                    event_datetime = datetime.strptime(event_datetime_string, "%I:%M%p %A %d %m %Y")

                    # the event description is stored on it's page
                    # this could probably also be done in one or two regexes
                    link = event_link(feed.group_name, int(event_id))
                    data = urllib2.urlopen(link).read()
                    event_doc = parseString(data)

                    body = event_doc.childNodes[1].childNodes[3]
                    divs = body.getElementsByTagName('div')
                    event_content_div = [x for x in divs if x.attributes.has_key('class') and x.attributes['class'].nodeValue == "eventContent"][0]

                    contents = event_content_div.getElementsByTagName('p')[1:]
                    event_details = "\n".join([x.firstChild.nodeValue for x in contents]) + ("\nMore details available \"here\":%s" % link)

                    # now that we have all the data for the event, either create a new one or sync with a currently existing one
                    try:
                        # check for events that have been cancelled on the site but exist in the feed
                        e = SteamEvent.objects.get(steam_id=event_id)
                        print "Syncing events %s from %s" % (e.shortDescription, event_title)
                        e.steam_id=event_id
                        e.type=feed.event_type
                        e.shortDescription=event_title
                        e.longDescription=event_details
                        e.start=event_datetime
                        e.displayFrom=datetime.now()
                        e.finish=event_datetime + timedelta(hours=3)
                        e.location=feed.location
                        e.cancelled=False
                    except SteamEvent.DoesNotExist:
                        print "Adding new event: %s" % event_title
                        e = SteamEvent.objects.create(steam_id=event_id,
                                                      type=feed.event_type,
                                                      shortDescription=event_title,
                                                      longDescription=event_details,
                                                      start=event_datetime,
                                                      displayFrom=datetime.now(),
                                                      finish=event_datetime + timedelta(hours=3),
                                                      location=feed.location,
                                                      )
                    e.save()

                # soundness - every active SteamEvent for this month should 
                #             be an event from this months feed
                this_month_date = datetime(year,month,1)
                next_month_date = this_month_date + relativedelta(months=1)

                for event in SteamEvent.objects.all().filter(start__gte=this_month_date, start__lt=next_month_date, cancelled=False):
                    event_ids = [x.attributes.get('eventID').nodeValue for x in event_items]
                    # should be replaced by some kind of find_if
                    try:
                        index = event_ids.index(str(event.steam_id))
                    except ValueError:
                        # cancel the event
                        print "Event must have been deleted.. cancelling!"
                        event.cancelled = True
                        event.save()

