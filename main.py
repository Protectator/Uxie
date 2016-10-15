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
from src.feeder import Feeder

from warnings import filterwarnings
import pymysql as pymysql
filterwarnings('ignore', category = pymysql.Warning)

parser = argparse.ArgumentParser(description="Download all Pokemon Showdown's stats files, and fill a database with its stats.")
parser.add_argument("dbms", help="Database Management System", choices=["mysql"])
parser.add_argument("host", help="Database address")
parser.add_argument("user", help="Database user")
parser.add_argument("password", help="User password")
parser.add_argument("dbname", help="Database name")
group = parser.add_mutually_exclusive_group()
group.add_argument("-p", "--only-parse", "--skip-download", help="do not download any file from the internet and only use available local files to build the database", action="store_true")
# group.add_argument("-d", "--only-download", "--skip-parse", help="do not parse and do not store any file in a database, and only download files from the internet", action="store_true")
parser.add_argument("-F", "--folder", help="folder to use to download files into, and to parse from")
parser.add_argument("-f", "--file", help="only process a single specific file")
parser.add_argument("-v", "--verbose", help="be verbose", action="store_true")
args = parser.parse_args()

# Phase 1 : Download
print args
if not args.only_parse:
    crawler = Crawler('')
    crawler.run()

# Phase 2 : Parse
feeder = Feeder('.')
feeder.feedAll(args.dbms, args.host, args.user, args.password, args.dbname)
