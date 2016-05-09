from grifarm import *

if __name__ == '__main__':
    c = Client()

    if c.check_version() and c.handshake1() and c.handshake2() and c.user_home() and c.pvp_home():
        while True:
            if c.get_user_battle_point() == 0 and c.get_user_quest_point() < 30:
                print('Sleeping... 900 seconds')
                time.sleep(900)

                if not c.user_home() or not c.pvp_home():  # Update PVP status
                    break

            c.show_status()

            while c.pvp_do():
                pass
            print('')

            while c.quest_do(7, 4):
            #while c.produce_quest_do(528, 4, 10):
                pass
            print('')

            c.mission_do()
