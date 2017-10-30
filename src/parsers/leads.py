#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016-2017 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.parsers.textfile import *


class LeadsFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.file = None
        self.currentLine = None
        self.data = {}
        self.data['usage'] = []

    def parse(self):
        with open(self.path, mode='r') as self.file:
            while self.nextLine() != "":
                self.parseLine()
        return self.data

    def nextLine(self):
        self.currentLine = self.file.readline()
        return self.currentLine

    def parseLine(self):
        if "Total leads:" in self.currentLine:
            self.data['total_leads'] = self.currentLine.split(': ')[1].strip()
            return
        elif "----" in self.currentLine:
            return
        elif " | " in self.currentLine:
            fields = [field.strip() for field in self.currentLine.split('|')[1:8]]
            if fields[0] != "Rank":
                pokemon = {}
                pokemon['rank'] = fields[0]
                pokemon['name'] = fields[1]
                pokemon['usage_percent'] = fields[2][:-1]
                pokemon['raw_number'] = fields[3]
                pokemon['raw_percent'] = fields[4][:-1]
                self.data['usage'].append(pokemon)
