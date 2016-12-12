#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import logging
import threading

from src.databases.mysql.mysql import *
from src.parsers.chaos import *
from src.parsers.leads import *
from src.parsers.metagame import *
from src.parsers.moveset import *
from src.parsers.usage import *
from src.constants import *
from src import utils
from tqdm import tqdm

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


# Decorator
def synchronized(method):
    def new_method(self, *arg, **kws):
        with self.lock:
            return method(self, *arg, **kws)

    return new_method


class Feeder:
    lock = threading.RLock()

    def __init__(self, baseFolder, dbms, host, user, password, dbname, filters):
        self.folder = baseFolder if baseFolder is not None else FOLDER_TO_SAVE
        self.feederDb = MySQL()
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.filters = filters
        self.toParse = Queue()
        self.log = logging.getLogger('main')

    def feedAll(self):
        # Phase 3 : Fill DB
        self.log.info("Connecting to database")
        self.feederDb.connect(self.host, self.user, self.password, self.dbname)
        self.log.info("Initializing tables")
        self.feederDb.initialize()
        self.log.info("Filtering local files")

        # Count files
        nbFiles = 0
        for root, dirs, files in os.walk(self.folder, topdown=False):
            for filePath in files:
                path = "/".join(os.path.join(root, filePath).split(os.sep))
                if os.path.getsize(path) == 0:
                    continue
                file = TextPage(path)
                if utils.filter(file, self.filters):
                    if file.folders:
                        if "/mega/" not in file.path:
                            self.toParse.put(file)
                            nbFiles += 1
                    else:
                        self.toParse.put(file)
                        nbFiles += 1


        # Parse them
        self.log.info("Parsing files")
        self.progressbar = tqdm(total=nbFiles, unit='file', dynamic_ncols=True, maxinterval=1,
                                mininterval=0.1, smoothing=0.05)
        self.progressbar.update(0)
        self.runningThreads = Queue()
        for i in range(DATABASE_THREADS):
            self.runningThreads.put(i)
            t = FeederWorker(self, i, self.toParse, self.runningThreads)
            t.setDaemon(True)
            t.start()
        self.runningThreads.join()
        self.progressbar.close()

    def postInsert(self):
        self.log.info("Creating Index")
        self.feederDb.connect(self.host, self.user, self.password, self.dbname)
        self.feederDb.postInsert()

    @synchronized
    def nextPage(self):
        try:
            next = self.toParse.get(False)
            return next
        except Empty:
            return None

class FeederWorker(threading.Thread):
    def __init__(self, feeder, tId, queue, runningThreads):
        threading.Thread.__init__(self)
        self.feeder = feeder
        self.db = MySQL()
        self.tId = tId
        self.queue = queue
        self.runningThreads = runningThreads
        self.log = logging.getLogger('main')
        self.name = "feederworker_" + str(tId)

    def run(self):
        self.log.debug("Starting " + self.name)
        self.db.connect(self.feeder.host, self.feeder.user, self.feeder.password, self.feeder.dbname)
        page = self.feeder.nextPage()
        while (page is not None):
            self.log.debug(self.name + " starting to parse " + page.path)
            path = "/".join(os.path.join(self.feeder.folder, page.localPath[1:]).split(os.sep))
            file = TextPage(path)
            if utils.filter(file, self.feeder.filters):
                self.log.debug("Parsing file " + path)
                fileType = file.folders
                try:
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
                            self.feeder.progressbar.update(1)
                            page = self.feeder.nextPage()
                            continue
                        parser = UsageFile(path)
                        parser.parse()
                        self.db.fillUsage(parser)
                except (pymysql.err.IntegrityError) as e:
                    if (e.args[0] == 1062 and "monotype" in file.meta and file.year == 2014 and file.month == 12):
                        pass # Known issue. 2014-12 contains twice every monotype entry. It's not a problem.
                    else:
                        raise
                except (IndexError, KeyError) as e2:
                    self.log.error("Error in thread " + self.name + " while parsing file at " + path + " : " + str(e2))
                    pass
            self.feeder.progressbar.update(1)
            page = self.feeder.nextPage()
        self.runningThreads.get()
        self.runningThreads.task_done()
        self.log.debug("Ending " + self.name)
