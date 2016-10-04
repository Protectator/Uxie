#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)
'''
import urllib2
import urlparse
import os, errno
import sys
import re
import pymysql.cursors
import json
from threading import Thread, Semaphore
from HTMLParser import HTMLParser

BASE_URL = "http://www.smogon.com/stats/"
FOLDER_TO_SAVE = "stats"

def downloadFile(url):
    index = urllib2.urlopen(BASE_URL + url)
    fileContent = index.read()
    return (fileContent.strip(), len(fileContent))

# A progress bar !
class ProgressBar():
    def __init__(self, maxProgress):
        self.progress = 0
        self.unit = 'Mo'
        self.divider = 1024 * 1024
        self.length = 80
        self.max = maxProgress
        self.up = '█'
        self.down = '.'
        self.prefix = "Downloaded: "

    def update(self, progress, size):
        if (progress > self.max):
            progress = self.max
        ups = int(progress * self.length / self.max)
        downs = self.length - ups
        perc = 100 * progress / self.max
        finalSize = int(size/self.divider)
        if (ups > 0):
            sys.stdout.write("\r%s[%s%s] (%i%%) %i/%i [%i %s]" % (self.prefix, self.up*ups, self.down*downs, perc, progress, self.max, finalSize, self.unit))
        sys.stdout.flush()
        if (progress == self.max):
            sys.stdout.write("\n")
            sys.stdout.flush()

# Download

class FolderPage(HTMLParser):
    '''
    Represents a downloaded web page with links
    '''
    def __init__(self, baseUrl):
        HTMLParser.__init__(self)
        self.folders = []
        self.files = []
        self.base = baseUrl

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'href':
                    if (not value) or (value[-3:] == "../"):
                        continue
                    elif value[-4:] == ".txt" or value[-5:] == ".json":
                        self.files.append(value)
                    else:
                        self.folders.append(value)

class Crawler():
    def __init__(self, baseUrl):
        self.index = baseUrl
        self.threads = {}
        self.finished = 0
        self.size = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)
        self.nbFiles = 0
        self.bar = ProgressBar(0)

    def run(self):
        self.downloadFolder(self.index)

    def shouldDownload(self, url):
        result = re.search('(\d+)-(\d+)\/.*', url)
        year = int(result.groups()[0])
        month = int(result.groups()[1])
        if month == 12:
            nextYear = year + 1
        else:
            nextYear = year
        nextMonth = (month) % 12 + 1
        finalPath = FOLDER_TO_SAVE + '/' + str(nextYear) + '-' + str(nextMonth).zfill(2) + '/'
        return not os.path.exists(finalPath)

    def downloadFolder(self, url):
        (content, size) = downloadFile(url)
        folder = FolderPage(BASE_URL)
        folder.feed(content)
        for link in folder.folders:
            finalUrl = url + link
            if (self.shouldDownload(finalUrl)):
                self.downloadFolder(finalUrl)
            else:
                print "Ignoring download of " + link

        self.nbFiles = len(folder.files)
        self.finished = 0
        self.size = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)
        self.bar = ProgressBar(self.nbFiles)

        if self.nbFiles > 0:
            print "/" + url + " : " + str(self.nbFiles) + " files to download."
            for link in folder.files:
                finalUrl = url + link
                self.threads[finalUrl] = Thread(target=self.downloadText, args=[finalUrl])
                self.threads[finalUrl].setName(finalUrl)
                self.threads[finalUrl].start()

            self.barrier.acquire()
            self.barrier.release()

    def downloadText(self, url):
        (content, size) = downloadFile(url)
        path = urlparse.urlsplit(url)[2]

        filePath = FOLDER_TO_SAVE + "/" + path

        if not os.path.exists(os.path.dirname(filePath)):
            try:
                os.makedirs(os.path.dirname(filePath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filePath, "w+") as file:
            file.write(content)

        self.mutex.acquire()
        self.finished += 1
        self.size += size
        self.bar.update(self.finished, self.size)
        self.mutex.release()
        if self.finished == self.nbFiles:
            self.barrier.release()
            print "Downloaded " + str(self.finished) + " files."

# Parse

class TextPage():
    def __init__(self, path):
        self.path = path
        matchs = re.search('^(?:/?\w+)?/?(\d+)-(\d+)/((?:[^/]+/)*)([^/]+)-(\d+)\.(txt|json)$', path)
        self.year = (matchs.groups()[0])
        self.month = (matchs.groups()[1])
        self.folders = (matchs.groups()[2])
        self.meta = (matchs.groups()[3])
        self.elo = (matchs.groups()[4])
        self.fileFormat = (matchs.groups()[5])
        self.data = []

class UsageFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)

    def parse(self):
        with open(self.path, mode='r') as file:
            for line in file:
                self.parseLine(line)
        return self.data

    def parseLine(self, line):
        if (line[0:15] == "Total battles: "):
            return
        elif (line[0:19] == " Avg. weight/team: "):
            return
        elif (line[0:2] == " +"):
            return
        elif (line[0:2] == " |"):
            fields = [ field.strip() for field in line.split('|')[1:8] ]
            if (fields[0] != "Rank"):
                fields[2] = fields[2][:-1]
                fields[4] = fields[4][:-1]
                fields[6] = fields[6][:-1]
                self.data.append(fields)

class MovesetFile(TextPage):
    def __init__(self, path):
        TextPage.__init__(self, path)
        self.file = None
        self.currentPokemon = None
        self.currentLine = None

    def parse(self):
        self.file = open(self.path, mode='r')
        while self.nextLine() != "":
            self.parsePokemon()
        self.file.close()
        return self.data

    def nextLine(self):
        self.currentLine = self.file.readline()
        return self.currentLine

    def parsePokemon(self):
        self.currentPokemon = {}
        self.parseName()
        self.parseCount()
        self.parseAbilities()
        self.parseItems()
        self.parseSpreads()
        self.parseMoves()
        self.parseTeammates()
        self.parseCounters()
        self.data.append(self.currentPokemon)

    def parseName(self):
        self.currentPokemon['name'] = self.nextLine().split('|')[1].strip() # ' | Skarmory | '
        pass

    def parseCount(self):
        self.nextLine() # '+----+'
        while not "+--" in self.nextLine():
            if "Raw count: " in self.currentLine:
                self.currentPokemon['raw_count'] = int(self.currentLine.split('|')[1].strip().split(': ')[1]) # ' | Raw count: 4 |  '
            elif "Avg. weight: " in self.currentLine:
                self.currentPokemon['avg_weight'] = float(self.currentLine.split('|')[1].strip().split(': ')[1]) # ' | Avg. weight: 0.4 |  '
            elif "Viability Ceiling:" in self.currentLine:
                self.currentPokemon['viability_ceiling'] = float(self.currentLine.split('|')[1].strip().split(': ')[1]) # ' | Viability Ceiling: 4 |  '
            else:
                raise RuntimeError('Line not recognized : ' + self.currentLine)

    def parseAbilities(self):
        self.nextLine() # '+----+'
        self.nextLine() # ' | Abilities | '
        self.currentPokemon['abilities'] = []
        while not "+--" in self.nextLine():
            ability = {}
            matchs = re.search('^ \| ([^|]+) +([\d.]+)%', self.currentLine) # ' | Gale Wings 67.393% | '
            ability['name'] = matchs.groups()[0]
            ability['percentage'] = float(matchs.groups()[1])
            self.currentPokemon['abilities'].append(ability)

    def parseItems(self):
        self.nextLine() # ' | Items | '
        self.currentPokemon['items'] = []
        while not "+--" in self.nextLine():
            item = {}
            matchs = re.search('^ \| ([^|]+) +([\d.]+)%', self.currentLine) # ' | Rocky Helmet 16.875% | '
            item['name'] = matchs.groups()[0]
            item['percentage'] = float(matchs.groups()[1])
            self.currentPokemon['items'].append(item)

    def parseSpreads(self):
        self.nextLine() # ' | Spreads | '
        self.currentPokemon['ev_spreads'] = []
        while not "+--" in self.nextLine():
            spread = {}
            matchs = re.search('^ \| (?:(\w+):(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)|(Other)) +([\d.]+)%', self.currentLine) # ' | Timid:0/0/0/252/4/252 58.111% | '
            if matchs.groups()[7] == "Other":
                spread['is_other'] = True
            else:
                spread['is_other'] = False
                spread['nature'] = matchs.groups()[0]
                spread['hp'] = int(matchs.groups()[1])
                spread['atk'] = int(matchs.groups()[2])
                spread['def'] = int(matchs.groups()[3])
                spread['spa'] = int(matchs.groups()[4])
                spread['spd'] = int(matchs.groups()[5])
                spread['spe'] = int(matchs.groups()[6])
            spread['percentage'] = float(matchs.groups()[8])
            self.currentPokemon['ev_spreads'].append(spread)

    def parseMoves(self):
        self.nextLine() # ' | Moves | '
        self.currentPokemon['moves'] = []
        while not "+--" in self.nextLine():
            move = {}
            matchs = re.search('^ \| ([^|]+) +([\d.]+)%', self.currentLine) # ' | Brave Bird 99.882% | '
            move['name'] = matchs.groups()[0]
            move['percentage'] = float(matchs.groups()[1])
            self.currentPokemon['moves'].append(move)

    def parseTeammates(self):
        self.nextLine() # ' | Teammates | '
        self.currentPokemon['teammates'] = []
        while not "+--" in self.nextLine():
            mate = {}
            matchs = re.search('^ \| ([^|]+) +([+-]?[\d.]+)%', self.currentLine) # ' | Meloetta +15.409% | '
            mate['name'] = matchs.groups()[0]
            mate['percentage'] = float(matchs.groups()[1])
            self.currentPokemon['teammates'].append(mate)

    def parseCounters(self):
        self.nextLine() # ' | Checks and Counters | '
        self.currentPokemon['counters'] = []
        while not "+--" in self.nextLine():
            counter = {}
            matchs = re.search('^ \| ([^|]+) ([\d.]+) \(([\d.]+)\D+([\d.]+)\)', self.currentLine) # ' | Trubbish 75.535 (86.41±2.72) | '
            counter['name'] = matchs.groups()[0]
            counter['number1'] = float(matchs.groups()[1])
            counter['number2'] = float(matchs.groups()[2])
            counter['number3'] = float(matchs.groups()[3])
            matchs2 = re.search('^ \|\s+\(([\d.]+)%.+/\s+([\d.]+)%', self.nextLine()) # ' | (28.9% KOed / 47.3% switched out)| '
            counter['koed'] = float(matchs2.groups()[0])
            counter['switched_out'] = float(matchs2.groups()[1])
            self.currentPokemon['counters'].append(counter)

class MetagameFile(TextPage):
    pass

class LeadsFile(TextPage):
    pass

class ChaosFile(TextPage):
    pass

class DataBase():
    pass

class MySQL(DataBase):
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(host='localhost',
                             user='uxie',
                             password='uxie',
                             db='uxie',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def initialize(self):
        with self.connection.cursor() as cursor:
            sql = """DROP TABLE IF EXISTS `usage`;
                  CREATE TABLE IF NOT EXISTS `usage` (
                    `year` int(11) NOT NULL,
                    `month` int(11) NOT NULL,
                    `format` varchar(32) NOT NULL,
                    `elo` int(11) NOT NULL,
                    `pokemon` varchar(32) NOT NULL,
                    `usage_percent` float DEFAULT NULL,
                    `raw_usage` int(11) DEFAULT NULL,
                    `raw_percent` float DEFAULT NULL,
                    `real_usage` int(11) DEFAULT NULL,
                    `real_percent` float DEFAULT NULL,
                    UNIQUE KEY `usage_year_month_format_elo_pokemon_pk` (`year`,`month`,`format`,`elo`,`pokemon`)
                  ) ENGINE=MyISAM DEFAULT CHARSET=latin1;"""
            cursor.execute(sql)
        self.connection.commit()

    def fillUsage(self, usageFile):
        try:
            with self.connection.cursor() as cursor:
                data = [[usageFile.year, usageFile.month, usageFile.meta, usageFile.elo, line[1], line[2], line[3], line[4], line[5], line[6]] for line in usageFile.data]
                sql = "INSERT INTO `usage` (`year`, `month`, `format`, `elo`, `pokemon`, `usage_percent`, `raw_usage`, `raw_percent`, `real_usage`, `real_percent`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()

# Fill DB

# Execute
# crawler = Crawler('')
# crawler.run()
# parser = Parser()
page = UsageFile('stats/2014-11/350cup-0.txt')
page.parse()
db = MySQL()
db.connect()
db.initialize()
db.fillUsage(page)
# page = MovesetFile('stats/2016-06/moveset/lc-1500.txt')
# page.parse()
print page.data