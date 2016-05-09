import re
import urllib.request, json
import time

def httpWrapper(url):
    try:
        data_raw = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return "NULL"

    return data_raw

def getMediaTl(twitter):
    ids = []

    for tweet in re.findall("twitter.com/(.+)/status/([0-9]+)", httpWrapper('https://twitter.com/%s/media' % twitter)):
        ids.append(int(tweet[1]))

    max_id = ids[len(ids) - 1];

    while 1:
        res_raw = httpWrapper('https://twitter.com/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_id=%d' % (twitter, max_id))

        try:
            res = json.loads(res_raw)
        except:
            print(res_raw)
            time.sleep(5)
            res_raw = httpWrapper('https://twitter.com/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_id=%d' % (twitter, max_id))
            res = json.loads(res_raw)

        if res['has_more_items'] == False:
            break

        for tweet in re.findall("twitter.com/(.+)/status/([0-9]+)", res['items_html']):
            ids.append(int(tweet[1]))

        max_id = int(res['max_id'])

    return ids

users = ['a']

for user in users:
    for twid in getMediaTl(user):
        print(twid)
