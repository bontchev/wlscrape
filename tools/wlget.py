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
__VERSION__ = "1.02"

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

def downloadTheData(theData, elementsPerDir):
    try:
        jsonData = json.loads(theData)
        paginate = False
        outputDir = ""
        seen = set()
        elementNum = 1
        if ((elementsPerDir > 0) and (len(theData) > elementsPerDir)):
            paginate = True
            pageNum = 1
            outputDir = makeOutputDir(pageNum)
        for element in jsonData:
            hash = element["md5"].upper()
            if (not hash in seen):
                seen.add(hash)
                fileName = hash + "." + element["ext"]
                if (paginate):
                    if (elementNum > elementsPerDir):
                        elementNum = 1
                        pageNum += 1
                        outputDir = makeOutputDir(pageNum)
                    fileName = os.path.join(outputDir, fileName)
                outputFile = wget.download(element["url"], out=fileName)
                elementNum += 1
    except Exception as e:
        error(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Downloads suspected malware from Wikileaks.")
    parser.add_argument("-e", "--elements", type=int, help="elements per page")
    parser.add_argument("file", nargs="+", help="JSON data file")
    args = parser.parse_args()
    elements = args.elements
    if (elements < 1):
        elements = 0
    for argument in args.file:
        try:
            with open(argument, "r") as contentFile:
                content = contentFile.read()
            downloadTheData(content, elements)
        except Exception as e:
            error(e)
    sys.exit(0)
