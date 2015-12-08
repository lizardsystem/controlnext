# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.temp_username'
        db.add_column('controlnext_userprofile', 'temp_username',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'UserProfile.user'
        db.alter_column('controlnext_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    def backwards(self, orm):
        # Deleting field 'UserProfile.temp_username'
        db.delete_column('controlnext_userprofile', 'temp_username')


        # User chose to not deal with backwards NULL issues for 'UserProfile.user'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserProfile.user'
        db.alter_column('controlnext_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

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
        'controlnext.basin': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Basin'},
            'current_fill': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'current_fill_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'grower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdbc_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsjdbc.JdbcSource']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_outflow_per_timeunit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'max_storage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'osmose_till_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'parameter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_flood_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rain_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'random_url_slug': ('django.db.models.fields.CharField', [], {'default': "u'xh2np0ld8upta4i0ivi2'", 'unique': 'True', 'max_length': '20'}),
            'recirculation': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'reverse_osmosis': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'controlnext.growerinfo': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'GrowerInfo'},
            'crop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'crop_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'controlnext.userprofile': {
            'Meta': {'ordering': "(u'user',)", 'object_name': 'UserProfile'},
            'grower': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['controlnext.GrowerInfo']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temp_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'controlnext.waterdemand': {
            'Meta': {'object_name': 'WaterDemand'},
            'daynumber': ('django.db.models.fields.IntegerField', [], {}),
            'demand': ('django.db.models.fields.FloatField', [], {}),
            'grower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weeknumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'lizard_fewsjdbc.jdbcsource': {
            'Meta': {'object_name': 'JdbcSource'},
            'connector_string': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'customfilter': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filter_tree_root': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdbc_tag_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'jdbc_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'timezone_string': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'usecustomfilter': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['controlnext']