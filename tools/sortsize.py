#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

def error(e):
    print("Error: %s." % e, file=sys.stderr)
    sys.exit(-1)

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def getTrueSize(number, unit):
    if (unit == "B"):
        return number
    elif (unit == "KiB"):
        return number * 1024
    elif (unit == "MiB"):
        return number * 1024 ** 2
    elif (unit == "GiB"):
        return number * 1024 ** 3
    else:
        error("Unknown unit: " + unit)

def compare(x, y):
    try:
        parts = x["size"].split(None)
        sizeX = int(getTrueSize(float(parts[0]), parts[1]))
        parts = y["size"].split(None)
        sizeY = int(getTrueSize(float(parts[0]), parts[1]))
    except Excepton as e:
        error(e)
    return sizeX - sizeY

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description='Sorts by the "size" key JSON files produced by wlscrape.py.')
    parser.add_argument("file", nargs="+", help="JSON data file")
    args = parser.parse_args()
    fullContent = []
    try:
        for argument in args.file:
            with open(argument, "r") as contentFile:
                content = contentFile.read()
            fullContent.extend(json.loads(content))
        print(json.dumps(sorted(fullContent, key=cmp_to_key(compare)), indent=4))
    except Exception as e:
        error(e)
    sys.exit(0)
