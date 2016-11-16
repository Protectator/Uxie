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
import requests
import codecs
import logging
import threading
import re

from src import utils
from src.parsers import textfile
from src.constants import *
from src.progressbar import *

try:
    from Queue import Queue, Empty
    from HTMLParser import HTMLParser
    from urlparse import urlsplit
except ImportError:
    from queue import Queue, Empty
    from urllib.parse import urlsplit
    from html.parser import HTMLParser


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


def shouldDownload(textPage):
    finalPath = FOLDER_TO_SAVE + textPage.localPath
    return not os.path.exists(finalPath)


# Decorator
def synchronized(method):
    def new_method(self, *arg, **kws):
        with self.lock:
            return method(self, *arg, **kws)

    return new_method


class Crawler:
    lock = threading.RLock()
    def __init__(self, baseUrl, filters):
        self.index = baseUrl
        self.toDownload = Queue()
        self.bar = ProgressBar(0)
        self.filters = filters
        self.log = logging.getLogger('main')

    def run(self):
        self.__discoverFolder('')
        self.__download()

    def __discoverFolder(self, url):
        self.log.info("Discovering " + url)
        (content, size) = downloadFile(url)
        folder = FolderPage(BASE_URL)
        folder.feed(content)
        for link in folder.folders:
            finalUrl = url + link
            if utils.filterFolder(finalUrl, self.filters):
                self.__discoverFolder(finalUrl)

        self.nbFiles = len(folder.files)

        if self.nbFiles > 0:
            for link in folder.files:
                finalUrl = url + link
                page = textfile.TextPage(finalUrl)
                if utils.filter(page, self.filters):
                    self.toDownload.put(page)

    def __download(self):
        self.runningThreads = Queue()
        for i in range(DOWNLOAD_THREADS):
            self.runningThreads.put(i)
            t = CrawlerWorker(self, i, self.toDownload, self.runningThreads)
            t.setDaemon(True)
            t.start()
        self.runningThreads.join()

    @synchronized
    def nextPage(self):
        try:
            next = self.toDownload.get(False)
            return next
        except Empty:
            return None

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


class CrawlerWorker(threading.Thread):
    def __init__(self, crawler, tId, queue, runningThreads):
        threading.Thread.__init__(self)
        self.crawler = crawler
        self.tId = tId
        self.queue = queue
        self.runningThreads = runningThreads
        self.log = logging.getLogger('main')
        self.name = "crawlerworker_" + str(tId)

    def run(self):
        self.log.debug("Starting " + self.name)
        page = self.crawler.nextPage()
        while (page is not None):
            self.log.debug(self.name + "starting to download " + page.path + " -> " + page.localPath)
            (content, size) = downloadFile(page.path)

            filePath = FOLDER_TO_SAVE + page.localPath

            if not os.path.exists(os.path.dirname(filePath)):
                try:
                    os.makedirs(os.path.dirname(filePath))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            with codecs.open(filePath, "w+", "utf-8") as newFile:
                newFile.write(content)
            page = self.crawler.nextPage()
        self.runningThreads.get()
        self.runningThreads.task_done()
        self.log.debug("Ending " + self.name)


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
