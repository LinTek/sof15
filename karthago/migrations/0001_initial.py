# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('constellation', models.CharField(help_text='E.g. <em>MPiRE</em>, <em>Grabbarna Grus</em>', max_length=256, verbose_name='constellation')),
                ('name', models.CharField(max_length=256, verbose_name='entry name')),
                ('members', models.PositiveIntegerField(default=10, verbose_name='number of members')),
                ('primary_contact_name', models.CharField(max_length=256, verbose_name='name')),
                ('primary_contact_address', models.CharField(max_length=256, verbose_name='address')),
                ('primary_contact_postcode', models.CharField(max_length=6, verbose_name='postcode')),
                ('primary_contact_city', models.CharField(max_length=64, verbose_name='city')),
                ('primary_contact_phone', models.CharField(max_length=256, verbose_name='phone')),
                ('primary_contact_email', models.EmailField(max_length=75, verbose_name='email')),
                ('secondary_contact_name', models.CharField(max_length=256, verbose_name='name')),
                ('secondary_contact_address', models.CharField(max_length=256, verbose_name='address')),
                ('secondary_contact_postcode', models.CharField(max_length=6, verbose_name='postcode')),
                ('secondary_contact_city', models.CharField(max_length=64, verbose_name='city')),
                ('secondary_contact_phone', models.CharField(max_length=256, verbose_name='phone')),
                ('secondary_contact_email', models.EmailField(max_length=75, verbose_name='email')),
                ('width', models.DecimalField(decimal_places=2, max_digits=4, blank=True, help_text='Width in meters, in direction of movement.', null=True, verbose_name='width')),
                ('length', models.DecimalField(decimal_places=2, max_digits=4, blank=True, help_text='Length in meters, in direction of movement.', null=True, verbose_name='length')),
                ('height', models.DecimalField(decimal_places=2, max_digits=4, blank=True, help_text='Height in meters.', null=True, verbose_name='height')),
                ('description', models.TextField(help_text='Describe your idea! Maximum 500 words.', verbose_name='description')),
                ('spex_description', models.TextField(help_text='Describe what will happen in, on and around your carriage! Music, theatre or anything else amusing? Maximum 500 words.', verbose_name='spex description')),
                ('other_information', models.TextField(help_text='Want us to know something else?', null=True, verbose_name='other information', blank=True)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'entry',
                'verbose_name_plural': 'entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryCustomMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('material', models.CharField(max_length=256, verbose_name='material')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=9, decimal_places=3)),
                ('unit', models.CharField(max_length=8, verbose_name='unit')),
                ('entry', models.ForeignKey(verbose_name='entry', to='karthago.Entry')),
            ],
            options={
                'verbose_name': 'entry custom material',
                'verbose_name_plural': 'entry custom materials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=9, decimal_places=3)),
                ('entry', models.ForeignKey(verbose_name='entry', to='karthago.Entry')),
            ],
            options={
                'ordering': ('entry', 'material', 'role'),
                'verbose_name': 'entry material',
                'verbose_name_plural': 'entry materials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.CharField(max_length=256, verbose_name='description')),
                ('max_members', models.PositiveIntegerField(verbose_name='max members')),
            ],
            options={
                'ordering': ('max_members', 'name'),
                'verbose_name': 'entry type',
                'verbose_name_plural': 'entry types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256, verbose_name='name')),
                ('unit', models.CharField(max_length=16, verbose_name='unit')),
            ],
            options={
                'ordering': ('-name',),
                'verbose_name': 'material',
                'verbose_name_plural': 'materials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaterialRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
                'verbose_name': 'material role',
                'verbose_name_plural': 'material roles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entrymaterial',
            name='material',
            field=models.ForeignKey(verbose_name='material', to='karthago.Material'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entrymaterial',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='karthago.MaterialRole'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entrycustommaterial',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='karthago.MaterialRole'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='entry_type',
            field=models.ForeignKey(related_name='entries', verbose_name='entry type', to='karthago.EntryType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='materials',
            field=models.ManyToManyField(to='karthago.Material', through='karthago.EntryMaterial'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('constellation', 'name')]),
        ),
    ]
