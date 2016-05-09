from grifarm import *
import csv
import sys

if __name__ == '__main__':
    c = Client()

    lst = []

    if c.check_version() and c.handshake1() and c.handshake2() and c.user_home() and c.pvp_home():
        members = c.get_circle_member("")

        for row in members:
            level = row['userStatus']['level']
            name = row['name']
            power1 = row['offenceDeckStatus']['frontOffencePower']
            power2 = row['offenceDeckStatus']['backOffencePower']
            power3 = row['offenceDeckStatus']['frontDefencePower']
            power4 = row['offenceDeckStatus']['backDefencePower']

            lst.append([level, name, power1 + power2 + power3 + power4])

    print('レベル,名前,総戦力')

    cw = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

    for row in sorted(lst, key=lambda x: x[2], reverse=True):
        cw.writerow(row)
