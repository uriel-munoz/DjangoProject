# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('product', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
