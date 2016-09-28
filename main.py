'''
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)
'''
import urllib2
from HTMLParser import HTMLParser

def downloadFile(url):
    index = urllib2.urlopen(url)
    fileContent = index.read()
    return fileContent.strip()

class WebPage(HTMLParser):
    '''
    Represents a downloaded web page with links
    '''
    def __init__(self, baseUrl):
        HTMLParser.__init__(self)
        self.folders = set()
        self.files = set()
        self.base = baseUrl

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'href':
                    if not value:
                        continue
                    elif value[-4:] == ".txt":
                        self.files.add(self.base + value)
                    else:
                        self.folders.add(self.base + value)

# Parse them


# Fill DBs

# Execute
BASE_URL = "http://www.smogon.com/stats/"
indexPage = WebPage(BASE_URL)
indexPage.feed(downloadFile(BASE_URL))

print(indexPage.folders)
print(indexPage.files)
