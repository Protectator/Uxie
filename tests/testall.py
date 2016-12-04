#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import unittest
import os

class ExecutionTest(unittest.TestCase):
    def test_exec(self):
        print("Testing a simple execution...")
        os.system("python uxie.py mysql localhost uxie uxie uxie -y 2014 -m 12 -t usage moveset metagame leads -g 0 -f uu nu")
