#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import errno
import os
import re
import requests
import codecs
import time
import logging

try:
    from HTMLParser import HTMLParser
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit
    from html.parser import HTMLParser

from threading import Thread, Semaphore

from src.constants import *
from src.progressbar import *


def downloadFile(url):
    tries = 0
    while tries < 3:
        try:
            r = requests.get(BASE_URL + url)
            r.encoding = "utf-8"
            fileContent = r.text
            return fileContent.strip(), len(fileContent)
        except (requests.ConnectionError, requests.ConnectTimeout) as e:
            tries += 1
            if tries >= 3:
                raise e


def shouldDownload(url):
    result = re.search('(\d+)-(\d+)\/.*', url)
    year = int(result.groups()[0])
    month = int(result.groups()[1])
    if month == 12:
        nextYear = year + 1
    else:
        nextYear = year
    nextMonth = month % 12 + 1
    finalPath = FOLDER_TO_SAVE + '/' + str(nextYear) + '-' + str(nextMonth).zfill(2) + '/'
    return not os.path.exists(finalPath)


class Crawler:
    def __init__(self, baseUrl):
        self.index = baseUrl
        self.threads = {}
        self.finished = 0
        self.size = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)
        self.nbFiles = 0
        self.bar = ProgressBar(0)
        self.log = logging.getLogger('main')

    def run(self):
        self.downloadFolder(self.index)

    def downloadFolder(self, url):
        (content, size) = downloadFile(url)
        folder = FolderPage(BASE_URL)
        folder.feed(content)
        for link in folder.folders:
            finalUrl = url + link
            if shouldDownload(finalUrl):
                self.downloadFolder(finalUrl)
            else:
                self.log.info("Ignoring download of " + link)

        self.nbFiles = len(folder.files)
        self.finished = 0
        self.size = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)
        self.bar = ProgressBar(self.nbFiles)

        if self.nbFiles > 0:
            self.log.info("/" + url + " : " + str(self.nbFiles) + " files to download.")
            for link in folder.files:
                finalUrl = url + link
                self.threads[finalUrl] = Thread(target=self.downloadText, args=[finalUrl])
                self.threads[finalUrl].setName(finalUrl)
                self.threads[finalUrl].daemon=True
                self.threads[finalUrl].start()
            # TODO: make this better
            while not self.barrier.acquire(False):
                time.sleep(1)
            self.barrier.release()

    def downloadText(self, url):
        (content, size) = downloadFile(url)
        path = urlsplit(url)[2]

        filePath = FOLDER_TO_SAVE + "/" + path

        if not os.path.exists(os.path.dirname(filePath)):
            try:
                os.makedirs(os.path.dirname(filePath))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with codecs.open(filePath, "w+", "utf-8") as newFile:
            newFile.write(content)

        self.mutex.acquire()
        self.finished += 1
        self.size += size
        self.bar.update(self.finished, self.size)
        self.mutex.release()
        if self.finished == self.nbFiles:
            self.barrier.release()
            self.log.info("Downloaded " + str(self.finished) + " files.")


class FolderPage(HTMLParser):
    """
    Represents a downloaded web page with links
    """

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
