#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import os

from src.databases.mysql import *
from src.parsers.usage import *
from src.parsers.leads import *
from src.parsers.metagame import *
from src.parsers.moveset import *
from src.parsers.chaos import *

class Feeder():

    def __init__(self, baseFolder):
        self.folder = baseFolder

    def feedAll(self, dbms, host, user, password, dbname):
        # Phase 3 : Fill DB
        print "Connecting to database"
        db = MySQL()
        db.connect(host, user, password, dbname)
        print "Initializing tables"
        db.initialize()
        print "Parsing files"
        for root, dirs, files in os.walk("stats", topdown=False):
            for filePath in files:
                path = "/".join(os.path.join(root, filePath).split(os.sep))
                if os.path.getsize(path) == 0:
                    continue
                file = TextPage(path)
                print "Parsing file " + path
                type = file.folders
                if type is None:
                    parser = UsageFile(path)
                    parser.parse()
                    db.fillUsage(parser)
                elif "leads" in type:
                    parser = LeadsFile(path)
                    parser.parse()
                    db.fillLeads(parser)
                elif "metagame" in type:
                    parser = MetagameFile(path)
                    parser.parse()
                    db.fillMetagame(parser)
                elif "moveset" in type:
                    parser = MovesetFile(path)
                    parser.parse()
                    db.fillMoveset(parser)
                elif "chaos" in type:
                    parser = ChaosFile(path)
                    parser.parse()
                    db.fillChaos(parser)
                else:
                    if type == "mega":
                        continue
                    parser = UsageFile(path)
                    parser.parse()
                    db.fillUsage(parser)
