# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Member'
        db.create_table('memberinfo_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('showDetails', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('guest', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('memberinfo', ['Member'])

        # Adding model 'GuestReason'
        db.create_table('memberinfo_guestreason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('memberinfo', ['GuestReason'])

        # Adding model 'WebsiteDetails'
        db.create_table('memberinfo_websitedetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('websiteUrl', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('websiteTitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('memberinfo', ['WebsiteDetails'])

        # Adding model 'NicknameDetails'
        db.create_table('memberinfo_nicknamedetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('memberinfo', ['NicknameDetails'])

        # Adding model 'GamingIDs'
        db.create_table('memberinfo_gamingids', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('steamID', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('xboxID', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('psnID', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('xfireID', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('memberinfo', ['GamingIDs'])

        # Adding model 'MemberJoin'
        db.create_table('memberinfo_memberjoin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('memberinfo', ['MemberJoin'])

        # Adding model 'Term'
        db.create_table('memberinfo_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_number', self.gf('django.db.models.fields.IntegerField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('which', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('memberinfo', ['Term'])

        # Adding model 'ShellAccount'
        db.create_table('memberinfo_shellaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('memberinfo', ['ShellAccount'])

        # Adding model 'DatabaseAccount'
        db.create_table('memberinfo_databaseaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('memberinfo', ['DatabaseAccount'])

        # Adding model 'Quota'
        db.create_table('memberinfo_quota', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('quota_size', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('memberinfo', ['Quota'])

        # Adding model 'MailingList'
        db.create_table('memberinfo_mailinglist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('list', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('memberinfo', ['MailingList'])

        # Adding M2M table for field users on 'MailingList'
        db.create_table('memberinfo_mailinglist_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(orm['memberinfo.mailinglist'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('memberinfo_mailinglist_users', ['mailinglist_id', 'user_id'])

        # Adding model 'ExecPosition'
        db.create_table('memberinfo_execposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('memberinfo', ['ExecPosition'])

        # Adding model 'ExecPlacement'
        db.create_table('memberinfo_execplacement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['memberinfo.ExecPosition'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('memberinfo', ['ExecPlacement'])

        # Adding model 'Society'
        db.create_table('memberinfo_society', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(related_name='represented_societies', to=orm['auth.User'])),
        ))
        db.send_create_signal('memberinfo', ['Society'])


    def backwards(self, orm):
        
        # Deleting model 'Member'
        db.delete_table('memberinfo_member')

        # Deleting model 'GuestReason'
        db.delete_table('memberinfo_guestreason')

        # Deleting model 'WebsiteDetails'
        db.delete_table('memberinfo_websitedetails')

        # Deleting model 'NicknameDetails'
        db.delete_table('memberinfo_nicknamedetails')

        # Deleting model 'GamingIDs'
        db.delete_table('memberinfo_gamingids')

        # Deleting model 'MemberJoin'
        db.delete_table('memberinfo_memberjoin')

        # Deleting model 'Term'
        db.delete_table('memberinfo_term')

        # Deleting model 'ShellAccount'
        db.delete_table('memberinfo_shellaccount')

        # Deleting model 'DatabaseAccount'
        db.delete_table('memberinfo_databaseaccount')

        # Deleting model 'Quota'
        db.delete_table('memberinfo_quota')

        # Deleting model 'MailingList'
        db.delete_table('memberinfo_mailinglist')

        # Removing M2M table for field users on 'MailingList'
        db.delete_table('memberinfo_mailinglist_users')

        # Deleting model 'ExecPosition'
        db.delete_table('memberinfo_execposition')

        # Deleting model 'ExecPlacement'
        db.delete_table('memberinfo_execplacement')

        # Deleting model 'Society'
        db.delete_table('memberinfo_society')


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
        'memberinfo.databaseaccount': {
            'Meta': {'object_name': 'DatabaseAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'memberinfo.execplacement': {
            'Meta': {'ordering': "['start']", 'object_name': 'ExecPlacement'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['memberinfo.ExecPosition']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'memberinfo.execposition': {
            'Meta': {'ordering': "['title']", 'object_name': 'ExecPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'memberinfo.gamingids': {
            'Meta': {'object_name': 'GamingIDs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'psnID': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'steamID': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'xboxID': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'xfireID': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'memberinfo.guestreason': {
            'Meta': {'object_name': 'GuestReason'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'memberinfo.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'memberinfo.member': {
            'Meta': {'object_name': 'Member'},
            'guest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'showDetails': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'memberinfo.memberjoin': {
            'Meta': {'object_name': 'MemberJoin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'memberinfo.nicknamedetails': {
            'Meta': {'object_name': 'NicknameDetails'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'memberinfo.quota': {
            'Meta': {'object_name': 'Quota'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'quota_size': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'memberinfo.shellaccount': {
            'Meta': {'object_name': 'ShellAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'memberinfo.society': {
            'Meta': {'object_name': 'Society', '_ormbases': ['auth.User']},
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'represented_societies'", 'to': "orm['auth.User']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'memberinfo.term': {
            'Meta': {'object_name': 'Term'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_number': ('django.db.models.fields.IntegerField', [], {}),
            'which': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'memberinfo.websitedetails': {
            'Meta': {'object_name': 'WebsiteDetails'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'websiteTitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'websiteUrl': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['memberinfo']
