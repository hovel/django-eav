# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Attribute.created'
        db.alter_column(u'eav_attribute', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Attribute.datatype'
        db.alter_column(u'eav_attribute', 'datatype', self.gf('eav.fields.EavDatatypeField')(max_length=8))

        # Changing field 'Value.created'
        db.alter_column(u'eav_value', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'Attribute.created'
        db.alter_column(u'eav_attribute', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Attribute.datatype'
        db.alter_column(u'eav_attribute', 'datatype', self.gf('eav.fields.EavDatatypeField')(max_length=6))

        # Changing field 'Value.created'
        db.alter_column(u'eav_value', 'created', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug', 'parent'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '8'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'display_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50'})
        },
        u'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['eav.EnumValue']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        u'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': u"orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': u"orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['eav']