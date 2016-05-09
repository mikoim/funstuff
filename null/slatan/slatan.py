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

regex = re.compile('\d+-\d+-\d+.json')

for root, _, filenames in os.walk('data'):

    for filename in filter(lambda x: regex.match(x), filenames):
        filename = os.path.join(root, filename)

        daily = json.load(open(filename))

        for post in filter(judge, daily):

            m = MeCab.Tagger()

            for word in filter(lambda x: x, map(parse, m.parse(post['text']).split('\n'))):

                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

result = []

for key, val in words.items():
    if val > 5:
        result.append({'text': key, 'size': val})

print(result)
