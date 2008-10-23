from django.db import models

class Page(models.Model):
    slug = models.CharField(max_length=30)
    
    def __unicode__(self):
            return self.slug

    def get_data(self):
        return self.pagerevision_set.latest('date_written')

    def get_peers(self):
        parent_slug = '/'.join(self.slug.split('/')[:-1])
        return Page.objects.filter(slug__startswith=parent_slug)

class PageRevision(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=30)
    text = models.TextField()
    date_written = models.DateField()
    login = models.BooleanField()

    def __unicode__(self):
            return self.title

