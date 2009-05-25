from django.db import models

from compsoc.search import register
from compsoc.settings import DATE_FORMAT_STRING
from time import strftime

COMMS_TYPE = (
    ('NL','Newsletter'),
    ('M','Minute'),
    ('N','News Item'),
)

def lookup(item_type):
    data = Communication.objects.filter(type=item_type).order_by('-date')
    store = {}
    for comm in data:
        store[(comm.date.year,comm.date.month)] = True
    return map(lambda (y,m): (y,strftime("%b",(0,m,0,0,0,0,0,0,0))),sorted(store.keys(),reverse=True))

class Communication(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    text = models.TextField()
    type = models.CharField(max_length=2,choices=COMMS_TYPE)

    def get_absolute_url(self):
        return "/details/%d" % (self.id,)

    def __unicode__(self):
        return self.title

    def successors(self):
        return Communication.objects.filter(date__gte=self.date).filter(type=self.type).exclude(pk=self.id)
    
    def predecessors(self):
        return Communication.objects.filter(date__lte=self.date).filter(type=self.type).exclude(pk=self.id)

    def has_next_item(self):
        return bool(self.successors())

    def has_prev_item(self):
        return bool(self.predecessors())

    def next_item(self):
        # earliest successor
        return self.successors().order_by('date')[0]

    def prev_item(self):
        return self.predecessors().latest('date')
    
    def last_change_time(self):
        from django.contrib.admin.models import LogEntry,ContentType
        try:
            cct = ContentType.objects.get(name='communication')
            return LogEntry.objects.filter(object_id=self.pk,content_type=cct).latest('action_time').action_time.strftime(DATE_FORMAT_STRING)
        except:
            return 0

register(Communication, ['title'])
