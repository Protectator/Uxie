#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import re


class TextPage:
    def __init__(self, path):
        self.path = path
        matchs = re.search('(\d+)-(\d+)(?:/?([^/]+)){0,2}/([^/]+)-(\d+)\.(\w+)', path)
        self.year = (matchs.groups()[0])
        self.month = (matchs.groups()[1])
        self.folders = (matchs.groups()[2])
        self.meta = (matchs.groups()[3])
        self.elo = (matchs.groups()[4])
        self.fileFormat = (matchs.groups()[5])
