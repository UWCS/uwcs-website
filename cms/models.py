from django.db import models

class Page(models.Model):
    slug = models.CharField(max_length=30)
    
    def __unicode__(self):
            return self.slug

class PageRevision(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=30)
    text = models.TextField()
    date_written = models.DateField()
    login = models.BooleanField()

    def __unicode__(self):
            return self.title

