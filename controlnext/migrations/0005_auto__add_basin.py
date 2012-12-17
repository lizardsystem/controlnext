# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Basin'
        db.create_table('controlnext_basin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['controlnext.GrowerInfo'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('filter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('parameter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rain_filter_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rain_location_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('max_storage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_storage_pct', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_storage_pct', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rain_flood_surface', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_outflow_per_timeunit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('basin_top', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('level_indicator_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('current_fill', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('current_fill_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('jdbc_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_fewsjdbc.JdbcSource'], null=True, blank=True)),
        ))
        db.send_create_signal('controlnext', ['Basin'])


    def backwards(self, orm):
        
        # Deleting model 'Basin'
        db.delete_table('controlnext_basin')


    models = {
        'controlnext.basin': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Basin'},
            'basin_top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_fill': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'current_fill_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdbc_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsjdbc.JdbcSource']", 'null': 'True', 'blank': 'True'}),
            'level_indicator_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_outflow_per_timeunit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'max_storage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['controlnext.GrowerInfo']"}),
            'parameter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_flood_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rain_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'controlnext.growerinfo': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'GrowerInfo'},
            'basin_top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fill_parameter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdbc_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsjdbc.JdbcSource']", 'null': 'True', 'blank': 'True'}),
            'level_indicator_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'max_outflow_per_timeunit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'max_storage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_storage_pct': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_filter_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rain_flood_surface': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rain_location_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'usecustomfilter': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['controlnext']
