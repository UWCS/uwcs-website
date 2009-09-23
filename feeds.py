from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from compsoc.comms.models import Communication
from compsoc.events.models import Event, Signup, SeatingRevision
from datetime import datetime

class LatestNews(Feed):
    title = "Latest Compsoc news items"
    link = "/"
    description = "All the updates from the University of Warwick Computing Society"

    def items(self):
        return Communication.objects.filter(type='N').order_by('-date')[:10]

    #def item_link(self,item):
        #return "/details/%i/" % item.id

    def item_pubdate(self,item):
        return datetime.fromordinal(item.date.toordinal())

class LatestAtomNews(LatestNews):
    feed_type = Atom1Feed
    subtitle = LatestNews.description

class NextEvents(Feed):
    title = "Next Compsoc Events"
    link = "/events/calendar/"
    description = "Next 10 events from the University of Warwick Computing Society"

    def items(self):
        return filter(lambda e: e.is_now_or_later(),Event.objects.order_by('start').exclude(displayFrom__gte=datetime.now()))[:10]

    def item_link(self,event):
        return "/events/details/%i/" % event.id

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
	return item.start

class NextAtomEvents(NextEvents):
    feed_type = Atom1Feed
    subtitle = NextEvents.description

class LatestMinutes(Feed):
    title = "Compsoc Exec Meeting Minutes"
    link = "/"
    description = "Minutes written by the secretary of the University of Warwick Computing Society"

    def items(self):
        return Communication.objects.filter(type='M').order_by('-date')[:10]

    def item_link(self,item):
        return "/details/%i/" % item.id

    def item_pubdate(self,item):
        return datetime.fromordinal(item.date.toordinal())

class LatestAtomMinutes(LatestMinutes):
    feed_type = Atom1Feed
    subtitle = LatestMinutes.description

class LatestNewsletters(Feed):
    title = "Compsoc Exec Meeting Newsletters"
    link = "/"
    description = "Newsletters written by the University of Warwick Computing Society Exec"

    def items(self):
        return Communication.objects.filter(type='N').order_by('-date')[:10]

    def item_link(self,item):
        return "/details/%i/" % item.id

    def item_pubdate(self,item):
        return datetime.fromordinal(item.date.toordinal())

class LatestAtomNewsletters(LatestNewsletters):
    feed_type = Atom1Feed
    subtitle = LatestNewsletters.description

class LatestSignups(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Event.objects.get(id=bits[0])

    def title(self, obj):
        return "Recent signups for event %s" % obj

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        return Signup.objects.filter(event=obj).order_by('-time')[:10]

    def item_link(self, item):
        return item.event.get_absolute_url()

class LatestSeatingRevisions(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return SeatingRevision.objects.get(id=bits[0])

    def title(self, obj):
        return "Latest seating revisions for %s" % obj.event

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.event.get_absolute_url()

    def items(self, obj):
        return SeatingRevision.objects.filter(event=obj.event).order_by('-id')[:10]
