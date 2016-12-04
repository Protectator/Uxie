#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import re
import os


class TextPage:
    def __init__(self, path, size = 0):
        self.path = path
        matchs = re.search('(\d+)-(\d+)(?:/?([^/]+)){0,2}/([^/]+)-(\d+)\.(\w+)', path)
        if not matchs:
            path = os.path.normpath(path)
            matchs = re.search('(\d+)-(\d+)(?:/?([^/]+)){0,2}/([^/]+)-(\d+)\.(\w+)', path)
        if not matchs:
            matchs = re.search('(\d+)-(\d+)(?:\\\\?([^\\\]+)){0,2}\\\\([^\\\]+)-(\d+)\.(\w+)', path)
        if not matchs:
            raise RuntimeError('Invalid path specified :' + path)
        self.year = int(matchs.groups()[0])
        self.month = int(matchs.groups()[1])
        self.folders = (matchs.groups()[2])
        self.meta = (matchs.groups()[3])
        self.elo = int(matchs.groups()[4])
        self.fileFormat = (matchs.groups()[5])
        self.size = size
        self.localPath = "/%(year)s-%(month)s/%(folders)s/%(meta)s-%(elo)s.%(fileFormat)s" % {
            'year' : self.year,
            'month' : self.month if self.month > 10 else '0' + str(self.month),
            'folders' : self.folders if self.folders is not None else "",
            'meta' : self.meta,
            'elo' : self.elo,
            'fileFormat' : self.fileFormat
        }
