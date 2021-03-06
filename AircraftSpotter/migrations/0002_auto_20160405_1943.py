# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-05 23:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AircraftSpotter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorReport',
            fields=[
                ('error_id', models.IntegerField(primary_key=True, serialize=False)),
                ('wrong_aircraft', models.BooleanField(default=False)),
                ('bad_picture', models.BooleanField(default=False)),
                ('open_response', models.CharField(blank=True, max_length=200)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AircraftSpotter.Aircraft')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_history', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='types',
            options={'managed': False, 'ordering': ('type_id',)},
        ),
    ]
