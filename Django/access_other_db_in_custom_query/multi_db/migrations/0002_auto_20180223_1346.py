# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-23 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=12)),
            ],
        ),
        migrations.DeleteModel(
            name='Professor',
        ),
    ]
