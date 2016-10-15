#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.parsers.textfile import *


class ChaosFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.file = None

    def parse(self):
        return None # TODO : Implement
