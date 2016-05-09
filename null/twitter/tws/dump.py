from pymongo import MongoClient

tweets = MongoClient().tws.tweets

for i in tweets.find(
        {
            '$and': [
                {'id': {'$gt': 541479240785346561}},
                {'entities.media': {'$exists': True}},
                {'retweeted': False}
            ]
        }
):
    tweet_id = i['id']

    for j in i['entities']['media']:
        url = j['media_url']
        ext = url.split('/')[-1].split('.')[-1]
        print('curl -o {:d}.{:s} {:s}:orig'.format(tweet_id, ext, url))
