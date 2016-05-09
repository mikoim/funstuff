from pymongo import MongoClient
import csv
import sys

lst = {}
l = []
db = MongoClient().grifarm
col = db.players

for row in col.find():
    power1 = row['offenceDeckStatus']['frontOffencePower']
    power2 = row['offenceDeckStatus']['backOffencePower']
    power3 = row['offenceDeckStatus']['frontDefencePower']
    power4 = row['offenceDeckStatus']['backDefencePower']

    if 'guildName' not in row:
        continue
    else:
        circle = row['guildName']
        if circle in lst:
            lst[circle] += power1 + power2 + power3 + power4
        else:
            lst[circle] = power1 + power2 + power3 + power4

for i, v in lst.items():
    l.append([i, v])

print('サークル,総戦力')

cw = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

for row in sorted(l, key=lambda x: x[1], reverse=True):
    cw.writerow(row)