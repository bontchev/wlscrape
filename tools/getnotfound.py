#!/usr/bin/env python

from __future__ import print_function
import argparse
import requests
import json
import wget
import sys
import os

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.01"

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

def downloadTheFiles(jsonData, hashes, elementsPerDir):
    seen = set()
    i = 0
    paginate = False
    outputDir = ""
    if ((elementsPerDir > 0) and (len(jsonData) > elementsPerDir)):
        paginate = True
        pageNum = 0
        elementNum = 0
        outputDir = makeOutputDir(pageNum)
    for element in jsonData:
        url = element["url"]
        ext = element["ext"]
        hash = element["md5"].upper()
        if (hash in hashes and not hash in seen):
            seen.add(hash)
            i += 1
            fileName = hash + "." + ext
            if (paginate):
                elementNum += 1
                if (elementNum > elementsPerDir):
                    elementNum = 0
                    pageNum += 1
                    outputDir = makeOutputDir(pageNum)
                fileName = os.path.join(outputDir, fileName)
            print("[" + str(i) + "] " + url + " -> " + fileName, file=sys.stderr)
            try:
                outputFile = wget.download(url, out=fileName)
            except Exception as e:
                error(e)
            print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Downloads suspected malware from Wikileaks.")
    parser.add_argument("-e", "--elements", type=int, help="elements per page")
    parser.add_argument("jsonfile", help="JSON data file")
    parser.add_argument("notfoundhashes", help="file with MD5 hashes of unknown files")
    args = parser.parse_args()
    elements = args.elements
    if (elements < 1):
        elements = 0
    try:
        with open(args.jsonfile, "r") as contentFile:
            content = contentFile.read()
        jsonData = json.loads(content)
        with open(args.notfoundhashes, "r") as hashFile:
            hashes = [line.split()[0].upper() for line in hashFile]
    except Exception as e:
        error(e)
    downloadTheFiles(jsonData, hashes, elements)
    sys.exit(0)
