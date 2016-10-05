#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from textfile import *


class UsageFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.data = []

    def parse(self):
        with open(self.path, mode='r') as usageFile:
            for line in usageFile:
                self.parseLine(line)
        return self.data

    def parseLine(self, line):
        if line[0:15] == "Total battles: ":
            return
        elif line[0:19] == " Avg. weight/team: ":
            return
        elif line[0:2] == " +":
            return
        elif line[0:2] == " |":
            fields = [field.strip() for field in line.split('|')[1:8]]
            if fields[0] != "Rank":
                fields[2] = fields[2][:-1]
                fields[4] = fields[4][:-1]
                fields[6] = fields[6][:-1]
                self.data.append(fields)