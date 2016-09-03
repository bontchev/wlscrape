#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Lists the MD5 hashes of a wlscrape.py output.")
    parser.add_argument("file", nargs="+", help="JSON data file")
    args = parser.parse_args()
    for argument in args.file:
        try:
            with open(argument, "r") as contentFile:
                content = contentFile.read()
            jsonData = json.loads(content)
        except Exception as e:
            print("Error: %s." % e, file=sys.stderr)
            sys.exit(-1)
        for element in jsonData:
            print(element["md5"].upper())
    sys.exit(0)
