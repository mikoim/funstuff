# -*- coding: utf-8 -*-

import json
import urllib.request
import time
import pymongo
import http.client

def httpWrapper(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def getUnixEpoch():
    return int(time.time() * 1000)

def getGirlList():
    i = 0
    baseUrl = "http://tokimeki-calendar.com/api/mobile/girl_list_api/search?name=&age_range=&height_range=&blood=&page="
    girls = []

    while True:
        data_raw = httpWrapper(baseUrl + str(i) + "&_=" + str(getUnixEpoch()))
        data_json = json.loads(data_raw, encoding='utf-8')

        if data_json['code'] != '0' or data_json['auth'] != '0' or len(data_json['girl_list']) == 0:
            break

        for girl in data_json['girl_list']:
            girls.append(girl)

        i += 1

    return girls

def getGirlInfo(girl_id):
    baseUrl = "http://tokimeki-calendar.com/api/mobile/plus_contents_api/girl?girl_id="

    data_raw = httpWrapper(baseUrl + girl_id + "&_=" + str(getUnixEpoch()))
    data_json = json.loads(data_raw, encoding='utf-8')

    return data_json

def getGrilPhotos(girlInfo):
    photos = []

    for photo in girlInfo['images'][0]:
        photos.append(photo)

    return photos

def getLastModTime(path):
    conn = http.client.HTTPConnection("tokimeki-calendar.com")
    conn.request("HEAD", path)
    res = conn.getresponse()
    return int(time.mktime(time.strptime(res.getheaders()[4][1], '%a, %d %b %Y %H:%M:%S %Z')) * 1000)

conn = pymongo.Connection()
db = conn.tw2db
col = db.tm

girls = getGirlList()

for girl in girls:

    info = getGirlInfo(girl['girl_id'])
    photos = getGrilPhotos(info)

    girl_id = info['girl_id']
    name = info['name']
    hitocome = info['hitocome']

    for photo in photos:
        dbtml = {'author':'', 'time':'', 'title':'', 'via':'', 'src':'', 'message':''}
        dbtml['author'] = name
        dbtml['title'] = name + " @ tokimeki girl"
        dbtml['via'] = 'http://tokimeki-calendar.com/mobile/tokimeki-girl.html?id=' + girl_id
        dbtml['message'] = hitocome
        dbtml['time'] = getLastModTime("/" + photo)
        dbtml['src'] = 'http://tokimeki-calendar.com/%s' % (photo)
        col.insert(dbtml)
