# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refund', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='order',
            field=models.ForeignKey(related_name='refunds', verbose_name='Order', to='order.Order'),
            preserve_default=True,
        ),
    ]
