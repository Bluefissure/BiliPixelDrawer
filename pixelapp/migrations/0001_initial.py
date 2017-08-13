# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pixel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('color', models.IntegerField(default=0)),
                ('updtime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=64, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('project', models.ForeignKey(related_name='token', to='pixelapp.Project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('nickname', models.CharField(default=b'Anonymous', max_length=64, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(related_name='token', to='pixelapp.User'),
        ),
        migrations.AddField(
            model_name='pixel',
            name='finuser',
            field=models.ForeignKey(related_name='pixel', to='pixelapp.User'),
        ),
        migrations.AddField(
            model_name='pixel',
            name='project',
            field=models.ForeignKey(related_name='pixel', to='pixelapp.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='pixel',
            unique_together=set([('project', 'x', 'y')]),
        ),
    ]
