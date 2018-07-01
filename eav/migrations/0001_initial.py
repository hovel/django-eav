# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import eav.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='User-friendly attribute name', max_length=100, verbose_name='name')),
                ('slug', eav.fields.EavSlugField(help_text='Short unique attribute label', verbose_name='slug')),
                ('description', models.CharField(help_text='Short description', max_length=256, null=True, verbose_name='description', blank=True)),
                ('datatype', eav.fields.EavDatatypeField(max_length=8, verbose_name='data type', choices=[(b'text', 'Text'), (b'float', 'Float'), (b'int', 'Integer'), (b'date', 'Date'), (b'datetime', 'Datetime'), (b'bool', 'True / False'), (b'object', 'Django Object'), (b'enum', 'Multiple Choice')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('display_in_list', models.BooleanField(default=False, verbose_name='display in admin list view')),
                ('searchable', models.BooleanField(default=False, verbose_name='Allow searching on field')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'attribute',
                'verbose_name_plural': 'attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnumGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'enum group',
                'verbose_name_plural': 'enum groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnumValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=50, verbose_name='value', db_index=True)),
            ],
            options={
                'verbose_name': 'enum value',
                'verbose_name_plural': 'enum values',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity_id', models.IntegerField()),
                ('value_text', models.TextField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('value_int', models.IntegerField(null=True, blank=True)),
                ('value_date', models.DateTimeField(null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('generic_value_id', models.IntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('attribute', models.ForeignKey(verbose_name='attribute', to='eav.Attribute', on_delete=models.CASCADE)),
                ('entity_ct', models.ForeignKey(related_name='value_entities', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('generic_value_ct', models.ForeignKey(related_name='value_values', blank=True, to='contenttypes.ContentType', on_delete=models.CASCADE, null=True)),
                ('value_enum', models.ForeignKey(related_name='eav_values', blank=True, to='eav.EnumValue', on_delete=models.CASCADE, null=True)),
            ],
            options={
                'verbose_name': 'value',
                'verbose_name_plural': 'values',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='enumgroup',
            name='enums',
            field=models.ManyToManyField(to='eav.EnumValue', verbose_name='enum group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='enum_group',
            field=models.ForeignKey(verbose_name='choice group', blank=True, to='eav.EnumGroup', on_delete=models.CASCADE, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='parent',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', on_delete=models.CASCADE, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='site',
            field=models.ForeignKey(verbose_name='site', to='sites.Site', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('site', 'slug', 'parent')]),
        ),
        migrations.CreateModel(
            name='PartitionedAttribute',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('eav.attribute',),
        ),
    ]
