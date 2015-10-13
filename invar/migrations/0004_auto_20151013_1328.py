# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0003_auto_20150918_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('pk',), 'verbose_name': 'invoice', 'verbose_name_plural': 'invoices', 'permissions': [['view_economic_report', 'Can view economic report']]},
        ),
    ]
