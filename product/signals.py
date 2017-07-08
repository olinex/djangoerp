#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from . import models
from hashlib import md5
from django.db import transaction
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save, m2m_changed
from django.core.serializers.json import DjangoJSONEncoder


@receiver(m2m_changed, sender=models.ProductTemplate.attributes.through)
def change_product_template_attribute(sender, instance, **kwargs):
    '''创建产品模板时,自动创建所有的'''
    if not kwargs.get('reverse') and kwargs.get('action') in ('post_add', 'post_remove'):
        instance.sync_create_products()


@receiver(post_save, sender=models.Product)
def create_attribute_md5(sender, instance, created, **kwargs):
    '''保存时,更新产品属性的md5值'''
    if not created:
        m = md5()
        m.update(json.dumps(instance.attributes, cls=DjangoJSONEncoder).encode('utf8'))
        instance.attributes_md5 = m.hexdigest()
