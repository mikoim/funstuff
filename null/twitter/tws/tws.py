from pymongo import MongoClient, errors

import tweepy


class Tws:
    def __init__(self, keyword):
        self.tweets = MongoClient().tws.tweets
        self.auth = tweepy.AppAuthHandler('',
                                          '')
        self.api = tweepy.API(self.auth)

        self.keyword = keyword

    def get_past(self):
        while True:
            counter = 0
            res = self.api.search(q=self.keyword, count=100, max_id=self.tweets.find().sort('id', 1)[0]['id'])

            if len(res) is 0:
                break

            print(len(res))

            for tweet in res:
                try:
                    self.tweets.insert(tweet._json)
                except errors.DuplicateKeyError:
                    print('Duplicate key.')
                    counter += 1

            if counter > 1:
                break

    def get_recently(self):
        first = True
        max_id = 0

        while True:
            counter = 0

            if first:
                res = self.api.search(q=self.keyword, count=100)
                first = False
            else:
                res = self.api.search(q=self.keyword, count=100, max_id=max_id)

            if len(res) is 0:
                break

            print(len(res))

            for tweet in res:
                try:
                    self.tweets.insert(tweet._json)
                    max_id = tweet.id
                except errors.DuplicateKeyError:
                    print('Duplicate key.')
                    counter += 1

            if counter > 99:
                break


if __name__ == '__main__':
    tws = Tws('A OR B')
    tws.get_recently()
