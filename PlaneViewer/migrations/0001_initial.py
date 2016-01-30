# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('image_page', models.CharField(max_length=200)),
                ('image_url', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('image_license', models.CharField(max_length=100)),
                ('license_text', models.CharField(max_length=1000)),
                ('location', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('aircraft', models.CharField(max_length=100)),
                ('aircraft_Type', models.CharField(max_length=50)),
                ('redownload_flag', models.BooleanField()),
            ],
            options={
                'db_table': 'images',
                'managed': False,
            },
        ),
    ]
