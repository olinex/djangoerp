# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-14 10:56
from __future__ import unicode_literals

from django.db import migrations
import djangoperm.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170514_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=djangoperm.db.fields.CharField(default='zh-han', help_text='用户设置的默认语言', max_length=20, null=True, perms={'read': False, 'write': False}, verbose_name='语言'),
        ),
    ]
