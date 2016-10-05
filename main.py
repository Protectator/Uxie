#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.parsers.metagame import *
# Fill DB

# Execute
# crawler = Crawler('')
# crawler.run()
# parser = Parser()
# page = UsageFile('stats/2014-11/350cup-0.txt')
# page.parse()
# page = MovesetFile('stats/2016-06/moveset/lc-1500.txt')
# page.parse()
page =  MetagameFile('stats/2014-11/metagame/battlespotspecial7-0.txt')
page.parse()
'''
db = MySQL()
db.connect()
db.initialize()
db.fillUsage(page)'''
print page.data
