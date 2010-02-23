from django.db import models
from django.contrib.admin.models import User

class Society(models.Model):
    """
    Represents a student society hosted on our servers.
    """
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    email = models.EmailField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Societies"

    def __unicode__(self):
        return "%s (su%d)" % (self.name, self.number)

class SocietyContact(models.Model):
    """
    Relates a society with a contact for that society
    """
    society = models.ForeignKey(Society)
    user = models.ForeignKey(User)
    start_date = models.DateField()

    class Meta:
        ordering = ['society','-start_date']

    def __unicode__(self):
        return "%s (%s)" % (self.society, self.start_date.year)

class SocietyLogEntry(models.Model):
    """
    Stores a note on a society
    """
    society = models.ForeignKey(Society)
    content = models.TextField()
    date = models.DateTimeField()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Society log entries"

    def __unicode__(self):
        return "Society log: %s" % society
