import re
import urllib.request, json

def httpWrapper(url):
    try:
        data_raw = urllib.request.urlopen(url).read().decode('gbk')
    except:
        return "NULL"

    return data_raw

def getPhotos(url):
    photos = []

    for photo in re.findall('data-lazyload-src="(.+?)"', httpWrapper(url)):
        photos.append(photo)

    return photos

urls = ["http://pp.163.com/sakurakyon/pp/10831234.html"]

for url in urls:
    for photo in getPhotos(url):
        print(photo)
