#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.parsers.textfile import *


class MovesetFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.file = None
        self.currentPokemon = None
        self.currentLine = None
        self.data = []

    def parse(self):
        with open(self.path, mode='r') as self.file:
            while self.nextLine() != "":
                self.parseLine()
        return self.data

    def nextLine(self):
        self.currentLine = self.file.readline()
        return self.currentLine

    def parseLine(self):
        try:
            self.currentPokemon = {}
            self.parseName()
            self.parseCount()
            self.parseAbilities()
            self.parseItems()
            self.parseSpreads()
            self.parseMoves()
            self.parseTeammates()
            self.parseCounters()
            self.data.append(self.currentPokemon)
        except AttributeError: # Halt execution if file is incomplete. e.g. /stats/2015-07/moveset/anythinggoes-1630.txt
            if self.currentLine is None or self.currentLine == "":
                return


    def parseName(self):
        self.currentPokemon['name'] = self.nextLine().split('|')[1].strip()  # ' | Skarmory | '
        pass

    def parseCount(self):
        self.nextLine()  # '+----+'
        while "+--" not in self.nextLine():
            if "Raw count: " in self.currentLine:
                self.currentPokemon['raw_count'] = int(
                    self.currentLine.split('|')[1].strip().split(': ')[1])  # ' | Raw count: 4 |  '
            elif "Avg. weight: " in self.currentLine:
                if "---" not in self.currentLine:
                    self.currentPokemon['avg_weight'] = float(
                        self.currentLine.split('|')[1].strip().split(': ')[1])  # ' | Avg. weight: 0.4 |  '
            elif "Viability Ceiling:" in self.currentLine:
                self.currentPokemon['viability_ceiling'] = int(
                    self.currentLine.split('|')[1].strip().split(': ')[1])  # ' | Viability Ceiling: 4 |  '
            else:
                raise RuntimeError('Line not recognized : ' + self.currentLine)

    def parseAbilities(self):
        self.nextLine()  # '+----+'
        self.nextLine()  # ' | Abilities | '
        self.currentPokemon['abilities'] = []
        while "+--" not in self.currentLine:
            ability = {}
            matches = re.search('^ \| ([^|]+) +(-?[\d.]+)%', self.currentLine)  # ' | Gale Wings 67.393% | '
            ability['name'] = matches.groups()[0].strip()
            ability['percentage'] = float(matches.groups()[1])
            self.currentPokemon['abilities'].append(ability)
            self.nextLine()

    def parseItems(self):
        self.nextLine()  # ' | Items | '
        self.currentPokemon['items'] = []
        while "+--" not in self.nextLine():
            item = {}
            matches = re.search('^ \| ([^|]+) +(-?[\d.]+)%', self.currentLine)  # ' | Rocky Helmet 16.875% | '
            item['name'] = matches.groups()[0].strip()
            item['percentage'] = float(matches.groups()[1])
            self.currentPokemon['items'].append(item)

    def parseSpreads(self):
        self.nextLine()  # ' | Spreads | '
        self.currentPokemon['spreads'] = []
        while "+--" not in self.nextLine():
            spread = {}
            matches = re.search('^ \| (?:(\w+):(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)|(Other)) +(-?[\d.]+)%',
                                self.currentLine)  # ' | Timid:0/0/0/252/4/252 58.111% | '
            if matches.groups()[7] == "Other":
                spread['is_other'] = True
                spread['nature'] = "Other"
                spread['hp'] = None
                spread['atk'] = None
                spread['def'] = None
                spread['spa'] = None
                spread['spd'] = None
                spread['spe'] = None
            else:
                spread['is_other'] = False
                spread['nature'] = matches.groups()[0].strip()
                spread['hp'] = int(matches.groups()[1])
                spread['atk'] = int(matches.groups()[2])
                spread['def'] = int(matches.groups()[3])
                spread['spa'] = int(matches.groups()[4])
                spread['spd'] = int(matches.groups()[5])
                spread['spe'] = int(matches.groups()[6])
            spread['percentage'] = float(matches.groups()[8])
            self.currentPokemon['spreads'].append(spread)

    def parseMoves(self):
        self.nextLine()  # ' | Moves | '
        self.currentPokemon['moves'] = []
        while "+--" not in self.nextLine():
            move = {}
            matches = re.search('^ \| ([^|]+) +(-?[\d.]+)%', self.currentLine)  # ' | Brave Bird 99.882% | '
            move['name'] = matches.groups()[0].strip()
            move['percentage'] = float(matches.groups()[1])
            self.currentPokemon['moves'].append(move)

    def parseTeammates(self):
        self.nextLine()  # ' | Teammates | '
        self.currentPokemon['teammates'] = []
        while "+--" not in self.nextLine():
            mate = {}
            matches = re.search('^ \| ([^|]+) +([+-]?[\d.]+)%', self.currentLine)  # ' | Meloetta +15.409% | '
            mate['name'] = matches.groups()[0].strip()
            mate['percentage'] = float(matches.groups()[1])
            self.currentPokemon['teammates'].append(mate)

    def parseCounters(self):
        self.nextLine()  # ' | Checks and Counters | '
        self.currentPokemon['counters'] = []
        while "+--" not in self.nextLine():
            counter = {}
            matches = re.search('^ \| ([^|]+) ([\d.]+) \(([\d.]+)\D+([\d.]+)\)',
                                self.currentLine)  # ' | Trubbish 75.535 (86.41±2.72) | '
            counter['name'] = matches.groups()[0].strip()
            counter['number1'] = float(matches.groups()[1])
            counter['number2'] = float(matches.groups()[2])
            counter['number3'] = float(matches.groups()[3])
            matches2 = re.search('^ \|\s+\(([\d.]+)%.+/\s+(-?[\d.]+)%',
                                 self.nextLine())  # ' | (28.9% KOed / 47.3% switched out)| '
            counter['koed'] = float(matches2.groups()[0])
            counter['switched_out'] = float(matches2.groups()[1])
            self.currentPokemon['counters'].append(counter)
