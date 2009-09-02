from django.db import models
from urllib import urlopen
from compsoc.search import register
from compsoc.settings import GAMING_SERVER, MEDIA_ROOT
import os

# set timeout - note this should be written for python 3k
import socket
socket.setdefaulttimeout(0.1)

class Page(models.Model):
    slug = models.CharField(max_length=30)
    
    def __unicode__(self):
            return self.slug

    def get_data(self):
        return self.pagerevision_set.latest('date_written')

    def text(self):
        # This is to allow templates dealing with both Communications and
        # Pages to use the same methods.
        return self.get_data().text

    def title(self):
        return self.get_data().title

    def login(self):
        return self.get_data().login

    def get_siblings_and_self(self):
        parent_slug = '/'.join(self.slug.split('/')[:-1])
        peers = []

        child_prefix = parent_slug

        if parent_slug != "":
            child_prefix += '/'

        for p in Page.objects.filter(slug__startswith=child_prefix):
            if p.slug[len(child_prefix):].count('/') == 0:
                peers.append(p)
        return peers

    def get_children(self):
        url = self.slug + '/'
        children = []
        for p in Page.objects.filter(slug__startswith=url):
            if p.slug[len(url):].count('/') == 0:
                children.append(p)
        return sorted(children, key=lambda x: x.title())

    def get_absolute_url(self):
        return "/cms/%s" % self.slug

register(Page, ['title','text'])

class Attachment(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=50)

    def upload_path(self, filename, *args, **kwargs):
        return "cms/%s/attachment/%s" % (self.page.slug, filename)

    file = models.FileField(upload_to=upload_path)

    def __unicode__(self):
        return self.file.name

    def get_absolute_url(self):
        return "/%s" % self.file.name

class PageRevision(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=30)
    text = models.TextField()
    comment = models.CharField(max_length=30)
    date_written = models.DateTimeField()
    login = models.BooleanField()

    def __unicode__(self):
            return self.title

class Game(models.Model):
    title = models.CharField(max_length=255)
    port = models.IntegerField()

    def __unicode__(self):
        return self.title

    def is_online(self):
        try:
            urlopen("http://%s:%i"%(GAMING_SERVER,self.port)).close()
            return True
        except IOError:
            return False
