# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipocompeticion',
            name='precio',
        ),
        migrations.AddField(
            model_name='competicion',
            name='precio',
            field=models.FloatField(default=False),
            preserve_default=False,
        ),
    ]
