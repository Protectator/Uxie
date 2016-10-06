#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import redgreenunittest as unittest
from tests.testparsers import UsageTest

def suite():
    return unittest.TestSuite((
        unittest.makeSuite(UsageTest)
    ))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())