#!/usr/bin/env python

from __future__ import print_function
from lxml import html
import itertools
import argparse
import requests
import json
import wget
import sys
import os

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.05"

site = "https://wikileaks.org"
area = "/akp-emails/"

def error(e):
    print("Error: %s." % e, file=sys.stderr)
    sys.exit(-1)

def processData(tree, ext, blacklist):
    try:
        links = tree.xpath("//*[@id='searchresult']/tbody/tr/td[2]/a/@href")
        sizes = tree.xpath("//*[@id='searchresult']/tbody/tr/td[3]/text()")
        md5s  = tree.xpath("//*[@id='searchresult']/tbody/tr/td[4]/text()")
    except Exception as e:
        error(e)
    data = []
    for i in range(len(links)):
        theUrl = site + area + links[i]
        if (not theUrl in blacklist):
            data.append({"md5" : md5s[i], "url" : theUrl, "ext" : ext, "size" : sizes[i]})
    return data

def processExtension(ext, blacklist, options):
    unique = options.unique
    pageNums = options.pages
    url = site + area + "?file=" + ext
    if (options.spam):
        url += "&spam=1"
    if (options.duplicates):
        url += "&dupl=1"
    url += "&count=" + str(options.elements) + "&page=1&#searchresult"
    print(url, file=sys.stderr)
    pageNum = 1
    theData = []
    seen = set()
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        if ((len(pageNums) == 0) or (pageNum in pageNums)):
            newData = processData(tree, ext, blacklist)
            if (unique):
                for element in newData:
                    if (not element["md5"] in seen):
                        seen.add(element["md5"])
                        theData.append(element)
            else:
                theData += newData
        #nextButtonXPath = "//*[@id='right-pane']/div[5]/div/ul/li[last()]/a/@href"
        nextButtonXPath  = "//*[@id='right-pane']/div[3]/div/ul/li[last()]/a/@href"
        next = tree.xpath(nextButtonXPath)
        while len(next):
            url = site + next[0]
            print (url, file=sys.stderr)
            pageNum += 1
            page = requests.get(url)
            tree = html.fromstring(page.content)
            if ((len(pageNums) == 0) or (pageNum in pageNums)):
                newData = processData(tree, ext, blacklist)
                if (unique):
                    for element in newData:
                        if (not element["md5"] in seen):
                            seen.add(element["md5"])
                            theData.append(element)
                else:
                    theData += newData
            next = tree.xpath(nextButtonXPath)
    except Exception as e:
        error(e)
    return theData

def makeOutputDir(pageNum):
    outputDir = str(pageNum).zfill(3)
    try:
        if (not os.path.exists(outputDir)):
            os.mkdir(outputDir)
    except Exception as e:
        error(e)
    return outputDir

def printTheData(theData, options):
    md5only = options.md5only
    download = options.download
    elementsPerPage = options.elements
    print("Number of files found: %d." % len(theData), file=sys.stderr)
    try:
        jsonData = json.dumps(theData, indent=4)
        if (not md5only and not download):
            print(jsonData)
        else:
            if (download):
                paginate = False
                outputDir = ""
                if (len(theData) > elementsPerPage):
                    paginate = True
                    pageNum = 0
                    elementNum = 0
                    outputDir = makeOutputDir(pageNum)
            for element in theData:
                md5 = element["md5"].upper()
                if (md5only):
                    print(md5)
                if (download):
                    fileName = md5 + "." + element["ext"]
                    if (paginate):
                        fileName = os.path.join(outputDir, fileName)
                        elementNum += 1
                        if (elementNum >= elementsPerPage):
                            elementNum = 0
                            pageNum += 1
                            outputDir = makeOutputDir(pageNum)
                    outputFile = wget.download(element["url"], out=fileName)
    except Exception as e:
        error(e)

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
    for ext in args.ext:
        theData += processExtension(ext, theBlacklist, args)
    printTheData(theData, args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Scapes suspected malware from Wikileaks.")
    parser.add_argument("-m", "--md5only",    action="store_true", help="only list the hashes")
    parser.add_argument("-d", "--download",   action="store_true", help="download the files")
    parser.add_argument("-s", "--spam",       action="store_true", help="look in the spam folder too")
    parser.add_argument("-p", "--duplicates", action="store_true", help="include duplicates")
    parser.add_argument("-u", "--unique",     action="store_true", help="fetch only one entry per unique MD5")
    parser.add_argument("-e", "--elements", type=int, default=200, help="elements per page")
    parser.add_argument("-b", "--blacklist", dest="blacklist", default=None, help="blacklist file")
    parser.add_argument("-a", "--pages", type=getList, dest="pages", default=[], help="list of pages to process")
    parser.add_argument("ext", nargs="+", help="file extension")
    args = parser.parse_args()
    main(args)
    sys.exit(0)
