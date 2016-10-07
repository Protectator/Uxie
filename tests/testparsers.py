#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import unittest
from src.parsers.usage import UsageFile
from src.parsers.metagame import MetagameFile
from src.parsers.moveset import MovesetFile
from src.parsers.leads import LeadsFile
from src.parsers.chaos import ChaosFile

class UsageTest(unittest.TestCase):
    def test_parse(self):
        usage_file = UsageFile('tests/textfiles/2016-08/uu-1760.txt')
        usage_file.parse()
        result = usage_file.data
        self.assertEquals(result['usage'][84]['name'], "Shuckle", "85th Pokemon is Shuckle")
        self.assertEquals(result['usage'][84]['rank'], "85", "Rank of Shuckle is 85")
        self.assertEquals(result['usage'][84]['usage_percent'], "1.23560", "Shuckle has 1.23560% usage")
        self.assertEquals(result['total_battles'], "588918", "Total battles is 588918")
        self.assertEquals(result['avg_weight'], "0.015", "Average weight is 0.015")


class MetagameTest(unittest.TestCase):
    def test_parse(self):
        metagame_file = MetagameFile('tests/textfiles/2016-08/metagame/uu-1760.txt')
        metagame_file.parse()
        result = metagame_file.data
        self.assertEquals(result['teams'][0]['type'], "weatherless", "First team is weatherless")
        self.assertEquals(result['teams'][0]['percentage'], "96.57497", "weatherless' usage is 96.57407%")
        self.assertEquals(result['teams'][25]['type'], "sand", "26th team is sand")
        self.assertEquals(result['graph']['lowest'], -2.0, "Graph's lowest is -2.0")
        self.assertEquals(result['graph']['increment'], 0.25, "Graph's increment is 0.25")
        self.assertEquals(result['graph']['characterValue'], 0.44, "Graph's character value is 0.44%")
        self.assertEquals(result['graph']['bars'][0], 1, "Graph's first bar length is 1")
        self.assertEquals(result['graph']['bars'][2], 14, "Graph's third bar length is 14")
        self.assertEquals(len(result['graph']['bars']), 20, "Graph's length is 20")


class MovesetTest(unittest.TestCase):
    def test_parse(self):
        moveset_file = MovesetFile('tests/textfiles/2016-08/moveset/uu-1760.txt')
        moveset_file.parse()
        result = moveset_file.data
        self.assertEquals(result[1]['name'], "Steelix-Mega")
        self.assertEquals(result[1]['raw_count'], 15127)
        self.assertEquals(result[1]['avg_weight'], 0.0193931433493)
        self.assertEquals(result[1]['viability_ceiling'], 88)
        self.assertEquals(result[0]['abilities'][0]['name'], "Pixilate")
        self.assertEquals(result[0]['abilities'][0]['percentage'], 99.652)
        self.assertEquals(result[0]['abilities'][1]['name'], "Cute Charm")
        self.assertEquals(result[0]['abilities'][1]['percentage'], 0.348)
        self.assertEquals(result[0]['items'][0]['name'], "Leftovers")
        self.assertEquals(result[0]['items'][0]['percentage'], 45.327)
        self.assertEquals(result[0]['items'][3]['name'], "Other")
        self.assertEquals(result[0]['items'][3]['percentage'], 1.290)
        self.assertEquals(result[0]['spreads'][0]['is_other'], False)
        self.assertEquals(result[0]['spreads'][0]['nature'], "Modest")
        self.assertEquals(result[0]['spreads'][0]['hp'], 0)
        self.assertEquals(result[0]['spreads'][0]['atk'], 0)
        self.assertEquals(result[0]['spreads'][0]['def'], 0)
        self.assertEquals(result[0]['spreads'][0]['spa'], 252)
        self.assertEquals(result[0]['spreads'][0]['spd'], 4)
        self.assertEquals(result[0]['spreads'][0]['spe'], 252)
        self.assertEquals(result[0]['spreads'][0]['percentage'], 9.452)
        self.assertEquals(result[0]['spreads'][6]['is_other'], True)
        self.assertEquals(result[0]['spreads'][6]['nature'], "Other")
        self.assertEquals(result[0]['spreads'][6]['hp'], None)
        self.assertEquals(result[0]['spreads'][6]['atk'], None)
        self.assertEquals(result[0]['spreads'][6]['def'], None)
        self.assertEquals(result[0]['spreads'][6]['spa'], None)
        self.assertEquals(result[0]['spreads'][6]['spd'], None)
        self.assertEquals(result[0]['spreads'][6]['spe'], None)
        self.assertEquals(result[0]['spreads'][6]['percentage'], 57.668)
        self.assertEquals(result[0]['moves'][0]['name'], "Hyper Voice")
        self.assertEquals(result[0]['moves'][0]['percentage'], 99.466)
        self.assertEquals(result[0]['moves'][11]['name'], "Other")
        self.assertEquals(result[0]['moves'][11]['percentage'], 16.493)
        self.assertEquals(result[0]['teammates'][0]['name'], "Krookodile")
        self.assertEquals(result[0]['teammates'][0]['percentage'], 9.854)
        self.assertEquals(result[0]['teammates'][11]['name'], "Qwilfish")
        self.assertEquals(result[0]['teammates'][11]['percentage'], 2.313)
        self.assertEquals(result[0]['counters'][0]['name'], "Nidoking")
        self.assertEquals(result[0]['counters'][0]['number1'], 72.955)
        self.assertEquals(result[0]['counters'][0]['number2'], 90.57)
        self.assertEquals(result[0]['counters'][0]['number3'], 4.40)
        self.assertEquals(result[0]['counters'][0]['koed'], 28.8)
        self.assertEquals(result[0]['counters'][0]['switched_out'], 61.8)
        self.assertEquals(result[0]['counters'][6]['name'], "Blissey")
        self.assertEquals(result[0]['counters'][6]['number1'], 53.809)
        self.assertEquals(result[0]['counters'][6]['number2'], 69.21)
        self.assertEquals(result[0]['counters'][6]['number3'], 3.85)
        self.assertEquals(result[0]['counters'][6]['koed'], 5.1)
        self.assertEquals(result[0]['counters'][6]['switched_out'], 64.1)


class LeadsTest(unittest.TestCase):
    def test_parse(self):
        leads_file = LeadsFile('tests/textfiles/2016-08/leads/uu-1760.txt')
        leads_file.parse()
        result = leads_file.data
        self.assertEquals(result['usage'][45]['name'], "Shuckle", "46th Pokemon is Shuckle")
        self.assertEquals(result['usage'][45]['rank'], "46", "Rank of Shuckle is 46")
        self.assertEquals(result['usage'][45]['usage_percent'], "0.64718", "Shuckle has 0.64718% usage")
        self.assertEquals(result['total_leads'], "1177836", "Total battles is 1177836")


class ChaosTest(unittest.TestCase):
    def test_parse(self):
        pass