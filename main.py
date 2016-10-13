#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import argparse

from src.crawler import Crawler
from src.databases.mysql import *
from src.parsers.usage import *
from src.parsers.leads import *
from src.parsers.metagame import *
from src.parsers.moveset import *

parser = argparse.ArgumentParser(description="Download all Pokemon Showdown's stats files, and fill a database with its stats.")
parser.add_argument("dbms", help="Database Management System", choices=["mysql"])
parser.add_argument("host", help="Database address")
parser.add_argument("user", help="Database user")
parser.add_argument("password", help="User password")
parser.add_argument("dbname", help="Database name")
parser.add_argument("-D", "--skip-download", help="do not download any file from the internet and only use available local files to build the database.", action="store_true")
parser.add_argument("-f", "--file", help="only process a single specified file")
args = parser.parse_args()

# Phase 1 : Download
print args
if not args.skip_download:
    crawler = Crawler('')
    crawler.run()

# Phase 2 : Parse
if args.file is not None:
    file = TextPage(args.file)
    type = file.folders
    if "leads" in type:
        parser = LeadsFile(args.file)
    elif "metagame" in type:
        parser = MetagameFile(args.file)
    elif "moveset" in type:
        parser = MetagameFile(args.file)
    elif "chaos" in type:
        parser = MetagameFile(args.file)
    else:
        parser = UsageFile(args.file)

    # Phase 3 : Fill DB
    db = MySQL()
    db.connect(args.host, args.user, args.password, args.dbname)
    db.initialize()
    db.fillMoveset(parser)
