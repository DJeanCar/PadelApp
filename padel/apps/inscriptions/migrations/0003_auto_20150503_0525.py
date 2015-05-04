# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscriptions', '0002_auto_20150503_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugadorxequipo',
            name='equipo',
            field=models.ForeignKey(to='inscriptions.Equipo'),
            preserve_default=True,
        ),
    ]
