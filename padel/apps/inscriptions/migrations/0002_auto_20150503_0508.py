# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='nivel',
            field=models.ForeignKey(blank=True, to='torneos.Nivel', null=True),
            preserve_default=True,
        ),
    ]
