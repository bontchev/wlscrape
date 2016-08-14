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
__VERSION__ = "1.02"

site = "https://wikileaks.org"
area = "/akp-emails/"

def processData(tree, ext):
    try:
        links = tree.xpath("//*[@id='searchresult']/tbody/tr/td[2]/a/@href")
        md5s  = tree.xpath("//*[@id='searchresult']/tbody/tr/td[4]/text()")
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
    data = []
    for i in range(len(links)):
        found = False
        for element in data:
            if (element["md5"] == md5s[i]):
                found = True
                break
        if (not found):
            data.append({"md5" : md5s[i], "url" : site + area + links[i], "ext" : ext})
    return data

def processExtension(ext, spam):
    url = site + area + "?file=" + ext
    if (spam):
        url += "&spam=1"
    url += "&count=200&page=1&#searchresult"
    print(url, file=sys.stderr)
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
    theData = processData(tree, ext)
    #nextButtonXPath = "//*[@id='right-pane']/div[5]/div/ul/li[last()]/a/@href"
    nextButtonXPath  = "//*[@id='right-pane']/div[3]/div/ul/li[last()]/a/@href"
    try:
        next = tree.xpath(nextButtonXPath)
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
    while len(next):
        url = site + next[0]
        print (url, file=sys.stderr)
        try:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            theData += processData(tree, ext)
            next = tree.xpath(nextButtonXPath)
        except Exception as e:
            print("Error: %s." % e, file=sys.stderr)
            sys.exit(-1)
    return theData

def printTheData(theData, md5only, download):
    print("Number of unique files found: %d." % len(theData), file=sys.stderr)
    try:
        jsonData = json.dumps(theData, indent=4)
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
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
                    print("Error: %s." % e, file=sys.stderr)
                    sys.exit(-1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scapes suspected malware from Wikileaks.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __VERSION__)
    parser.add_argument("-m", "--md5only", action="store_true", help="only list the hashes")
    parser.add_argument("-d", "--download", action="store_true", help="download the files")
    parser.add_argument("-s", "--spam", action="store_true", help="look in the spam folder too")
    parser.add_argument("ext", nargs="+", help="file extension")
    args = parser.parse_args()
    theData = []
    for ext in args.ext:
        theData += processExtension(ext, args.spam)
    printTheData(theData, args.md5only, args.download)
    sys.exit(0)
