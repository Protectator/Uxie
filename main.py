'''
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)
'''
import urllib2
import urlparse
import os, errno
import time
from threading import Thread, Semaphore
from HTMLParser import HTMLParser

BASE_URL = "http://www.smogon.com/stats/"
FOLDER_TO_SAVE = "stats"

def downloadFile(url):
    print " URL " + url
    index = urllib2.urlopen(BASE_URL + url)
    fileContent = index.read()
    return fileContent.strip()

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

class TextPage():
    def __init__(self, directory, fileName, date, elo, content):
        self.directory = directory
        self.fileName = fileName
        self.date = date
        self.elo = elo
        self.content = content

class Crawler():
    def __init__(self, baseUrl):
        self.index = baseUrl
        self.threads = {}
        self.finished = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)
        self.nbFiles = 0

    def run(self):
        self.downloadFolder(self.index)

    def downloadFolder(self, url):
        content = downloadFile(url)
        folder = FolderPage(BASE_URL)
        folder.feed(content)
        for link in folder.folders:
            finalUrl = url + link
            print("-> " + finalUrl)
            self.downloadFolder(finalUrl)
            print("<- " + finalUrl)

        self.nbFiles = len(folder.files)
        print "" + str(self.nbFiles) + " files to download."

        self.finished = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

        for link in folder.files:
            finalUrl = url + link
            self.threads[finalUrl] = Thread(target=self.downloadText, args=[finalUrl])
            self.threads[finalUrl].setName(finalUrl)
            self.threads[finalUrl].start()

        self.barrier.acquire()
        self.barrier.release()

    def downloadText(self, url):
        content = downloadFile(url)
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
        print "Finished " + str(self.finished) + " !"
        self.mutex.release()
        if self.finished == self.nbFiles:
            self.barrier.release()
            print "Downloaded " + str(self.finished) + " files."

# Parse

class UsageFile(TextPage):
    pass

class MovesetFile(TextPage):
    pass

class MetagameFile(TextPage):
    pass

class LeadsFile(TextPage):
    pass

class ChaosFile(TextPage):
    pass

# Fill DB

# Execute
crawler = Crawler('')
crawler.run()