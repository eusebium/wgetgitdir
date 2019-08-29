#!/usr/bin/env python3
# -*- Coded By SadCode + Eus -*-

import re
import os
import urllib.request
import sys
import signal
import argparse
import json

# this ansi code lets us erase the current line
ERASE_LINE = "\x1b[2K"


def create_url(url):
	"""
	modifying the given url so that it returns JSON data when
	we do a GET requests later in this script
	"""

	# extract the branch name from the given url (e.g master)
	branch = re.findall(r"\/tree\/(.*?)\/", url)[0]
	
	api_url = url.replace("https://github.com", "https://api.github.com/repos")
	api_url = re.sub(r"\/tree\/.*?\/", "/contents/", api_url)
	api_url = api_url+"?ref="+branch

	return api_url


def get_files_and_dirs(api_url):
	r = urllib.request.urlretrieve(api_url)
	with open(r[0], "r") as f:
		raw_data = f.read()
	data = json.loads(raw_data)

	for _, file in enumerate(data):
		file_url = file["download_url"]
		path = file["path"]
		type = file["type"]
		dir_url = file["url"]

		if type == "file":
			download_file(file_url, path)
		else:
			os.makedirs(path, exist_ok=True)
			get_files_and_dirs(dir_url)


def download_file(file_url, path):
	try:
		urllib.request.urlretrieve(file_url, path)
	except:
		print('An error occured.')


def main():
	# disable CTRL+Z
	signal.signal(signal.SIGTSTP, signal.SIG_IGN)

	parser = argparse.ArgumentParser(description = "Download directories/folders from GitHub")
	parser.add_argument('url', action="store")

	args = parser.parse_args()

	repo_url = args.url

	download_dir = repo_url.split("/")[-1]

	os.makedirs(download_dir, exist_ok=True)

	# generate the url which returns the JSON data
	api_url = create_url(repo_url)

	# get files and directories
	get_files_and_dirs(api_url)

if __name__=="__main__":
	main()
