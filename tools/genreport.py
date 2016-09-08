#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
import sys

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.01"

site = "https://wikileaks.org"
area = "/akp-emails/"

def generateReport(jsonData, hashes, options):
    if (not options.noheader):
        if (options.html):
            print('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
            print('<html>')
            print('<head>')
            print('\t<meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">')
            print('\t<title>Malicious files found in the AKP leak on the Wikileaks site</title>')
            print('</head>')
            print('<body>')
            print('')
            print('<table style="text-align: center; width: 100%;" border="1" cellpadding="2" cellspacing="2">')
            print('\t<thead>')
            print('\t\t<tr>')
            print('\t\t\t<th>Number</th>')
            print('\t\t\t<th>Wikileaks e-mail</th>')
            print('\t\t\t<th>Wikileaks URL to the malicious attachment</th>')
            print('\t\t\t<th>VirusTotal analysis</th>')
            print('\t\t</tr>')
            print('\t</thead>')
            print('\t<tbody>')
        else:
            print("Number | Wikileaks e-mail | Wikileaks URL to the malicious attachment | VirusTotal analysis")
            print("--- | --- | --- | ---")
    row = 0
    for element in jsonData:
        hash = element["md5"].upper()
        if (hash in hashes):
            urlParts = element["url"].split("/")
            emailID = urlParts[5]
            fileID = urlParts[6]
            row += 1
            if (options.html):
                print('\t\t<tr>')
                print('\t\t\t<td>' + str(row) + '</td>')
                print('\t\t\t<td><a href="' + site + area + "emailid/" + emailID +
			'" target="_blank" rel="noopener noreferrer">' + emailID + '</a></td>')
                print('\t\t\t<td>hxxxx://wikileaks[.]org' + area + 'fileid/' +
			emailID + '/' + fileID + '</td>')
                print('\t\t\t<td><a href="https://www.virustotal.com/en/search/?query=' +
			hash + '" target="_blank" rel="noopener noreferrer">' + hash + '</a></td>')
                print('\t\t</tr>')
            else:
                print(str(row) + " | [" + emailID + "](" + site + area + "emailid/" + emailID +
			") | hxxxx://wikileaks[.]org" + area + "fileid/" + emailID + "/" + fileID +
			" | [" + hash + "](https://www.virustotal.com/en/search/?query=" + hash + ")")
    if (options.html and not options.nofooter):
        print('\t</tbody>')
        print('</table>')
        print('')
        print('</body>')
        print('</html>')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Generates report about malware on the Wikileaks site.")
    parser.add_argument("-m", "--html", action="store_true", help="Use HTML format")
    parser.add_argument("-n", "--noheader", action="store_true", help="Don't generate table header")
    parser.add_argument("-f", "--nofooter", action="store_true", help="Don't generate table footer")
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
    generateReport(jsonData, hashes, args)
    sys.exit(0)
