#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random, string
from decimal import Decimal as D
from . import models
from django.test import TestCase
from common.tests import EnvSetUpTestCase


class ProductCategory(EnvSetUpTestCase):
    def setUp(self):
        self.accountSetUp()
        self.productSetUp()
        self.instance = models.ProductCategory.objects.create(name='test')
        models.ProductCategory.objects.bulk_create([
            models.ProductCategory(name=name) for name in ['test1', 'test2', 'test3']
        ])
        self.queryset = models.ProductCategory.objects.all()

    def test_check_states(self):
        self.assertEqual(self.instance.check_states('delete'), False)
        self.assertEqual(self.instance.check_states('no_delete'), True)
        self.assertEqual(self.instance.check_states('active'), True)
        self.assertEqual(self.instance.check_states('no_active'), False)
        self.assertTrue(self.instance.check_states('no_delete','active'))
        self.assertTrue(self.instance.check_states('no_delete','no_active'))
        self.assertTrue(self.instance.check_states('delete','active'))
        self.assertFalse(self.instance.check_states('delete','no_active'))

    def test_set_state(self):
        self.instance.set_state('delete')
        self.assertEqual(self.instance.is_delete, True)
        self.instance.set_state('no_delete')
        self.assertEqual(self.instance.is_delete, False)
        self.instance.set_state('no_active')
        self.assertEqual(self.instance.is_active, False)
        self.instance.set_state('active')
        self.assertEqual(self.instance.is_active, True)

    def test_check_to_set_state(self):
        self.assertEqual(self.instance.check_to_set_state('no_delete', set_state='delete'), True)
        self.assertEqual(self.instance.is_delete, True)
        self.assertEqual(self.instance.check_to_set_state('delete', set_state='no_delete'), True)
        self.assertEqual(self.instance.is_delete, False)
        self.assertEqual(self.instance.check_to_set_state('active', set_state='no_active'), True)
        self.assertEqual(self.instance.is_active, False)
        self.assertEqual(self.instance.check_to_set_state('no_active', set_state='active'), True)
        self.assertEqual(self.instance.is_active, True)

    def test_check_state_queryset(self):
        self.assertEqual(models.ProductCategory.check_state_queryset('delete', self.queryset), False)
        self.assertEqual(models.ProductCategory.check_state_queryset('no_delete', self.queryset), True)

    def test_set_state_queryset(self):
        models.ProductCategory.set_state_queryset('delete', self.queryset)
        self.assertEqual(models.ProductCategory.check_state_queryset('delete', self.queryset), True)
        models.ProductCategory.set_state_queryset('no_delete', self.queryset)
        self.assertEqual(models.ProductCategory.check_state_queryset('no_delete', self.queryset), True)

    def test_check_to_set_state_queryset(self):
        self.assertEqual(models.ProductCategory.check_to_set_state_queryset('no_delete', 'delete', self.queryset), True)
        self.assertEqual(models.ProductCategory.check_to_set_state_queryset('delete', 'no_delete', self.queryset), True)