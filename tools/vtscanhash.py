#!/usr/bin/env python

from __future__ import print_function
from stat import *
import virustotal
import argparse
import sys
import os

__author__ = "Vesselin Bontchev <vbontchev@yahoo.com>"
__license__ = "GPL"
__VERSION__ = "1.00"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(version="%(prog)s version " + __VERSION__,
	description="Queries VirusTotal for a list of hashes.")
    parser.add_argument("-k", "--key", required=True, help="API key")
    parser.add_argument("-r", "--rate", type=int, default=4, help="requests per minute")
    parser.add_argument("hashFile", nargs="+", help="file with MD5 hashes of files")
    args = parser.parse_args()
    stdoutIsRedirected = S_ISREG(os.fstat(sys.stdout.fileno()).st_mode)
    hashes = []
    try:
        for fileArg in args.hashFile:
            with open(fileArg, "r") as hashFile:
                hashes += [line.split()[0].upper() for line in hashFile]
        v = virustotal.VirusTotal(args.key, limit_per_min=args.rate)
        for hash in hashes:
            if (stdoutIsRedirected):
                print("%s" % hash, file=sys.stderr)
            report = v.get(hash)
            if (report == None):
                print("%s\tNot found!" % hash)
            else:
                report.join()
                assert report.done == True
                if (report.positives > 0):
                    for scanner, malware in report:
                        if (not malware is None):
                            print("%s\t%s: %s" % (hash, scanner[0], malware))
                            break
                else:
                    print("%s\tNot found!" % hash)
            sys.stdout.flush()
    except Exception as e:
        print("Error: %s." % e, file=sys.stderr)
        sys.exit(-1)
    sys.exit(0)
