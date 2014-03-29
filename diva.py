#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# This script will compile a list of mp4 files for direct downloading of all
# recent broadcasts by The디바 at http://afreeca.com/vol33lov

import math, os, re, urllib2

# parses index and returns list of videos
def getindex():
	print "* Getting Index"
	index_url = urllib2.urlopen('http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?nStationNo=3292082&szBbsType=REVIEW')
	index_html = index_url.read()
	index_url.close()

	# determine number of pages
	pages = re.findall(r'<a href="#" onclick="goListPage\((\d+)\)">\d+</a>', index_html)
	pages = max(map(int, pages))
	print "** Found "+ str(pages) +" pages"

	# get videos on first page
	vids = re.findall(r"szBjId=vol33lov&nStationNo=(\d+)&nBbsNo=(\d+)&nTitleNo=(\d+)", index_html)

	# get videos on each additional page
	for page in range(2, pages+1):
		print "* Getting page "+ str(page)
		page_url = urllib2.urlopen('http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?nStationNo=3292082&szBbsType=REVIEW&nPageNo='+ str(page))
		page_html = page_url.read()
		page_url.close()
		matches = re.findall(r"szBjId=vol33lov&nStationNo=(\d+)&nBbsNo=(\d+)&nTitleNo=(\d+)", page_html)
		vids.extend(matches)

	# clear duplicates
	vids = list(set(vids))

	print "* Found "+ str(len(vids)) +" videos"

	return vids

# gets direct download URLs for video
def getvidurls(vid):
	print "* Getting video URLs: "+ str(vid)
	urls = []
	vid_url = urllib2.urlopen('http://afbbs.afreeca.com:8080/app/read_ucc_bbs.cgi?szBjId=vol33lov&nStationNo='+ vid[0] +'&nBbsNo='+ vid[1] +'&nTitleNo='+ vid[2])
	vid_html = vid_url.read()
	vid_url.close()

	# get date and id
	link = re.search(r"rowKey=(?P<date>\d+)_(?P<id>\d+)", vid_html)
	
	# get length in seconds to determine number of parts
	length = re.search(r"<span class=\"date\">(?P<h>\d+):(?P<m>\d+):(?P<s>\d+)", vid_html)
	length = float(int(length.group('h'))*60*60 + int(length.group('m'))*60 + int(length.group('s')))
	
	# parts are usually about an hour
	parts = int(math.ceil(length/60/60))

	vid_date = link.group('date')
	vid_id = link.group('id')
	# dir name always seems to be last three digits of vid_id
	vid_dir = vid_id[-3:]

	# afreeca content server hardcoded as of now, there might several others
	# available, however
	for part in range(1, parts+1):
		urls.append('http://101.79.252.143/vod/'+ vid_date +'/'+ vid_dir +'/'+ vid_id +'_'+ str(part) +'.mp4')
	
	print "** "+ str(urls)

	return urls

# compile and write download list of all video URLs
def writelist(index):
	dlurls = []
	for vid in index:
		urls = getvidurls(vid)
		dlurls.extend(urls)
	print "* Writing download list: download.list"
	dllist = open('download.list', 'w')
	for url in dlurls:
		print >> dllist, url
	dllist.close()
	
index = getindex()
writelist(index)
print "*** RUN: wget -c -i download.list"
print "*** ∩( ・ω・)∩ OMNOMNOM~"
