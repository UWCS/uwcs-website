from django.db import models
from urllib import urlopen
from compsoc.search import register
from compsoc.settings import GAMING_SERVER, MEDIA_ROOT
from django.db.models.fields.files import FieldFile
from django.db import IntegrityError

import os

# set timeout - note this should be written for python 3k
import socket
socket.setdefaulttimeout(0.1)

class Page(models.Model):
    slug = models.CharField(max_length=30, unique=True)
    
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

    def move(self, destination, with_attachments=True, with_children=True):
        """
        Moves a page to a new location. As well as changing the slug, it
        has the ability to move attached items and children also. 
        Will error if the root page cannot be moved, will silently fail to
        move any subpages that cannot be moved.
        NOTE: This will always call self.save()
        """
        if with_children: children = self.get_children()
        self.slug = destination

        # unique=True makes sure we can move to here first 
        self.save()

        # now remember to update the attachments
        if with_attachments:
            for a in self.attachment_set.iterator():
                a.move(self, save=True)

        if with_children:
            for child in children:
                suffix = child.slug.rstrip('/').split('/')[-1]
                # disjointed pages can exist, we might end up moving a 
                # child to somewhere that already exists, in this case we skip
                # that one.
                try:
                    child.move("%s/%s" % (destination, suffix))
                except IntegrityError:
                    pass

register(Page, ['title','text'])

class MovableFieldFile(FieldFile):
    """
    An extension to the standard FieldFile with the added ability to be moved/renamed.
    """
    def move(self, destination, save=False):
        """
        Will move the file on disk and update the model to reflect this.
        """
        self._require_file()

        old_location = self._name
        self._name = self.storage.save(destination, self.file)
        setattr(self.instance, self.field.name, self.name)

        # Update the filesize cache
        self._size = len(self.file)

        self.storage.delete(old_location)
        if save: self.instance.save()

class Attachment(models.Model):
    page = models.ForeignKey(Page)
    title = models.CharField(max_length=50)

    def upload_path(self, filename, *args, **kwargs):
        """
        Decides where to save the file, based on the page it's
        attached to.
        """
        return "cms/%s/attachment/%s" % (self.page.slug, filename)

    file = models.FileField(upload_to=upload_path)
    file.attr_class = MovableFieldFile

    def __unicode__(self):
        return self.file.name

    def get_absolute_url(self):
        return "/%s" % self.file.name

    def move(self, destination_page, save=False):
        """
        Updates the file field and moves physical file to reflect a new page.
        Useful for updating attachments when you move their related page.
        """
        name = self.file.name.rstrip('/').split('/')[-1]
        self.page = destination_page
        self.file.move("cms/%s/attachment/%s" % (destination_page.slug, name), save=save)

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
