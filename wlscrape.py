#!/usr/bin/env python

from __future__ import print_function
from lxml import html
import argparse
import requests
import json
import wget
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.03"

site = "https://wikileaks.org"
area = "/akp-emails/"

def error(e):
    print("Error: %s." % e, file=sys.stderr)
    sys.exit(-1)

def processData(tree, ext, blacklist):
    try:
        links = tree.xpath("//*[@id='searchresult']/tbody/tr/td[2]/a/@href")
        md5s  = tree.xpath("//*[@id='searchresult']/tbody/tr/td[4]/text()")
    except Exception as e:
        error(e)
    data = []
    for i in range(len(links)):
        theUrl = site + area + links[i]
        if (not theUrl in blacklist):
            data.append({"md5" : md5s[i], "url" : theUrl, "ext" : ext})
    return data

def processExtension(ext, spam, duplicates, blacklist):
    url = site + area + "?file=" + ext
    if (spam):
        url += "&spam=1"
    if (duplicates):
        url += "&dupl=1"
    url += "&count=200&page=1&#searchresult"
    print(url, file=sys.stderr)
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
    except Exception as e:
        error(e)
    theData = processData(tree, ext, blacklist)
    #nextButtonXPath = "//*[@id='right-pane']/div[5]/div/ul/li[last()]/a/@href"
    nextButtonXPath  = "//*[@id='right-pane']/div[3]/div/ul/li[last()]/a/@href"
    try:
        next = tree.xpath(nextButtonXPath)
    except Exception as e:
        error(e)
    while len(next):
        url = site + next[0]
        print (url, file=sys.stderr)
        try:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            theData += processData(tree, ext, blacklist)
            next = tree.xpath(nextButtonXPath)
        except Exception as e:
            error(e)
    return theData

def printTheData(theData, md5only, download):
    print("Number of files found: %d." % len(theData), file=sys.stderr)
    try:
        jsonData = json.dumps(theData, indent=4)
    except Exception as e:
        error(e)
    if (not md5only and not download):
        print(jsonData)
    else:
        for element in theData:
            if (md5only):
                print(element["md5"].upper())
            if (download):
                try:
                    filename = wget.download(element["url"], out=(element["md5"].upper() + "." + element["ext"]))
                except Exception as e:
                    error(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scapes suspected malware from Wikileaks.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __VERSION__)
    parser.add_argument("-m", "--md5only", action="store_true", help="only list the hashes")
    parser.add_argument("-d", "--download", action="store_true", help="download the files")
    parser.add_argument("-s", "--spam", action="store_true", help="look in the spam folder too")
    parser.add_argument("-p", "--duplicates", action="store_true", help="include duplicates")
    parser.add_argument("-b", "--blacklist", dest="blacklist", default=None, help="blacklist file")
    parser.add_argument("ext", nargs="+", help="file extension")
    args = parser.parse_args()
    theData = []
    theBlacklist = []
    if (args.blacklist != None):
        try:
            with open(args.blacklist, "r") as f:
                theBlacklist = [line for line in f.read().split('\n') if line.strip()]
        except Exception as e:
            error(e)
    for ext in args.ext:
        theData += processExtension(ext, args.spam, args.duplicates, theBlacklist)
    printTheData(theData, args.md5only, args.download)
    sys.exit(0)
