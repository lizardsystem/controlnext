# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GrowerInfo'
        db.create_table('controlnext_growerinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('crop', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fill_filter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fill_location_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fill_parameter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rain_filter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rain_location_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('max_storage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_storage_pct', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_storage_pct', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rain_flood_surface', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_outflow_per_timeunit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('basin_top', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('level_indicator_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('controlnext', ['GrowerInfo'])


    def backwards(self, orm):
        
        # Deleting model 'GrowerInfo'
        db.delete_table('controlnext_growerinfo')


    models = {
        'controlnext.growerinfo': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'GrowerInfo'},
            'basin_top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_parameter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_indicator_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_outflow_per_timeunit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_storage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_flood_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rain_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['controlnext']
