# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'QuoteObject'
        db.create_table(u'_objectdb_plugins_quote_quoteobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quoter', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hostmask', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('up', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('down', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('choob', ['QuoteObject'])

        # Adding model 'QuoteLine'
        db.create_table(u'_objectdb_plugins_quote_quoteline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['choob.QuoteObject'], null=True, db_column='quoteid', blank=True)),
            ('linenumber', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('isaction', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('choob', ['QuoteLine'])


    def backwards(self, orm):
        
        # Deleting model 'QuoteObject'
        db.delete_table(u'_objectdb_plugins_quote_quoteobject')

        # Deleting model 'QuoteLine'
        db.delete_table(u'_objectdb_plugins_quote_quoteline')


    models = {
        'choob.quoteline': {
            'Meta': {'object_name': 'QuoteLine', 'db_table': "u'_objectdb_plugins_quote_quoteline'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isaction': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'linenumber': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['choob.QuoteObject']", 'null': 'True', 'db_column': "'quoteid'", 'blank': 'True'})
        },
        'choob.quoteobject': {
            'Meta': {'object_name': 'QuoteObject', 'db_table': "u'_objectdb_plugins_quote_quoteobject'"},
            'down': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hostmask': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quoter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'up': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['choob']
