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
