# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('cms_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('cms', ['Page'])

        # Adding model 'Attachment'
        db.create_table('cms_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cms', ['Attachment'])

        # Adding model 'PageRevision'
        db.create_table('cms_pagerevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date_written', self.gf('django.db.models.fields.DateTimeField')()),
            ('login', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cms', ['PageRevision'])

        # Adding model 'Game'
        db.create_table('cms_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cms', ['Game'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('cms_page')

        # Deleting model 'Attachment'
        db.delete_table('cms_attachment')

        # Deleting model 'PageRevision'
        db.delete_table('cms_pagerevision')

        # Deleting model 'Game'
        db.delete_table('cms_game')


    models = {
        'cms.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cms.game': {
            'Meta': {'object_name': 'Game'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cms.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.pagerevision': {
            'Meta': {'object_name': 'PageRevision'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_written': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['cms']
