from grifarm import *

if __name__ == '__main__':
    c = Client()

    if c.check_version() and c.handshake1() and c.handshake2() and c.user_home() and c.pvp_home():
        c.gift_open()
