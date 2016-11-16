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

from src import utils
from src.parsers import textfile
from src.constants import *
from tqdm import tqdm

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


# Decorator
def synchronized(method):
    def new_method(self, *arg, **kws):
        with self.lock:
            return method(self, *arg, **kws)

    return new_method


class Crawler:
    lock = threading.RLock()

    def __init__(self, baseFolder, filters):
        self.folder = baseFolder if baseFolder is not None else FOLDER_TO_SAVE
        self.toDownload = Queue()
        self.filters = filters
        self.totalSize = 0
        self.log = logging.getLogger('main')

    def run(self):
        self.log.info("Looking for files to download at " + BASE_URL + " ...")
        self.__discoverFolder('')
        self.log.info("Starting to download " + str(self.toDownload.qsize()) + " files into folder " + self.folder)
        self.__download()

    def __discoverFolder(self, url):
        self.log.info("Discovering " + url)
        (content, size) = downloadFile(url)
        folder = FolderPage(BASE_URL)
        folder.feed(content)
        for link in folder.folders:
            finalUrl = url + link.url
            if utils.filterFolder(finalUrl, self.filters):
                self.__discoverFolder(finalUrl)
        self.nbFiles = len(folder.files)
        if self.nbFiles > 0:
            for link in folder.files:
                finalUrl = url + link.url
                page = textfile.TextPage(finalUrl, link.size)
                if utils.filter(page, self.filters):
                    self.totalSize += page.size
                    self.toDownload.put(page)

    def __download(self):
        self.progressbar = tqdm(total=self.totalSize, unit_scale=True, unit='o', dynamic_ncols=True, maxinterval=1,
                                mininterval=0.5, smoothing=0.05)
        self.runningThreads = Queue()
        for i in range(DOWNLOAD_THREADS):
            self.runningThreads.put(i)
            t = CrawlerWorker(self, i, self.toDownload, self.runningThreads)
            t.setDaemon(True)
            t.start()
        self.runningThreads.join()
        self.progressbar.close()

    @synchronized
    def nextPage(self):
        try:
            next = self.toDownload.get(False)
            return next
        except Empty:
            return None

    def __downloadText(self, url):
        (content, size) = downloadFile(url)
        path = urlsplit(url)[2]
        filePath = self.folder + "/" + path
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
            self.log.debug(self.name + " starting to download " + page.path)
            (content, size) = downloadFile(page.path)
            filePath = self.crawler.folder + page.localPath
            if not os.path.exists(os.path.dirname(filePath)):
                try:
                    os.makedirs(os.path.dirname(filePath))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            with codecs.open(filePath, "w+", "utf-8") as newFile:
                newFile.write(content)
            self.crawler.progressbar.update(page.size)
            page = self.crawler.nextPage()
        self.runningThreads.get()
        self.runningThreads.task_done()
        self.log.debug("Ending " + self.name)


class FileLink():
    def __init__(self, url):
        self.url = url
        self.size = 0

    def setSize(self, size):
        if self.size == 0:
            self.size = int(size)
        else:
            raise RuntimeError('Tried to set size of a FileLink that has already been set.')


class FolderPage(HTMLParser):
    """
    Represents a downloaded web page with links
    """

    def __init__(self, baseUrl):
        HTMLParser.__init__(self)
        self.folders = []
        self.files = []
        self.needSize = False
        self.base = baseUrl

    def handle_starttag(self, tag, attrs):
        if not self.needSize:
            if tag == 'a':
                for key, value in attrs:
                    if key == 'href':
                        if (not value) or (value[-3:] == "../"):
                            continue
                        elif value[-4:] == ".txt" or value[-5:] == ".json":
                            self.files.append(FileLink(value))
                            self.needSize = True
                        else:
                            self.folders.append(FileLink(value))
        else:
            raise RuntimeError('Tried to parse a link before the last one recieved a size.')

    def handle_data(self, data):
        try:
            parts = data.split()
            if len(parts) < 2:
                return
            val = int(parts[-1])
            if self.needSize:
                self.files[-1].setSize(val)
                self.needSize = False
            else:
                raise RuntimeError('Tried to add a size when no file was waiting for one.')
        except ValueError:
            pass  # It's probably something else : Everything's normal
