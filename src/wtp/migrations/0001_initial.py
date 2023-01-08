# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('wtp_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('confirmKey', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True, null=True, blank=True)),
            ('showInHallOfFame', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('showAsFirstSolver', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('showAsSolver', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('showPublicProfile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebookId', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True)),
            ('twitterAccessKey', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('twitterAccessSecret', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('twitterMessage', self.gf('django.db.models.fields.CharField')(default='', max_length=140, blank=True)),
            ('twitterAutoTweet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitterFailedAttempts', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('wtp', ['UserProfile'])

        # Adding model 'UserOpenID'
        db.create_table('wtp_useropenid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('wtp', ['UserOpenID'])

        # Adding model 'OpenIDAssociation'
        db.create_table('wtp_openidassociation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.TextField')(max_length=2047)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')()),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('assoc_type', self.gf('django.db.models.fields.TextField')(max_length=64)),
        ))
        db.send_create_signal('wtp', ['OpenIDAssociation'])

        # Adding model 'OpenIDNonce'
        db.create_table('wtp_openidnonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('wtp', ['OpenIDNonce'])

        # Adding model 'PageHit'
        db.create_table('wtp_pagehit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sessionKey', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('statusCode', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('wtp', ['PageHit'])

        # Adding model 'TrafficDigest'
        db.create_table('wtp_trafficdigest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('hour', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('requests', self.gf('django.db.models.fields.IntegerField')()),
            ('sessions', self.gf('django.db.models.fields.IntegerField')()),
            ('users', self.gf('django.db.models.fields.IntegerField')()),
            ('resolutions', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wtp', ['TrafficDigest'])

        # Adding unique constraint on 'TrafficDigest', fields ['date', 'hour']
        db.create_unique('wtp_trafficdigest', ['date', 'hour'])

        # Adding model 'SentMail'
        db.create_table('wtp_sentmail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('wtp', ['SentMail'])

        # Adding model 'Tweet'
        db.create_table('wtp_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestampCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('timestampSent', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('wtp', ['Tweet'])

        # Adding model 'License'
        db.create_table('wtp_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('wtp', ['License'])

        # Adding model 'Image'
        db.create_table('wtp_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageHash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('hint', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtp.License'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wtp', ['Image'])

        # Adding model 'Solution'
        db.create_table('wtp_solution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtp.Image'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('wtp', ['Solution'])

        # Adding unique constraint on 'Solution', fields ['image', 'value']
        db.create_unique('wtp_solution', ['image_id', 'value'])

        # Adding model 'Resolution'
        db.create_table('wtp_resolution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtp.Image'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtp.Solution'], null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('wtp', ['Resolution'])

        # Adding unique constraint on 'Resolution', fields ['image', 'user']
        db.create_unique('wtp_resolution', ['image_id', 'user_id'])

        # Adding model 'Comment'
        db.create_table('wtp_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wtp.Image'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('wtp', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Resolution', fields ['image', 'user']
        db.delete_unique('wtp_resolution', ['image_id', 'user_id'])

        # Removing unique constraint on 'Solution', fields ['image', 'value']
        db.delete_unique('wtp_solution', ['image_id', 'value'])

        # Removing unique constraint on 'TrafficDigest', fields ['date', 'hour']
        db.delete_unique('wtp_trafficdigest', ['date', 'hour'])

        # Deleting model 'UserProfile'
        db.delete_table('wtp_userprofile')

        # Deleting model 'UserOpenID'
        db.delete_table('wtp_useropenid')

        # Deleting model 'OpenIDAssociation'
        db.delete_table('wtp_openidassociation')

        # Deleting model 'OpenIDNonce'
        db.delete_table('wtp_openidnonce')

        # Deleting model 'PageHit'
        db.delete_table('wtp_pagehit')

        # Deleting model 'TrafficDigest'
        db.delete_table('wtp_trafficdigest')

        # Deleting model 'SentMail'
        db.delete_table('wtp_sentmail')

        # Deleting model 'Tweet'
        db.delete_table('wtp_tweet')

        # Deleting model 'License'
        db.delete_table('wtp_license')

        # Deleting model 'Image'
        db.delete_table('wtp_image')

        # Deleting model 'Solution'
        db.delete_table('wtp_solution')

        # Deleting model 'Resolution'
        db.delete_table('wtp_resolution')

        # Deleting model 'Comment'
        db.delete_table('wtp_comment')


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
        'wtp.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wtp.Image']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wtp.image': {
            'Meta': {'object_name': 'Image'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hint': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageHash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wtp.License']"}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'wtp.license': {
            'Meta': {'object_name': 'License'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'wtp.openidassociation': {
            'Meta': {'object_name': 'OpenIDAssociation'},
            'assoc_type': ('django.db.models.fields.TextField', [], {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.TextField', [], {'max_length': '2047'})
        },
        'wtp.openidnonce': {
            'Meta': {'object_name': 'OpenIDNonce'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'wtp.pagehit': {
            'Meta': {'object_name': 'PageHit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sessionKey': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'statusCode': ('django.db.models.fields.SmallIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'wtp.resolution': {
            'Meta': {'unique_together': "(('image', 'user'),)", 'object_name': 'Resolution'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wtp.Image']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wtp.Solution']", 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wtp.sentmail': {
            'Meta': {'object_name': 'SentMail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'wtp.solution': {
            'Meta': {'unique_together': "(('image', 'value'),)", 'object_name': 'Solution'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wtp.Image']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'wtp.trafficdigest': {
            'Meta': {'unique_together': "(('date', 'hour'),)", 'object_name': 'TrafficDigest'},
            'comments': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'hour': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requests': ('django.db.models.fields.IntegerField', [], {}),
            'resolutions': ('django.db.models.fields.IntegerField', [], {}),
            'sessions': ('django.db.models.fields.IntegerField', [], {}),
            'users': ('django.db.models.fields.IntegerField', [], {})
        },
        'wtp.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'timestampCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timestampSent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wtp.useropenid': {
            'Meta': {'object_name': 'UserOpenID'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wtp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'confirmKey': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebookId': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'showAsFirstSolver': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'showAsSolver': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'showInHallOfFame': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'showPublicProfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitterAccessKey': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'twitterAccessSecret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'twitterAutoTweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitterFailedAttempts': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'twitterMessage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['wtp']