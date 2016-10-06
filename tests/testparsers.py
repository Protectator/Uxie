#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import unittest
from src.parsers.usage import UsageFile

class UsageTest(unittest.TestCase):
    def test_parse(self):
        usage_file = UsageFile('tests/textfiles/2016-08/uu-1760.txt')
        usage_file.parse()
        obtained = usage_file.data['usage']
        self.assertEquals(obtained[84]['name'], "Shuckle")