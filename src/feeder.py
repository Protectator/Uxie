#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import os
import logging

from src.databases.mysql.mysql import *
from src.parsers.chaos import *
from src.parsers.leads import *
from src.parsers.metagame import *
from src.parsers.moveset import *
from src.parsers.usage import *
from src import utils


class Feeder:
    def __init__(self, baseFolder, dbms, host, user, password, dbname, filters):
        self.folder = baseFolder
        self.db = MySQL()
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.filters = filters
        self.log = logging.getLogger('main')

    def feedAll(self):
        # Phase 3 : Fill DB
        self.log.info("Connecting to database")
        self.db.connect(self.host, self.user, self.password, self.dbname)
        self.log.info("Initializing tables")
        self.db.initialize()
        self.log.info("Parsing files")
        for root, dirs, files in os.walk(self.folder, topdown=False):
            for filePath in files:
                path = "/".join(os.path.join(root, filePath).split(os.sep))
                if os.path.getsize(path) == 0:
                    continue
                file = TextPage(path)
                if utils.filter(file, self.filters):
                    self.log.info("Parsing file " + path)
                    fileType = file.folders
                    if fileType is None:
                        parser = UsageFile(path)
                        parser.parse()
                        self.db.fillUsage(parser)
                    elif "leads" in fileType:
                        parser = LeadsFile(path)
                        parser.parse()
                        self.db.fillLeads(parser)
                    elif "metagame" in fileType:
                        parser = MetagameFile(path)
                        parser.parse()
                        self.db.fillMetagame(parser)
                    elif "moveset" in fileType:
                        parser = MovesetFile(path)
                        parser.parse()
                        self.db.fillMoveset(parser)
                    elif "chaos" in fileType:
                        parser = ChaosFile(path)
                        parser.parse()
                        self.db.fillChaos(parser)
                    else:
                        if fileType == "mega":
                            continue
                        parser = UsageFile(path)
                        parser.parse()
                        self.db.fillUsage(parser)

    def postInsert(self):
        self.log.info("Creating Index")
        self.db.connect(self.host, self.user, self.password, self.dbname)
        self.db.postInsert()
