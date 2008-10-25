from django.db import models

from compsoc.search import register

COMMS_TYPE = (
    ('NL','Newsletter'),
    ('M','Minute'),
    ('N','News'),
)

class Communication(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    text = models.TextField()
    type = models.CharField(max_length=2,choices=COMMS_TYPE)

    def __unicode__(self):
        return self.title

register(Communication, ['title'])
