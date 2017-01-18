# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager
import django.contrib.sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ('eav', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='attribute',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
