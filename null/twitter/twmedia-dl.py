import re
import json
import time
import sys

import httplib2
from twitter import *
import magic


class TwitterMediaDL:
    http = httplib2.Http(".cache")
    baseUrl = "https://twitter.com"

    consumer_key = ""
    consumer_secret = ""
    access_token_key = ""
    access_token_secret = ""

    t = Twitter(auth=OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret))
    remaining = None

    def http_wrapper(self, uri):
        resp, content = self.http.request(
            uri=uri, method='GET'
        )

        return content

    def get_medias(self, nickname):
        ids = []

        for tweet in re.findall("twitter.com/(.+)/status/([0-9]+)",
                                self.http_wrapper(self.baseUrl + '/%s/media' % nickname).decode()):
            ids.append(int(tweet[1]))

        max_id = ids[len(ids) - 1]

        while 1:
            res_raw = self.http_wrapper(
                self.baseUrl + '/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_id=%d' % (
                    nickname, max_id)).decode()

            try:
                res = json.loads(res_raw)
            except:
                print(res_raw)
                time.sleep(5)
                res_raw = self.http_wrapper(
                    self.baseUrl + '/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_id=%d' % (
                        nickname, max_id)).decode()
                res = json.loads(res_raw)

            if not res['has_more_items']:
                break

            for tweet in re.findall("twitter.com/(.+)/status/([0-9]+)", res['items_html']):
                ids.append(int(tweet[1]))

            max_id = int(res['max_id'])

        return list(set(ids))

    def get_image_url(self, tweet_id):
        lst = []

        if self.remaining is None or self.remaining % 10 is 0 or self.remaining <= 1:
            self.check_limit()

        r = self.t.statuses.show(_id=tweet_id, _method='GET')
        self.remaining -= 1

        print('{:d}\t{:d}\t{:s}'.format(tweet_id, self.get_unix_epoch(r['created_at']), r['text']))

        for m in r['entities']['media']:
            lst.append(m['media_url'] + ':orig')

        return lst

    def check_limit(self):
        r = self.t.application.rate_limit_status(_method='GET')['resources']['statuses']['/statuses/show/:id']
        self.remaining = r['remaining']

        print("API Limit : {:d} / {:d} = {:f}".format(r['remaining'], r['limit'], r['remaining'] / r['limit']),
              file=sys.stderr)

        if r['remaining'] / r['limit'] < 0.10:
            reset = r['reset'] - time.time()
            print("Please wait... {:f}".format(reset), file=sys.stderr)
            time.sleep(reset + 10)

    @staticmethod
    def get_file_extension(binary):
        mime = magic.from_buffer(binary, True).decode()
        return mime.split('/')[1]

    @staticmethod
    def get_unix_epoch(created_at):
        return int(time.mktime(time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")))

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        tw = TwitterMediaDL()

        for tweetID in tw.get_medias(sys.argv[i]):
            list_url = tw.get_image_url(tweetID)

            for j in range(0, len(list_url)):
                raw = tw.http_wrapper(list_url[j])
                ext = tw.get_file_extension(raw)

                with open('{:d}_{:d}.{:s}'.format(tweetID, j, ext), 'wb') as f:
                    f.write(raw)
