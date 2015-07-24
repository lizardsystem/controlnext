# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from controlnext.models import random_slug

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'GrowerInfo.rain_filter_id'
        db.delete_column('controlnext_growerinfo', 'rain_filter_id')

        # Deleting field 'GrowerInfo.fill_parameter_id'
        db.delete_column('controlnext_growerinfo', 'fill_parameter_id')

        # Deleting field 'GrowerInfo.min_storage_pct'
        db.delete_column('controlnext_growerinfo', 'min_storage_pct')

        # Deleting field 'GrowerInfo.max_storage'
        db.delete_column('controlnext_growerinfo', 'max_storage')

        # Deleting field 'GrowerInfo.rain_flood_surface'
        db.delete_column('controlnext_growerinfo', 'rain_flood_surface')

        # Deleting field 'GrowerInfo.fill_filter_id'
        db.delete_column('controlnext_growerinfo', 'fill_filter_id')

        # Deleting field 'GrowerInfo.basin_top'
        db.delete_column('controlnext_growerinfo', 'basin_top')

        # Deleting field 'GrowerInfo.max_storage_pct'
        db.delete_column('controlnext_growerinfo', 'max_storage_pct')

        # Deleting field 'GrowerInfo.max_storage_pct'
        db.delete_column('controlnext_growerinfo', 'max_outflow_per_timeunit')

        # Deleting field 'GrowerInfo.level_indicator_height'
        db.delete_column('controlnext_growerinfo', 'level_indicator_height')

        # Deleting field 'GrowerInfo.rain_location_id'
        db.delete_column('controlnext_growerinfo', 'rain_location_id')

        # Deleting field 'GrowerInfo.fill_location_id'
        db.delete_column('controlnext_growerinfo', 'fill_location_id')

        # Deleting field 'GrowerInfo.jdbc_source'
        db.delete_column('controlnext_growerinfo', 'jdbc_source_id')

        # Deleting field 'GrowerInfo.location'
        db.delete_column('controlnext_growerinfo', 'location')

        # Deleting field 'Basin.greenhouse_valve_2_parameter_id'
        db.delete_column('controlnext_basin', 'greenhouse_valve_2_parameter_id')

        # Deleting field 'Basin.min_storage_pct'
        db.delete_column('controlnext_basin', 'min_storage_pct')

        # Deleting field 'Basin.greenhouse_valve_2_location_id'
        db.delete_column('controlnext_basin', 'greenhouse_valve_2_location_id')

        # Deleting field 'Basin.discharge_valve_parameter_id'
        db.delete_column('controlnext_basin', 'discharge_valve_parameter_id')

        # Deleting field 'Basin.greenhouse_valve_2_filter_id'
        db.delete_column('controlnext_basin', 'greenhouse_valve_2_filter_id')

        # Deleting field 'Basin.predicted_5d_rain_parameter_id'
        db.delete_column('controlnext_basin', 'predicted_5d_rain_parameter_id')

        # Deleting field 'Basin.predicted_5d_rain_filter_id'
        db.delete_column('controlnext_basin', 'predicted_5d_rain_filter_id')

        # Deleting field 'Basin.own_meter_location_id'
        db.delete_column('controlnext_basin', 'own_meter_location_id')

        # Deleting field 'Basin.own_meter_filter_id'
        db.delete_column('controlnext_basin', 'own_meter_filter_id')

        # Deleting field 'Basin.greenhouse_valve_1_parameter_id'
        db.delete_column('controlnext_basin', 'greenhouse_valve_1_parameter_id')

        # Deleting field 'Basin.own_meter_parameter_id'
        db.delete_column('controlnext_basin', 'own_meter_parameter_id')

        # Deleting field 'Basin.real_5d_rain_parameter_id'
        db.delete_column('controlnext_basin', 'real_5d_rain_parameter_id')

        # Deleting field 'Basin.greenhouse_valve_1_filter_id'
        db.delete_column('controlnext_basin', 'greenhouse_valve_1_filter_id')

        # Deleting field 'Basin.discharge_valve_filter_id'
        db.delete_column('controlnext_basin', 'discharge_valve_filter_id')

        # Deleting field 'Basin.basin_top'
        db.delete_column('controlnext_basin', 'basin_top')

        # Deleting field 'Basin.discharge_valve_location_id'
        db.delete_column('controlnext_basin', 'discharge_valve_location_id')

        # Deleting field 'Basin.level_indicator_height'
        db.delete_column('controlnext_basin', 'level_indicator_height')

        # Deleting field 'Basin.real_5d_rain_filter_id'
        db.delete_column('controlnext_basin', 'real_5d_rain_filter_id')

        # Deleting field 'Basin.max_storage_pct'
        db.delete_column('controlnext_basin', 'max_storage_pct')

        # Deleting field 'Basin.greenhouse_valve_1_location_id'cd
        db.delete_column('controlnext_basin', 'greenhouse_valve_1_location_id')

        # Deleting field 'Basin.on_main_map'
        db.delete_column('controlnext_basin', 'on_main_map')


    def backwards(self, orm):
        # Adding field 'GrowerInfo.rain_filter_id'
        db.add_column('controlnext_growerinfo', 'rain_filter_id',
                      self.gf('django.db.models.fields.CharField')(
                          max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.fill_parameter_id'
        db.add_column('controlnext_growerinfo', 'fill_parameter_id',
                      self.gf('django.db.models.fields.CharField')(
                          max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.min_storage_pct'
        db.add_column('controlnext_growerinfo', 'min_storage_pct',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.max_storage'
        db.add_column('controlnext_growerinfo', 'max_storage',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding  field 'GrowerInfo.max_outflow_per_time_unit'
        db.add_column('controlnext_growerinfo', 'max_outflow_per_timeunit',
                      self.gf('django.db.models.fields.DecimalField')(
                          max_digits=10, decimal_places=2, blank=True,
                          null=True, verbose_name=_("current fill (m3)")),
                      keep_default=False)

        # Adding field 'GrowerInfo.rain_flood_surface'
        db.add_column('controlnext_growerinfo', 'rain_flood_surface',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.fill_filter_id'
        db.add_column('controlnext_growerinfo', 'fill_filter_id',
                      self.gf('django.db.models.fields.CharField')(
                          max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.basin_top'
        db.add_column('controlnext_growerinfo', 'basin_top',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.max_storage_pct'
        db.add_column('controlnext_growerinfo', 'max_storage_pct',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.level_indicator_height'
        db.add_column('controlnext_growerinfo', 'level_indicator_height',
                      self.gf('django.db.models.fields.IntegerField')(
                          null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.rain_location_id'
        db.add_column('controlnext_growerinfo', 'rain_location_id',
                      self.gf('django.db.models.fields.CharField')(
                          max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.fill_location_id'
        db.add_column('controlnext_growerinfo', 'fill_location_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.jdbc_source'
        db.add_column('controlnext_growerinfo', 'jdbc_source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_fewsjdbc.JdbcSource'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'GrowerInfo.location'
        db.add_column('controlnext_growerinfo', 'location',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_2_parameter_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_2_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.min_storage_pct'
        db.add_column('controlnext_basin', 'min_storage_pct',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_2_location_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_2_location_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.discharge_valve_parameter_id'
        db.add_column('controlnext_basin', 'discharge_valve_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_2_filter_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_2_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.predicted_5d_rain_parameter_id'
        db.add_column('controlnext_basin', 'predicted_5d_rain_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.predicted_5d_rain_filter_id'
        db.add_column('controlnext_basin', 'predicted_5d_rain_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.own_meter_location_id'
        db.add_column('controlnext_basin', 'own_meter_location_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.own_meter_filter_id'
        db.add_column('controlnext_basin', 'own_meter_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_1_parameter_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_1_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.own_meter_parameter_id'
        db.add_column('controlnext_basin', 'own_meter_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.real_5d_rain_parameter_id'
        db.add_column('controlnext_basin', 'real_5d_rain_parameter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_1_filter_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_1_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.discharge_valve_filter_id'
        db.add_column('controlnext_basin', 'discharge_valve_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.basin_top'
        db.add_column('controlnext_basin', 'basin_top',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.discharge_valve_location_id'
        db.add_column('controlnext_basin', 'discharge_valve_location_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.level_indicator_height'
        db.add_column('controlnext_basin', 'level_indicator_height',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.real_5d_rain_filter_id'
        db.add_column('controlnext_basin', 'real_5d_rain_filter_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.max_storage_pct'
        db.add_column('controlnext_basin', 'max_storage_pct',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.greenhouse_valve_1_location_id'
        db.add_column('controlnext_basin', 'greenhouse_valve_1_location_id',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Basin.on_main_map'
        db.add_column('controlnext_basin', 'on_main_map',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdbc_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsjdbc.JdbcSource']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_outflow_per_timeunit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'max_storage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'osmose_till_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'grower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
            'parameter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_flood_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rain_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recirculation': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'reverse_osmosis': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'controlnext.growerinfo': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'GrowerInfo'},
            'crop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'crop_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'random_url_slug': ('django.db.models.fields.CharField', [], {'default': "u'fen0i3yc7tqfin1iyve7'", 'unique': 'True', 'max_length': '20'})
        },
        'controlnext.userprofile': {
            'Meta': {'ordering': "(u'owner',)", 'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'grower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'controlnext.waterdemand': {
            'Meta': {'object_name': 'WaterDemand'},
            'daynumber': ('django.db.models.fields.IntegerField', [], {}),
            'demand': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'grower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
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