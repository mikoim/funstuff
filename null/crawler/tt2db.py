# -*- coding: utf-8 -*-

import urllib.request
import time
import pymongo
import http.client
import re

def httpWrapper(url):
    try:
        data_raw = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return "NULL"

    return data_raw

def getGirlName(data_raw):
    matches = re.findall('名前[ ]+?/[ ]+?(.+?)(|\n)*( |)*(|\n)*( |)*(\(|<br />)', data_raw)

    for match in matches[0]:
        return match.replace(' ', '')

    return

def getGrilPhotos(data_raw):
    matches = re.findall('<span>(photos/.+?.jpg)</span>', data_raw)

    if len(matches) == 0:
        matches = re.findall('<a href="(photos/.+?.jpg)">', data_raw)

    return matches

def getLastModTime(path):
    conn = http.client.HTTPConnection("twintail-japan.com")
    conn.request("HEAD", path)
    res = conn.getresponse()
    return int(time.mktime(time.strptime(res.getheaders()[2][1], '%a, %d %b %Y %H:%M:%S %Z')) * 1000)

conn = pymongo.Connection()
db = conn.tw2db
col = db.tm

for x in range(1, 3):
    baseUrl = "http://twintail-japan.com/sailor/contents/%d.html" % x
    data_raw = httpWrapper(baseUrl)

    if data_raw != "NULL":
        name = getGirlName(data_raw)

        for photo in getGrilPhotos(data_raw):
            dbtml = {'author' : '', 'time' : '', 'title' : '', 'via' : '', 'src' : '', 'message' : ''}
            dbtml['author'] = name
            dbtml['title'] = name + " @ セーラ服とツインテール"
            dbtml['via'] = baseUrl
            dbtml['message'] = ""
            dbtml['time'] = getLastModTime("/sailor/contents/%d.html" % x)
            dbtml['src'] = 'http://twintail-japan.com/sailor/contents/%s' % (photo)

            col.insert(dbtml)

    print(x)