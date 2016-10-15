#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import sys


class ProgressBar:
    def __init__(self, maxProgress):
        self.progress = 0
        self.unit = 'Mo'
        self.divider = 1024 * 1024
        self.length = 60
        self.max = maxProgress
        self.up = '█'
        self.down = '.'
        self.prefix = "Downloaded: "

    def update(self, progress, size):
        if progress > self.max:
            progress = self.max
        ups = int(progress * self.length / self.max)
        downs = self.length - ups
        perc = 100 * progress / self.max
        finalSize = int(size / self.divider)
        if ups > 0:
            sys.stdout.write("\r%s[%s%s] (%i%%) %i/%i [%i %s]" % (
                self.prefix, self.up * ups, self.down * downs, perc, progress, self.max, finalSize, self.unit))
        sys.stdout.flush()
        if progress == self.max:
            sys.stdout.write("\n")
            sys.stdout.flush()
