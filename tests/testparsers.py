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
        self.assertEqual(result['usage'][84]['name'], "Shuckle", "85th Pokemon is Shuckle")
        self.assertEqual(result['usage'][84]['rank'], "85", "Rank of Shuckle is 85")
        self.assertEqual(result['usage'][84]['usage_percent'], "1.23560", "Shuckle has 1.23560% usage")
        self.assertEqual(result['total_battles'], "588918", "Total battles is 588918")
        self.assertEqual(result['avg_weight'], "0.015", "Average weight is 0.015")


class MetagameTest(unittest.TestCase):
    def test_parse(self):
        metagame_file = MetagameFile('tests/textfiles/2016-08/metagame/uu-1760.txt')
        metagame_file.parse()
        result = metagame_file.data
        self.assertEqual(result['teams'][0]['type'], "weatherless", "First team is weatherless")
        self.assertEqual(result['teams'][0]['percentage'], "96.57497", "weatherless' usage is 96.57407%")
        self.assertEqual(result['teams'][25]['type'], "sand", "26th team is sand")
        self.assertEqual(result['graph']['lowest'], -2.0, "Graph's lowest is -2.0")
        self.assertEqual(result['graph']['increment'], 0.25, "Graph's increment is 0.25")
        self.assertEqual(result['graph']['characterValue'], 0.44, "Graph's character value is 0.44%")
        self.assertEqual(result['graph']['bars'][0], 1, "Graph's first bar length is 1")
        self.assertEqual(result['graph']['bars'][2], 14, "Graph's third bar length is 14")
        self.assertEqual(len(result['graph']['bars']), 20, "Graph's length is 20")


class MovesetTest(unittest.TestCase):
    def test_parse(self):
        moveset_file = MovesetFile('tests/textfiles/2016-08/moveset/uu-1760.txt')
        moveset_file.parse()
        result = moveset_file.data
        self.assertEqual(result[1]['name'], "Steelix-Mega")
        self.assertEqual(result[1]['raw_count'], 15127)
        self.assertEqual(result[1]['avg_weight'], 0.0193931433493)
        self.assertEqual(result[1]['viability_ceiling'], 88)
        self.assertEqual(result[0]['abilities'][0]['name'], "Pixilate")
        self.assertEqual(result[0]['abilities'][0]['percentage'], 99.652)
        self.assertEqual(result[0]['abilities'][1]['name'], "Cute Charm")
        self.assertEqual(result[0]['abilities'][1]['percentage'], 0.348)
        self.assertEqual(result[0]['items'][0]['name'], "Leftovers")
        self.assertEqual(result[0]['items'][0]['percentage'], 45.327)
        self.assertEqual(result[0]['items'][3]['name'], "Other")
        self.assertEqual(result[0]['items'][3]['percentage'], 1.290)
        self.assertEqual(result[0]['spreads'][0]['is_other'], False)
        self.assertEqual(result[0]['spreads'][0]['nature'], "Modest")
        self.assertEqual(result[0]['spreads'][0]['hp'], 0)
        self.assertEqual(result[0]['spreads'][0]['atk'], 0)
        self.assertEqual(result[0]['spreads'][0]['def'], 0)
        self.assertEqual(result[0]['spreads'][0]['spa'], 252)
        self.assertEqual(result[0]['spreads'][0]['spd'], 4)
        self.assertEqual(result[0]['spreads'][0]['spe'], 252)
        self.assertEqual(result[0]['spreads'][0]['percentage'], 9.452)
        self.assertEqual(result[0]['spreads'][6]['is_other'], True)
        self.assertEqual(result[0]['spreads'][6]['nature'], "Other")
        self.assertEqual(result[0]['spreads'][6]['hp'], None)
        self.assertEqual(result[0]['spreads'][6]['atk'], None)
        self.assertEqual(result[0]['spreads'][6]['def'], None)
        self.assertEqual(result[0]['spreads'][6]['spa'], None)
        self.assertEqual(result[0]['spreads'][6]['spd'], None)
        self.assertEqual(result[0]['spreads'][6]['spe'], None)
        self.assertEqual(result[0]['spreads'][6]['percentage'], 57.668)
        self.assertEqual(result[0]['moves'][0]['name'], "Hyper Voice")
        self.assertEqual(result[0]['moves'][0]['percentage'], 99.466)
        self.assertEqual(result[0]['moves'][11]['name'], "Other")
        self.assertEqual(result[0]['moves'][11]['percentage'], 16.493)
        self.assertEqual(result[0]['teammates'][0]['name'], "Krookodile")
        self.assertEqual(result[0]['teammates'][0]['percentage'], 9.854)
        self.assertEqual(result[0]['teammates'][11]['name'], "Qwilfish")
        self.assertEqual(result[0]['teammates'][11]['percentage'], 2.313)
        self.assertEqual(result[0]['counters'][0]['name'], "Nidoking")
        self.assertEqual(result[0]['counters'][0]['number1'], 72.955)
        self.assertEqual(result[0]['counters'][0]['number2'], 90.57)
        self.assertEqual(result[0]['counters'][0]['number3'], 4.40)
        self.assertEqual(result[0]['counters'][0]['koed'], 28.8)
        self.assertEqual(result[0]['counters'][0]['switched_out'], 61.8)
        self.assertEqual(result[0]['counters'][6]['name'], "Blissey")
        self.assertEqual(result[0]['counters'][6]['number1'], 53.809)
        self.assertEqual(result[0]['counters'][6]['number2'], 69.21)
        self.assertEqual(result[0]['counters'][6]['number3'], 3.85)
        self.assertEqual(result[0]['counters'][6]['koed'], 5.1)
        self.assertEqual(result[0]['counters'][6]['switched_out'], 64.1)


class LeadsTest(unittest.TestCase):
    def test_parse(self):
        leads_file = LeadsFile('tests/textfiles/2016-08/leads/uu-1760.txt')
        leads_file.parse()
        result = leads_file.data
        self.assertEqual(result['usage'][45]['name'], "Shuckle", "46th Pokemon is Shuckle")
        self.assertEqual(result['usage'][45]['rank'], "46", "Rank of Shuckle is 46")
        self.assertEqual(result['usage'][45]['usage_percent'], "0.64718", "Shuckle has 0.64718% usage")
        self.assertEqual(result['total_leads'], "1177836", "Total battles is 1177836")


class ChaosTest(unittest.TestCase):
    def test_parse(self):
        chaos_file = ChaosFile('tests/textfiles/2016-08/chaos/battlespotspecial17-0.json')
        result = chaos_file.parse()
