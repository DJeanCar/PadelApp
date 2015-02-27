# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0002_auto_20150221_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocompeticion',
            name='slug',
            field=models.SlugField(default=False),
            preserve_default=False,
        ),
    ]
