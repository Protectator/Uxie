#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.parsers.textfile import *


class MetagameFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.file = None
        self.currentLine = None
        self.data = {}

    def parse(self):
        with open(self.path, mode='r') as self.file:
            while self.nextLine() != "":
                self.parseLine()
        return self.data

    def nextLine(self):
        self.currentLine = self.file.readline()
        return self.currentLine

    def parseLine(self):
        if "Stalliness" and "mean" in self.currentLine:
            self.parseStalliness()
        elif "%" in self.currentLine:
            self.parseTeam()
        else:
            return

    def parseStalliness(self):
        graph = {}
        matches = re.search('mean: *(-?[\d.]+)', self.currentLine)  # ' Stalliness (mean:  0.105)'
        graph['mean'] = matches.groups()[0]
        self.parseGraph()

    def parseGraph(self):
        graph = {}
        firstNumber = None
        secondNumber = None
        firstNumberLine = None
        secondNumberLine = None
        nbLines = 0
        graph['bars'] = []
        while "|" in self.nextLine():  # ' -2.0|###'
            number = self.currentLine.split('|')[0].strip()
            if firstNumber == None and number != "":
                if number[0] == '+':
                    number = number[1:]
                firstNumber = float(number)
                firstNumberLine = nbLines
            elif secondNumber == None and number != "":
                if number[0] == '+':
                    number = number[1:]
                secondNumber = float(number)
                secondNumberLine = nbLines
            graph['bars'].append(self.currentLine.count('#'))
            nbLines += 1
        graph['increment'] = (secondNumber - firstNumber) / float(secondNumberLine - firstNumberLine)
        graph['lowest'] = firstNumber - firstNumberLine * graph['increment']
        matches = re.search('=\s+([\d.]+)\s?%', self.nextLine())  # ' one # =  0.68%'
        graph['characterValue'] = matches.groups()[0]
        self.data['graph'] = graph

    def parseTeam(self):
        self.data['teams'] = []
        while "%" in self.nextLine():
            team = {}
            matches = re.search('(\w+)\.*\s?(\d[\d.]+)', self.currentLine)  # ' semistall..................... 5.39178%'
            team['type'] = matches.groups()[0]
            team['percentage'] = matches.groups()[1]
            self.data['teams'].append(team)
