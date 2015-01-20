# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Attribute', fields ['site', 'slug']
        db.delete_unique('eav_attribute', ['site_id', 'slug'])

        # Deleting field 'Attribute.type'
        db.delete_column('eav_attribute', 'type')

        # Adding field 'Attribute.display_in_list'
        db.add_column('eav_attribute', 'display_in_list',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Attribute.searchable'
        db.add_column('eav_attribute', 'searchable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Attribute.parent'
        db.add_column('eav_attribute', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Attribute', fields ['site', 'parent', 'slug']
        db.create_unique('eav_attribute', ['site_id', 'parent_id', 'slug'])

    def backwards(self, orm):
        # Removing unique constraint on 'Attribute', fields ['site', 'parent', 'slug']
        db.delete_unique('eav_attribute', ['site_id', 'parent_id', 'slug'])

        # Adding field 'Attribute.type'
        db.add_column('eav_attribute', 'type',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Attribute.display_in_list'
        db.delete_column('eav_attribute', 'display_in_list')

        # Deleting field 'Attribute.searchable'
        db.delete_column('eav_attribute', 'searchable')

        # Deleting field 'Attribute.parent'
        db.delete_column('eav_attribute', 'parent_id')

        # Adding unique constraint on 'Attribute', fields ['site', 'slug']
        db.create_unique('eav_attribute', ['site_id', 'slug'])

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug', 'parent'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'display_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50'})
        },
        'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eav.EnumValue']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': "orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': "orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['eav']