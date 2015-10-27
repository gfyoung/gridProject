# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gridEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_name', models.CharField(max_length=1000)),
                ('event_location', models.CharField(max_length=1000)),
                ('start_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='gridEventVendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grid_event', models.ForeignKey(to='gridApp.gridEvent')),
            ],
        ),
        migrations.CreateModel(
            name='gridVendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_name', models.CharField(max_length=1000)),
                ('vendor_link', models.CharField(max_length=1000)),
                ('vendor_img', models.CharField(max_length=1000)),
                ('event_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='grideventvendor',
            name='grid_vendor',
            field=models.ForeignKey(to='gridApp.gridVendor'),
        ),
    ]
