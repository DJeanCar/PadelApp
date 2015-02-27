# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0003_tipocompeticion_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competicion',
            old_name='precio',
            new_name='price',
        ),
    ]
