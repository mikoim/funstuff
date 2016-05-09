from grifarm import *


def get_portion():
    zz = Client()

    flag = False

    for i in range(10):
        zz.check_version()
        zz.handshake1()
        zz.handshake2()
        zz.user_home()

        if flag:
            flag = False
            zz.set_version("1.1.0")
        else:
            flag = True
            zz.set_version("1.0.9")


if __name__ == '__main__':
    c = Client()

    if c.check_version() and c.handshake1() and c.handshake2() and c.user_home() and c.pvp_home():
        while True:

            while c.produce_quest_do(660, 2, 10):
                pass
            print('')

            c.mission_do()

            try:
                c.use_item()
            except Exception:
                get_portion()
                c.gift_open(10)