#Various tools for processing the wlscrape.py output

##genreport.py

The script takes two arguments on the command line. The first argument is a JSON-formatted file that has been created by saving the standard output of `wlscape.py`. The second argument is a file, containing a list of MD5 hashes (one per line; only the first word on the line is used) that have been determined to be malware known to at least one of the scanners used by [VirusTotal](https://www.virustotal.com/). The script outputs a markdown-formatted table, ready to be included in a [GitHub report](https://github.com/bontchev/wlscrape/blob/master/malware.md).

##getnotfound.py

The script takes two arguments on the command line. The first argument is a JSON-formatted file that has been created by saving the standard output of `wlscape.py`. The second argument is a file, containing a list of MD5 hashes (one per line; only the first word on the line is used), the malicious status of which is not known to [VirusTotal](https://www.virustotal.com/) (either because they have never been submitted for scanning, or because none of the scanners detects anything in them). Such a list of hashes is one of the files (the one whose name begins with `NOTFOUND_`), produced by [VTScan](https://github.com/hasherezade/mal_sort/tree/master/vtscan). If an MD5 hash is present more than once, the additional ones are ignored. The script then downloads these files from the [Wikileaks](https://www.wikileaks.org) site for manual examination. If the `-e` option is used, it must be followed by an integer number `N`, greater than zero. Then the downloaded files will be split into subdirectories (named `000`, `001`, etc.), with no more than `N` files per subdirectory. If no option is specified, the files are downloaded to the current directory.

##getsize.py

The script takes as one or more arguments on the command line JSON-formatted files that have been created by saving the standard output of `wlscrape.py`. It outputs the number of files on the [Wikileaks](https://www.wikileaks.org) site that are listed in the JSON data, as well as their total size. This is useful to plan how much free disk space one would need before starting to download these files.

##listmd5s.py

The script takes as one or more arguments on the command line JSON-formatted files that have been created by saving the standard output of `wlscrape.py`. It outputs only the MD5 hash of each entry, one hash per line, converted to upper case, ready for [VTScan](https://github.com/hasherezade/mal_sort/tree/master/vtscan) to submit them to [VirusTotal](https://www.virustotal.com/). The result is equivalent to running `wlscrape.py` with the option `--md5only` (or `-m`) but this script is handy if you have already run `wlscrape.py`, have produced JSON-formatted data, and need just the list of MD5 hashes without having to scrape the [Wikileaks](https://www.wikileaks.org) site again.

#wlget.py

The script takes as one or more arguments on the command line JSON-formatted files that have been created by saving the standard output of `wlscrape.py`. It downloads the files from the [Wikileaks](https://www.wikileaks.org) site that are described in the JSON data. This script is useful when you have already obtained the necessary JSON-formatted file information by running `wlscrape.py` with the appropriate options and want to just download the files, without searching the [Wikileaks](https://www.wikileaks.org) site again. If two or more entries share the same MD5 hash, only the first one will be used. If the `-e` option is used, it must be followed by an integer number `N`, greater than zero. Then the downloaded files will be split into subdirectories (named `000`, `001`, etc.), with no more than `N` files per subdirectory. If no option is specified, the files are downloaded to the current directory.
