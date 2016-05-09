import MeCab
import os
import json
import re


def parse(row):
    pair = row.split(',')[0].split('\t')

    if len(pair) == 2 and pair[1] in ['名詞', '動詞']:
        return pair[0]

    return None


def judge(row):
    return 'type' in row and 'user' in row and row['type'] == 'message' and len(row['text']) >= 2


words = {}
users = {}

regex = re.compile('\d+-\d+-\d+.json')

for row in json.load(open('users.json')):
    if 'is_bot' in row and not row['is_bot']:
        users[row['id']] = row['name']

for root, _, filenames in os.walk('data'):

    for filename in filter(lambda x: regex.match(x), filenames):
        filename = os.path.join(root, filename)

        daily = json.load(open(filename))

        for post in filter(judge, daily):
            user = post['user']

            if user in words:
                words[user] += 1
            else:
                words[user] = 1

result = []

for key, val in words.items():
    if key in users:
        result.append({'text': users[key], 'size': val})

print(result)
