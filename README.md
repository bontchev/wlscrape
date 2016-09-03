#WLScrape.py - A tool for scrapping the possible malware from the Wikileaks AKP leak

##Introduction

[Wikileaks](https://www.wikileaks.org) has released a large set of e-mails leaked from the Turkish party AKP. Unfortunately, no processing of any kind has been performed on these e-mails - they are just a raw dump. Since many of the AKP members have been recipients of malware sent by e-mail (most likely random spam but could have also been targeted attacks), the received malware in the e-mails is also present in the dump. As a result, the Wikileaks site is hosting malware. For the record, I consider this to be extremely irresponsible from the part of Wikileaks. Malware distribution is __not__ "journalism" by _any_ definition of the term.

This script was written for the purpose of getting information about the attached files with suspicious extensions, so that they could be scanned - either by downloading them and scanning them locally, or by obtaining their MD5 hashes and submitting those to [VirusTotal](https://www.virustotal.com/).

##Installation

The script should work both in Python 2.6+ and 3.x, although I've been using it only with Python 2.7.6. It depends on the several Python modules, some which are not part of the default installation, so they will have to be installed before the script is able to run. They can all be installed via the command

	pip install module_name

If you are on Linux and want to install the module system-wide, use

	sudo pip install module_name

In particular, the following modules have to be installed:

	lxml
	argparse
	requests
	json
	wget
	sys
	os

In addition, if the script produces bizarre `InsecurePlatform` errors, you should run the command

	pip install "requests[security]"

The above is for Windows. If you use a different command shell (e.g., `bash` or `zsh` on Linux), you might need to escape the brackets in a different way, e.g.

	sudo pip install requests\[security\]

On some Linux systems this might not be enough. If, after doing it, you're still getting bizarre SSL-related errors, run the following command:

	sudo pip install pyopenssl ndg-httpsclient pyasn1 --upgrade

##Usage

The script takes as a command-line argument one or more file extensions. It fetches information from the Wikileaks site (and the AKP e-mail dump area on it, in particular) about the e-mail file attachments matching these extensions. By default, it outputs a JSON array containing the URL where the file resides, the MD5 hash of the file, and the extension of the file.

Suggested extensions that might contain malware are: `docm`, `exe`, `jar`, `ace`, `arj`, `cab`, `gz`, `js`, `pps`, `ppt`, `rar`, `rtf`, `pdf`, `zip`. Attention: the `pdf` and `zip` extensions will result in thousands of files!

###Command-line options

`-h`, `--help`	Displays a short explanation how to use the script and what the command-line options are.

`-v`, `--version`	Displays the version of the script.

`-m`, `--md5only`	Instead of a JSON array, the script outputs only the MD5 hashes of the files, one per line, in upper case.

`-d`, `--download`	The script downloads the files that match the specified extension(s). The files are saved in the with a name equal to their MD5 hash in upper case (and not the original name in the e-mail attachment, in order to prevent different files with the same names from overwriting each other) and extension equal to the matching extension. If there are duplicated files, `(N)` will be appended to the file name, where `N` is the duplicate number. The files are saved in the current directory if there is only one page of search results, or in subdirectories named `000`, `001`, etc., one subdirectory per page of search results. 

`-s`, `--spam`	Look for the specified file extension(s) in the spam folder, too.

`-p`, `--duplicates`	Search the duplicated e-mails too, whatever Wikileaks means by that.

`-u`, `--unique`	Retrieve only the entries unique by MD5.

`-e`, `--elements` N	Number of elements per results page. Must be in the range of [10,200]. Default is 200. Makes sense to use it only with the `-d` option; it will determine the number of downloaded files per subdirectory.

`-b`, `--blacklist` `BLACKLiST`	Specify a file (`BLACKLIST`) containing one URL per line. The links with these URLs will be ignored.

`-a`, `--pages` `PAGES` Specify a list of ranges (e.g., 2-5,7,9-10) of search result pages to process.

##Change log

Version 1.00:	Initial version.

Version 1.01:	Wikileaks changed slightly the format of the page and the script was able to process only the first page of a multi-page output. Fixed.

Version 1.02:	Implemented the option to check the e-mails marked as spam too.

Version 1.03:	Removed the code that was ignoring the duplicate files, since the idea is to find _all_ links on the Wikileaks site that contain malware. Added the option to search the duplicated e-mails too, whatever Wikileaks means by that. Added the option to specify a list of links to ignore (e.g., because they no longer point to malware).

Version 1.04:	Implemented the option to retrieve only files unique by MD5. If there is more than one, only the first one found will be listed. Implemented the option to specify which pages of the search results to process. Implemented the option to specify the number of entries per page of search results.
