#!/usr/bin/env python

from __future__ import print_function
import argparse
import locale
import json
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

def error(e):
    print("Error: %s." % e, file=sys.stderr)
    sys.exit(-1)

def humanBytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B  = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776
   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} Kb'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} Mb'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} Gb'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} Tb'.format(B/TB)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Computes the total files size of a wlscrape.py output.")
    parser.add_argument("file", nargs="+", help="JSON data file")
    args = parser.parse_args()
    numFiles = 0
    totalSize = 0.0
    for argument in args.file:
        try:
            with open(argument, "r") as contentFile:
                content = contentFile.read()
            jsonData = json.loads(content)
            for element in jsonData:
                numFiles += 1
                parts = element["size"].split(None)
                totalSize += getTrueSize(float(parts[0]), parts[1])
        except Exception as e:
            error(e)
    locale.setlocale(locale.LC_ALL, "")
    print("Number of files found: %s." % locale.format("%d", numFiles, grouping=True), file=sys.stderr)
    print("Total size: {0}.".format(humanBytes(totalSize)), file=sys.stderr)
    sys.exit(0)
