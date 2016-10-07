#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import sys
import redgreenunittest as unittest
from tests.testparsers import UsageTest, MetagameTest, MovesetTest

def suite():
    return unittest.TestSuite((
        unittest.makeSuite(UsageTest),
        unittest.makeSuite(MetagameTest),
        unittest.makeSuite(MovesetTest)
    ))

if __name__ == '__main__':
    ret = not unittest.TextTestRunner(verbosity=2).run(suite()).wasSuccessful()
    sys.exit(ret)