#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

site = "https://wikileaks.org"
area = "/akp-emails/"

def generateReport(jsonData, hashes):
    print("Wikileaks e-mail containing the malicious attachment | Wikileaks URL to the malicious attachment | VirusTotal analysis")
    print("--- | --- | ---")
    for element in jsonData:
        hash = element["md5"].upper()
        if (hash in hashes):
            urlParts = element["url"].split("/")
            emailID = urlParts[5]
            fileID = urlParts[6]
            print("[" + emailID + "](" + site + area + "emailid/" + emailID +
		") | hxxxx://wikileaks[.]org" + area + "fileid/" + emailID + "/" + fileID +
		" | [" + hash + "](https://www.virustotal.com/en/search/?query=" + hash + ")")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Generates report about malware on the Wikileaks site.")
    parser.add_argument("jsonfile", help="JSON data file")
    parser.add_argument("foundhashes", help="file with MD5 hashes of infected files")
    args = parser.parse_args()
    try:
        with open(args.jsonfile, "r") as contentFile:
            content = contentFile.read()
        jsonData = json.loads(content)
        with open(args.foundhashes, "r") as hashFile:
            hashes = [line.split()[0].upper() for line in hashFile]
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
    generateReport(jsonData, hashes)
    sys.exit(0)
