# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150503_0443'),
        ('torneos', '0008_auto_20150422_0403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('preferencia_horaria', models.TextField(max_length=50, null=True, blank=True)),
                ('nivel', models.IntegerField(null=True, blank=True)),
                ('pagado', models.BooleanField(default=False)),
                ('timpestamp', models.DateField(auto_now_add=True)),
                ('activo', models.BooleanField(default=False)),
                ('nombre_club', models.CharField(max_length=200, null=True)),
                ('ubicacion_sede', models.CharField(max_length=200, null=True)),
                ('localidad', models.CharField(max_length=100, null=True)),
                ('dia_juego', models.CharField(max_length=10, null=True)),
                ('hora_juego', models.CharField(max_length=5, null=True)),
                ('categoria', models.ForeignKey(to='torneos.Categoria', null=True)),
                ('competicion', models.ForeignKey(to='torneos.Competicion')),
                ('division', models.ForeignKey(to='torneos.Division', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JugadorxEquipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capitan', models.BooleanField(default=b'False')),
                ('activo', models.BooleanField(default=b'False')),
                ('lesionado', models.BooleanField(default=False)),
                ('timpestamp', models.DateTimeField(auto_now=True)),
                ('equipo', models.ForeignKey(related_name='Equipo(JugadorxEquipo)', to='inscriptions.Equipo')),
                ('jugador', models.ForeignKey(to='users.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='equipo',
            name='jugadores',
            field=models.ManyToManyField(to='users.Player', through='inscriptions.JugadorxEquipo'),
            preserve_default=True,
        ),
    ]
