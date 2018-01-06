#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@author:    olinex
@time:      2017/8/24 下午2:30
"""

__all__ = ['md5_hexdigest']

import json
from hashlib import md5
from django.core.serializers.json import DjangoJSONEncoder


def md5_hexdigest(object):
    """
    automatically change object to json md5 string
    :param object: float/inter/string/list/tuple/set/dict
    :return: string
    """
    m = md5()
    m.update(json.dumps(object, cls=DjangoJSONEncoder,sort_keys=True).encode(('utf8')))
    return m.hexdigest()
