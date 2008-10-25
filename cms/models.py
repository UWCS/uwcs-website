from django.db import models

class Page(models.Model):
    slug = models.CharField(max_length=30)
    
    def __unicode__(self):
            return self.slug

    def get_data(self):
        return self.pagerevision_set.latest('date_written')

    def get_peers(self):
        parent_slug = '/'.join(self.slug.split('/')[:-1])+'/'
        peers = []
        for p in Page.objects.filter(slug__startswith=parent_slug):
            if not p.slug.startswith(self.slug):
                peers.append(p)
        return peers

    def get_children(self):
        url = self.slug+'/'
        return Page.objects.filter(slug__startswith=url)

class PageRevision(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=30)
    text = models.TextField()
    comment = models.CharField(max_length=30)
    date_written = models.DateTimeField()
    login = models.BooleanField()

    def __unicode__(self):
            return self.title

