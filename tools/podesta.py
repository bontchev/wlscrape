#!/usr/bin/env python

from __future__ import print_function
from lxml import html
import itertools
import argparse
import requests
import wget
import sys
import os

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

site = "https://wikileaks.org"
area = "/podesta-emails/"

def error(e):
    print("Error: %s." % e, file=sys.stderr)
    sys.exit(-1)

def makeOutputDir(pageNum):
    outputDir = str(pageNum).zfill(3)
    try:
        if (not os.path.exists(outputDir)):
            os.mkdir(outputDir)
    except Exception as e:
        error(e)
    return outputDir

def printTheEmails(theData, options):
    download = options.download
    elementsPerPage = options.elements
    try:
        if (download):
            paginate = False
            outputDir = ""
            elementNum = 1
            if (len(theData) > elementsPerPage):
                paginate = True
                pageNum = 1
                outputDir = makeOutputDir(pageNum)
        for url in theData:
            if (download):
                fileName = url.replace(site + area + "get/", "") + ".eml"
                if (paginate):
                    if (elementNum > elementsPerPage):
                        elementNum = 1
                        pageNum += 1
                        outputDir = makeOutputDir(pageNum)
                    fileName = os.path.join(outputDir, fileName)
                outputFile = wget.download(url, out=fileName)
                elementNum += 1
            else:
                print(url)
    except Exception as e:
        error(e)

def processData(tree, blacklist, options):
    elementsPerPage = options.elements
    theData = []
    try:
        links = tree.xpath("//*[@id='searchresult']/tbody/tr/td[@colspan='4']/a/@href")
        for i in range(len(links)):
            theUrl = site + area + links[i].replace("emailid", "get")
            if (not theUrl in blacklist):
                theData.append(theUrl)
    except Exception as e:
        error(e)
    return theData

def getTheEmails(blacklist, options):
    pageNums = options.pages
    url = site + area + "?q=&sort=1"
    url += "&count=" + str(options.elements) + "&page=1&#searchresult"
    print(url, file=sys.stderr)
    pageNum = 1
    theData = []
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        if ((len(pageNums) == 0) or (pageNum in pageNums)):
            newData = processData(tree, blacklist, options)
            theData += newData
        nextButtonXPath  = "//*[@id='right-pane']/div[3]/div/ul/li[last()]/a/@href"
        next = tree.xpath(nextButtonXPath)
        while len(next):
            url = site + next[0]
            print (url, file=sys.stderr)
            pageNum += 1
            page = requests.get(url)
            tree = html.fromstring(page.content)
            if ((len(pageNums) == 0) or (pageNum in pageNums)):
                newData = processData(tree, blacklist, options)
                theData += newData
            next = tree.xpath(nextButtonXPath)
    except Exception as e:
        error(e)
    return theData

def getList(argument):
    return list(set(itertools.chain.from_iterable([range(int(y[0]), int(y[1]) + 1) for y in [(x.split('-') + [x])[:2] for x in argument.split(',')]])))

def main(args):
    theData = []
    theBlacklist = []
    if (args.blacklist != None):
        try:
            with open(args.blacklist, "r") as blacklistFile:
                theBlacklist = [line.split()[0] for line in blacklistFile.read().split('\n') if line.strip()]
        except Exception as e:
            error(e)
    if (args.elements < 10):
        args.elements = 10
    if (args.elements > 200):
        args.elements = 200
    printTheEmails(getTheEmails(theBlacklist, args), args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Scapes the Podesta e-mails from Wikileaks.")
    parser.add_argument("-d", "--download",   action="store_true", help="download the e-mails")
    parser.add_argument("-e", "--elements", type=int, default=200, help="e-mails per page")
    parser.add_argument("-b", "--blacklist", dest="blacklist", default=None, help="blacklist file")
    parser.add_argument("-a", "--pages", type=getList, dest="pages", default=[], help="list of pages to process")
    args = parser.parse_args()
    main(args)
    sys.exit(0)
