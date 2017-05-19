#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from html.parser import HTMLParser
import urllib.request
from urllib import parse
import sys
import re

def usage():
    print("[*]Usage: python comment_crawler.py [URL to crawl]")
    exit(0)

if len(sys.argv) < 2:
    usage()
    
visitedLinks = []
loadedComments = []
prevStartTag = ""

output=open("comments.txt",'w')

class LinkParser(HTMLParser):
    def substringOf(self,comment):
        global loadedComments
        for loaded in loadedComments:
            if loaded.find(comment) != -1:
                return True
        return False

    def handleJSComments(self,url,jsString):
        global loadedComments
        first = True
        for m in re.finditer('/*', jsString):
            comment = jsString[m.start():]
            comment = comment[:comment.find('*/')+2]
            if self.substringOf(comment) == False:
                if first:
                    print(url+": ")
                    output.write(url+": ")
                    output.write("\n")
                    first = False
                print(comment)
                output.write(comment)
                output.write("\n")
                loadedComments.append(comment)
        for m in re.finditer('//', jsString):
            comment = jsString[m.start():]
            comment = comment[:comment.find('\n')]
            if comment not in loadedComments:
                if first:
                    print(url+": ")
                    output.write(url+": ")
                    output.write("\n")
                    first = False
                print(comment)
                output.write(comment)
                output.write("\n")
                loadedComments.append(comment) 

    def handleHTMLComments(self,url,htmlString):
        global loadedComments
        if '<!--' not in htmlString:
            return
        first = True
        for m in re.finditer('<!--', htmlString):
             comment = htmlString[m.start():]
             comment = comment[:comment.find('-->')+3]
             if self.substringOf(comment) == False:
                if first:
                    print(url+": ")
                    output.write(url+": ")
                    output.write("\n")
                    first = False
                print(comment)
                output.write(comment)
                output.write("\n")
                loadedComments.append(comment)           

    def findAllCommentsFromHtml(self,url,htmlString):
        if '.js' in url:
            self.handleJSComments(url,htmlString)
        else:
            self.handleHTMLComments(url,htmlString)

             
    def handle_data(self, data):
        global prevStartTag
        if prevStartTag == 'script':
            self.handleJSComments(self.baseUrl,data)

    def handle_starttag(self, tag, attrs):
        global visitedLinks,prevStartTag
        prevStartTag = tag
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    if newUrl[:4] == 'http':
                        domain = newUrl.split('/')[2].split('.')[0]
                        if self.domain in domain and newUrl not in visitedLinks:
                            self.links = self.links + [newUrl]
                            visitedLinks.append(newUrl)
        elif tag == 'script':
            for (key, value) in attrs:
                if key == 'src':
                    #print(value)
                    if (value[0] == '/' and value[1] != '/') or self.domain in value:
                        newUrl = self.baseUrl + value
                        if self.domain in newUrl and newUrl not in visitedLinks:
                            self.links = self.links + [newUrl]
                            visitedLinks.append(newUrl)

    def getLinks(self, url):
        global visitedLinks
        self.links = []
        self.baseUrl = url
        response = urllib.request.urlopen(url)
        #print(response.getcode())
        htmlBytes = response.read()
        htmlString = htmlBytes.decode('utf-8')
        self.findAllCommentsFromHtml(url,htmlString)
        #print(htmlString)
        self.feed(htmlString)
        return (htmlString, self.links)

def spider(url, maxPages):
    parsed_uri = urlparse(url)
    domain = url.split('/')[2].split('.')[0]
    print("Domain is " + domain)
    pagesToVisit = [url]
    numberVisited = 0
    parser = LinkParser()
    LinkParser.domain = property(lambda self: domain)
            
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            #print(numberVisited, 'Visiting:', url)
            (data, links) = parser.getLinks(url)
            pagesToVisit = pagesToVisit + links
        except urllib.error.HTTPError as e:
            pass
            #print(e)
            #print("Error! Skipping URL")
        except KeyboardInterrupt:
            output.close()
            sys.exit(0)
spider(sys.argv[1], 1000)
