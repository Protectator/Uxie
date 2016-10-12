#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
from src.databases.mysql import *
from src.parsers.usage import *
from src.parsers.leads import *
from src.parsers.metagame import *
from src.parsers.moveset import *
# Fill DB

# Execute
# crawler = Crawler('')
# crawler.run()
# parser = Parser()
# page = UsageFile('stats/2014-11/350cup-0.txt')
# page.parse()
# page = MovesetFile('stats/2016-06/moveset/lc-1500.txt')
# page.parse()

# page = UsageFile('stats/2016-08/uu-0.txt')
# page.parse()
# page = LeadsFile('stats/2016-08/leads/uu-0.txt')
# page.parse()
# page = MetagameFile('stats/2016-08/metagame/uu-0.txt')
# page.parse()
page = MovesetFile('stats/2016-08/moveset/uu-0.txt')
page.parse()

db = MySQL()
db.connect()
db.initialize()
db.fillMoveset(page)
