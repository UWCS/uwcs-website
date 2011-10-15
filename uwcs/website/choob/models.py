from django.db import models

class QuoteObject(models.Model):
    quoter = models.CharField(max_length=255, blank=True)
    hostmask = models.CharField(max_length=255, blank=True)
    lines = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    up = models.IntegerField(null=True, blank=True)
    down = models.IntegerField(null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = u'_objectdb_plugins_quote_quoteobject'

    def lines(self):
        return self.quoteline_set.order_by('linenumber')

    def __unicode__(self):
        s = ''
        for line in self.quoteline_set.order_by('linenumber'):
            s += str(line) + '\n'
        return s

class QuoteLine(models.Model):
    quote = models.ForeignKey(QuoteObject,null=True, blank=True, db_column='quoteid')
    linenumber = models.IntegerField(null=True, blank=True)
    nick = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)
    isaction = models.NullBooleanField(null=True, blank=True)
    
    class Meta:
        db_table = u'_objectdb_plugins_quote_quoteline'

    def __unicode__(self):
        return "%i. <%s> %s" % (self.linenumber,self.nick,self.message)
