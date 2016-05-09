from pymongo import MongoClient
import csv
import sys

lst = []

db = MongoClient().grifarm
col = db.players

for row in col.find():
    level = row['userStatus']['level']
    name = row['name']
    profile = row['userStatus']['profileMessage']
    power1 = row['offenceDeckStatus']['frontOffencePower']
    power2 = row['offenceDeckStatus']['backOffencePower']
    power3 = row['offenceDeckStatus']['frontDefencePower']
    power4 = row['offenceDeckStatus']['backDefencePower']

    if not 'guildName' in row:
        circle = ''
    else:
        circle = row['guildName']

    lst.append([level, name, circle, profile, power1 + power2, power3 + power4, power1 + power2 + power3 + power4])

print('レベル,名前,所属サークル,プロフィール,総攻撃力,総防御力,総戦力')

cw = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

for row in sorted(lst, key=lambda x: x[6], reverse=True):
    cw.writerow(row)