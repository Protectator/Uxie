#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016-2017 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import unittest

from src.databases.mysql.mysql import MySQL

class MysqlTest(unittest.TestCase):
    def test_db(self):
        print("Testing MySQL initialize...")
        db = MySQL()
        db.connect('localhost', 'uxie', 'uxie', 'uxie')
        db.initialize()
