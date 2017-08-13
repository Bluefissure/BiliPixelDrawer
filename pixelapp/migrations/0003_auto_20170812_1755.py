# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixelapp', '0002_auto_20170812_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pixel',
            name='finuser',
            field=models.ForeignKey(related_name='pixel', to='pixelapp.User', null=True),
        ),
    ]
