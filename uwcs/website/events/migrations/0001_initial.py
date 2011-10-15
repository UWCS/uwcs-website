# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventType'
        db.create_table('events_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('info', self.gf('django.db.models.fields.TextField')()),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('events', ['EventType'])

        # Adding model 'Location'
        db.create_table('events_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image_url', self.gf('django.db.models.fields.CharField')(default='/static/img/no_location.png', max_length=255)),
            ('map_loc', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('events', ['Location'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.EventType'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Location'])),
            ('shortDescription', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('longDescription', self.gf('django.db.models.fields.TextField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('finish', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 15, 23, 22, 49, 8519))),
            ('displayFrom', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding model 'SteamEvent'
        db.create_table('events_steamevent', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['events.Event'], unique=True, primary_key=True)),
            ('steam_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('events', ['SteamEvent'])

        # Adding model 'SeatingRoom'
        db.create_table('events_seatingroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Location'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('max_cols', self.gf('django.db.models.fields.IntegerField')()),
            ('max_rows', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('events', ['SeatingRoom'])

        # Adding model 'EventSignup'
        db.create_table('events_eventsignup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['events.Event'], unique=True)),
            ('signupsLimit', self.gf('django.db.models.fields.IntegerField')()),
            ('open', self.gf('django.db.models.fields.DateTimeField')()),
            ('close', self.gf('django.db.models.fields.DateTimeField')()),
            ('fresher_open', self.gf('django.db.models.fields.DateTimeField')()),
            ('guest_open', self.gf('django.db.models.fields.DateTimeField')()),
            ('seating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.SeatingRoom'], null=True, blank=True)),
        ))
        db.send_create_signal('events', ['EventSignup'])

        # Adding model 'Signup'
        db.create_table('events_signup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('events', ['Signup'])

        # Adding unique constraint on 'Signup', fields ['event', 'user']
        db.create_unique('events_signup', ['event_id', 'user_id'])

        # Adding model 'SeatingRevision'
        db.create_table('events_seatingrevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('events', ['SeatingRevision'])

        # Adding unique constraint on 'SeatingRevision', fields ['event', 'number']
        db.create_unique('events_seatingrevision', ['event_id', 'number'])

        # Adding model 'Seating'
        db.create_table('events_seating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.SeatingRevision'])),
            ('col', self.gf('django.db.models.fields.IntegerField')()),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('events', ['Seating'])

        # Adding model 'SteamEventFeed'
        db.create_table('events_steameventfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.EventType'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Location'])),
        ))
        db.send_create_signal('events', ['SteamEventFeed'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SeatingRevision', fields ['event', 'number']
        db.delete_unique('events_seatingrevision', ['event_id', 'number'])

        # Removing unique constraint on 'Signup', fields ['event', 'user']
        db.delete_unique('events_signup', ['event_id', 'user_id'])

        # Deleting model 'EventType'
        db.delete_table('events_eventtype')

        # Deleting model 'Location'
        db.delete_table('events_location')

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Deleting model 'SteamEvent'
        db.delete_table('events_steamevent')

        # Deleting model 'SeatingRoom'
        db.delete_table('events_seatingroom')

        # Deleting model 'EventSignup'
        db.delete_table('events_eventsignup')

        # Deleting model 'Signup'
        db.delete_table('events_signup')

        # Deleting model 'SeatingRevision'
        db.delete_table('events_seatingrevision')

        # Deleting model 'Seating'
        db.delete_table('events_seating')

        # Deleting model 'SteamEventFeed'
        db.delete_table('events_steameventfeed')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'displayFrom': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 15, 23, 22, 49, 22415)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']"}),
            'longDescription': ('django.db.models.fields.TextField', [], {}),
            'shortDescription': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventType']"})
        },
        'events.eventsignup': {
            'Meta': {'object_name': 'EventSignup'},
            'close': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['events.Event']", 'unique': 'True'}),
            'fresher_open': ('django.db.models.fields.DateTimeField', [], {}),
            'guest_open': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open': ('django.db.models.fields.DateTimeField', [], {}),
            'seating': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.SeatingRoom']", 'null': 'True', 'blank': 'True'}),
            'signupsLimit': ('django.db.models.fields.IntegerField', [], {})
        },
        'events.eventtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EventType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'events.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'default': "'/static/img/no_location.png'", 'max_length': '255'}),
            'map_loc': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'events.seating': {
            'Meta': {'object_name': 'Seating'},
            'col': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.SeatingRevision']"}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'events.seatingrevision': {
            'Meta': {'unique_together': "(('event', 'number'),)", 'object_name': 'SeatingRevision'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'events.seatingroom': {
            'Meta': {'object_name': 'SeatingRoom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_cols': ('django.db.models.fields.IntegerField', [], {}),
            'max_rows': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']"})
        },
        'events.signup': {
            'Meta': {'ordering': "['time']", 'unique_together': "(('event', 'user'),)", 'object_name': 'Signup'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'events.steamevent': {
            'Meta': {'object_name': 'SteamEvent', '_ormbases': ['events.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['events.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'steam_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'events.steameventfeed': {
            'Meta': {'object_name': 'SteamEventFeed'},
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventType']"}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']"})
        }
    }

    complete_apps = ['events']
