#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import argparse
import logging
from warnings import filterwarnings

import pymysql as pymysql

from src.crawler import Crawler
from src.feeder import Feeder

filterwarnings('ignore', category = pymysql.Warning)

# Configuring logging
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')

fileHandler = logging.FileHandler('logs/main.log', mode='w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)
log.addHandler(streamHandler)

# Configuring argument parsing
parser = argparse.ArgumentParser(description="Download all Pokemon Showdown's stats files, and fill a database with its stats.")
parser.add_argument("dbms", help="Database Management System", choices=["mysql"])
parser.add_argument("host", help="Database address")
parser.add_argument("user", help="Database user")
parser.add_argument("password", help="User password")
parser.add_argument("dbname", help="Database name")
parser.add_argument("-v", "--verbose", help="be verbose", action="store_true")
parser.add_argument("-V", "--version", help="show the version number and exit", action="version", version="%(prog)s 0.1")
parser.add_argument("-1", "--skip-download", help="do not download any file from the internet and only use available local files to build the database", action="store_true")
parser.add_argument("-2", "--skip-parse", help="do not parse and do not store any file in a database, and only download files from the internet", action="store_true")
parser.add_argument("-3", "--skip-index", help="do not create index the recommended columns in the final database", action="store_true")
parser.add_argument("-y", "--year", help="Filter : Only treat files in use these years", nargs="+", type=int)
parser.add_argument("-m", "--month", help="Filter : Only treat files in these months", nargs="+", type=int)
parser.add_argument("-f", "--format", help="Filter : Only treat files of these formats", nargs="+")
parser.add_argument("-g", "--gxe", help="Filter : Only treat files at exactly these gxe limits", nargs="+", type=int)
parser.add_argument("-t", "--type", help="Filter : Only treat files of these types", nargs="+", choices=['usage', 'chaos', 'leads', 'metagame', 'moveset'])
parser.add_argument("-d", "--directory", help="directory to use to download files into, and to parse from")
args = parser.parse_args()

if args.verbose:
    streamHandler.setLevel(logging.DEBUG)

filters = {
    'year' : args.year,
    'month' : args.month,
    'format' : args.format,
    'gxe' : args.gxe,
    'type' : args.type
}

# Phase 1 : Download
if not args.skip_download:
    crawler = Crawler(args.directory, filters)
    crawler.run()

# Phase 2 : Parse
if not args.skip_parse:
    feeder = Feeder('stats', args.dbms, args.host, args.user, args.password, args.dbname)
    feeder.feedAll()

# Phase 3 : Post-Insertion
if not args.skip_index:
    feeder = Feeder('stats', args.dbms, args.host, args.user, args.password, args.dbname)
    feeder.postInsert()
