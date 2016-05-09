from grifarm import *

lst = []

db = MongoClient().grifarm
col = db.players

for row in col.find():
    frontOffencePower = row['offenceDeckStatus']['frontOffencePower']
    backOffencePower = row['offenceDeckStatus']['backOffencePower']

    frontDefencePower = row['offenceDeckStatus']['frontDefencePower']
    backDefencePower = row['offenceDeckStatus']['backDefencePower']

    power = frontOffencePower + backOffencePower + frontDefencePower + backDefencePower

    if 'guildName' not in row and power > 600000:
        lst.append(row['userStatus']['userId'])

c = Client()
if c.check_version() and c.handshake1() and c.handshake2() and c.user_home() and c.pvp_home():
    for player_id in lst:
        try:
            c.invite_player(player_id)
        except Exception:
            c.check_version()
            c.handshake1()
            c.handshake2()
            c.user_home()