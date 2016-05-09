from datetime import datetime
import time
import inspect
import json

import httplib2  # Before use, you must apply patch for fixing SSL host validation bug.
from pymongo import MongoClient


class Client:
    def __init__(self):
        self.http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        self.db = MongoClient().grifarm

        self.version = ''
        self.user_agent = ''.format(
            self.version)

        self.headers = {
            'Content-Type': 'application/json',
            'X-Accept-Timezone': 'GMT+99:00',
            'User-Agent': self.user_agent
        }

        self.api_base = ''

        # Basic configuration
        self.token = 'dummy'  # Don't edit this entry
        self.user_id = ''  # Enter your user id
        self.session_key = ''  # Grab your session key from sniffer

        # For simulating official client behavior
        self.master_resource_version = None
        self.image_resource_version = None
        self.sound_resource_version = None
        self.ccbi_resource_version = None
        self.school_resource_version = None
        self.master_data_version = None

        self.character_id = None

        self.user_name = None
        self.user_level = None

        self.user_quest_point_max = None
        self.user_quest_recovery_time = None

        self.user_pvp_rank = None
        self.user_pvp_point = None
        self.user_pvp_point_recovery_time = None
        self.user_pvp_offense_win_count = None
        self.user_pvp_offense_lose_count = None
        self.user_pvp_defense_win_count = None
        self.user_pvp_defense_lose_count = None
        self.user_pvp_consecutive_win_count = None

        self.pvp_battle_type = None

        self.user_quest_list = []

    def get_user_quest_point(self):
        return int(self.user_quest_point_max - (128 * (-time.time() + self.user_quest_recovery_time) / 7536))

    def get_user_battle_point(self):
        return self.user_pvp_point

    def set_user_quest_recovery_time(self, string):
        self.user_quest_recovery_time = self.get_epoch_from_iso(string)
        return

    def get_epoch_from_iso(self, string):
        return int(time.mktime(time.strptime(string, "%Y-%m-%dT%H:%M:%S"))) - time.timezone

    def set_version(self, version):
        self.version = version

    def show_status(self, show_user=True, show_quest=True, show_pvp=True):
        if show_user:
            print('\n==== User ====')
            print('Name : {:s}\nLevel : {:d}\nQP : {:d}/{:d}\nBP : {:d}/5'.format(
                self.user_name,
                self.user_level,
                self.get_user_quest_point(),
                self.user_quest_point_max,
                self.get_user_battle_point()
            ))

        if show_quest:
            print('\n==== Quest ====')
            for quest in self.user_quest_list:
                print('Chapter {:d}\n  Clear : {:d}\n  Current Area : {:d}'.format(
                    quest['chapterId'], quest['clearCount'], quest['currentQuestAreaId']
                ))

        if show_pvp:
            print('\n==== PVP ====')
            print(
                'Rank : {:d}\nConsecutive Win: {:d}勝\nOffense : {:d}勝 {:d}敗 => {:.5f}\nDefense : {:d}勝 {:d}敗 => {:.5f}'.format(
                    self.user_pvp_rank,
                    self.user_pvp_consecutive_win_count,
                    self.user_pvp_offense_win_count, self.user_pvp_offense_lose_count,
                    self.user_pvp_offense_win_count / self.user_pvp_offense_lose_count,
                    self.user_pvp_defense_win_count, self.user_pvp_defense_lose_count,
                    self.user_pvp_defense_win_count / self.user_pvp_defense_lose_count
                ))

        print('')

        return

    def check_version(self):
        body = {
            'os': 2,
            'appVersion': self.version
        }

        resp, content = self.http.request(uri=self.api_base + '/version/status/', method='POST', headers=self.headers,
                                          body=json.dumps(body))

        if resp['status'] != '200':
            print('check_version : Error {:d}'.format(resp['status']))
            return False

        if json.loads(content.decode())['versionStatus'] == 0:
            print('check_version : Latest version may be released!')
            return False

        return True

    def parse_response_header(self, resp):
        self.master_resource_version = resp['masterResourceVersion']
        self.image_resource_version = resp['imageResourceVersion']
        self.sound_resource_version = resp['soundResourceVersion']
        self.ccbi_resource_version = resp['ccbiResourceVersion']
        self.school_resource_version = resp['schoolResourceVersion']
        self.master_data_version = resp['masterDataVersion']

        self.token = resp['token']

        return

    def make_request_body(self, additional=None):
        body = {
            "appVersion": self.version,
            "userId": self.user_id,
            "sessionkey": self.session_key,
            "language": "ja",
            "os": 2,
            "osVersion": "",
            "device": "",
            "requestTimestamp": datetime.utcnow().replace(microsecond=0).isoformat(),
            "token": self.token
        }

        if additional:
            body.update(additional)

        return json.dumps(body)

    def handshake1(self):
        resp = self.http_wrapper('/tutorial/progress/get/', body=self.make_request_body())

        self.parse_response_header(resp)
        self.character_id = resp['characterId']

        return True

    def handshake2(self):
        resp = self.http_wrapper('/data/gamestart/get2/',
                                 body=self.make_request_body({"masterDataVersion": self.master_data_version}))

        self.user_name = resp['user']['iuser']['name']
        self.user_level = resp['user']['iuserStatus']['level']

        self.user_quest_point_max = resp['user']['iuserStatus']['maxVital']
        self.set_user_quest_recovery_time(resp['user']['iuserStatus']['maxVitalRecoveryTime'])

        for quest in resp['user']['iuserQuest']:
            self.user_quest_list.append(quest)

        self.user_quest_list = sorted(self.user_quest_list, key=lambda x: x['chapterId'])

        return True

    def user_home(self):
        resp = self.http_wrapper('/mypage/top/', body=self.make_request_body())

        self.user_pvp_point = resp['pvpBp']
        self.user_pvp_point_recovery_time = self.get_epoch_from_iso(resp['pvpBpMaxRecoveryTime'])

        return True

    def pvp_home(self):
        resp = self.http_wrapper('/pvp/top/get/', body=self.make_request_body())

        self.user_pvp_rank = resp['pvpUser']['pvpRank']
        self.user_pvp_consecutive_win_count = resp['pvpUser']['offenseConsecutiveWinCount']
        self.user_pvp_offense_win_count = resp['pvpUser']['offenseWinCountSum']
        self.user_pvp_offense_lose_count = resp['pvpUser']['offenseLoseCountSum']
        self.user_pvp_defense_win_count = resp['pvpUser']['defenseWinCountSum']
        self.user_pvp_defense_lose_count = resp['pvpUser']['defenseLoseCountSum']
        self.pvp_battle_type = resp['pvpBattleType']

        return True

    def pvp_do(self, target_user_id=None):
        if self.user_pvp_point == 0:
            print('pvp_do : PVP point is zero.')
            return False

        if self.user_pvp_rank >= 8:
            print('pvp_do : PVP rank is too high.')
            # return False

        if target_user_id is None:
            for i in range(1000):
                resp = self.http_wrapper('/pvp/targets/matching/',
                                         body=self.make_request_body({"pvpBattleType": self.pvp_battle_type}))

                for user in resp['matchingPvpTargetUserList']:
                    profile = self.get_player_profile(user['userId'])
                    if profile is None:
                        power = 9999999999
                    else:
                        power = profile['offenceDeckStatus']['frontTotalPower'] + profile['offenceDeckStatus'][
                            'backTotalPower']

                    if 550000 > power > 300000:
                        print('pvp_do : duck found. [{:s} [{:d}] / {:d}勝 {:d}敗]'.format(
                            user['name'], user['userId'], user['defenseWinRankCount'], user['defenseLoseRankCount']
                        ))
                        if profile is not None:
                            print('{:s} [Lv{:d}] : {:d}'.format(profile['name'], profile['userStatus']['level'], power))
                        target_user_id = user['userId']
                        break

                if target_user_id is not None:
                    break

            time.sleep(1)

        if target_user_id is None:
            print('pvp_do : duck NOT found.')
            return False

        # Part 2
        resp = self.http_wrapper('/pvp/battle/execute/',
                                 body=self.make_request_body({"targetUserId": target_user_id, "pvpBattleType": 1}))

        self.user_pvp_rank = resp['pvpUser']['pvpRank']
        self.user_pvp_consecutive_win_count = resp['pvpUser']['offenseConsecutiveWinCount']
        self.user_pvp_offense_win_count = resp['pvpUser']['offenseWinCountSum']
        self.user_pvp_offense_lose_count = resp['pvpUser']['offenseLoseCountSum']
        self.user_pvp_defense_win_count = resp['pvpUser']['defenseWinCountSum']
        self.user_pvp_defense_lose_count = resp['pvpUser']['defenseLoseCountSum']

        self.user_pvp_point -= 1

        if resp['win']:
            print('pvp_do : Win!')
        else:
            print('pvp_do : Lose!')

        return True

    def quest_do(self, chapter_id=6, chapter_type=1):
        if len(self.user_quest_list) < chapter_id:
            print('quest_do : chapter_id is invalid. {:d} <= {:d}'.format(chapter_id, len(self.user_quest_list)))
            return False

        if self.get_user_quest_point() < 30:
            print('quest_do : Quest point is low. {:d} < 30'.format(self.get_user_quest_point()))
            return False

        self.http_wrapper('/quest/start/', body=self.make_request_body({"chapterId": chapter_id}))

        # Part 2 - n
        while self.get_user_quest_point() >= 5:
            print('quest_do : Go! Go! Go!')

            resp = self.http_wrapper('/quest/area/execute/', body=self.make_request_body({
                "chapterId": chapter_id, "chapterType": chapter_type,
                "questAreaId": self.user_quest_list[chapter_id - 1]['currentQuestAreaId']
            }))

            self.set_user_quest_recovery_time(resp['questResult']['userInfo']['userStatus']['maxVitalRecoveryTime'])
            self.user_quest_list[chapter_id - 1]['currentQuestAreaId'] = resp['questResult']['userInfo']['userQuest'][
                'currentQuestAreaId']

            if 'normalResult' in resp['questResult']:  # Normal result
                for result in resp['questResult']['normalResult']['setList']:
                    if result['setType'] == 'NORMAL_SET':  # Unknown
                        pass

                    elif result['setType'] == 'EVENT_LV_UP':  # Level up
                        print('quest_do : Level up. {:d} -> {:d}'.format(result['userLevel'] - 1, result['userLevel']))
                        self.user_quest_point_max = result['userMaxVital']
                        self.set_user_quest_recovery_time(result['userMaxVitalRecoveryTime'])
                        self.user_level = result['userLevel']
                        return True

                    elif result['setType'] == 'EVENT_DROP':  # Drop item
                        print('quest_do : Item dropped. {:d}x{:d}個'.format(
                            result['dropRewardId'], result['dropRewardCount']
                        ))

                    elif result['setType'] == 'EVENT_VITAL_LIMIT':  # Quest point is low
                        if result['userVital'] < 5:
                            print('quest_do : Quest point is low. {:d} < 5'.format(result['userVital']))
                            return False
                        else:
                            print('quest_do : Server says Quest point is low... it wrong! {:d} >= 5'.format(
                                result['userVital']))
                            return False

            elif 'bossResult' in resp['questResult']:  # Boss result
                pass

    def mission_do(self):
        resp = self.http_wrapper('/map/status/', body=self.make_request_body({"mapId": 1}))

        for mission in resp['missionList']:
            mission_type = mission['missionType']
            mission_id = mission['missionId']

            if mission['status'] == 0:  # Accept
                print('mission_do : {:d}:{:d} - Accept'.format(mission_type, mission_id))
                self.http_wrapper('/map/accept/', body=self.make_request_body(
                    {
                        "missionType": mission_type,
                        "missionId": mission_id
                    }
                ))
            elif mission['status'] == 1:  # In progress
                print('mission_do : {:d}:{:d} - In progress'.format(mission_type, mission_id))
                pass
            elif mission['status'] == 2:  # Clear
                print('mission_do : {:d}:{:d} - Clear'.format(mission_type, mission_id))
                self.http_wrapper('/map/clear/', body=self.make_request_body(
                    {
                        "missionType": mission_type,
                        "missionId": mission_id
                    }
                ))
                pass

    def http_wrapper(self, uri, header=None, body=None):
        if header is None:
            header = self.headers

        org = inspect.stack()[1][3]

        resp, content = self.http.request(
            uri=self.api_base + uri, method='POST', headers=header,
            body=body
        )

        if resp['status'] != '200':
            print('{:s} : Error {:s}'.format(org, resp['status']))
            raise Exception

        resp = json.loads(content.decode())

        if resp['status'] == 10000:
            print('{:s} : Currently undergoing maintenance.'.format(org))
            raise Exception

        if resp['status'] != 0:
            print('{:s} : {:s} / {:s}'.format(org, resp['errorTitle'], resp['errorMessage']))
            raise Exception

        self.parse_response_header(resp)

        return resp

    def produce_quest_do(self, event_id=398, produce_quest_id=3, min_point=60):
        if self.get_user_quest_point() < min_point:
            print('produce_quest_do : Quest point is low. {:d} < {:d}'.format(self.get_user_quest_point(), min_point))
            return False

        self.http_wrapper('/produce/quest/get/',
                          body=self.make_request_body({"eventId": event_id, "produceQuestId": produce_quest_id}))

        decrease_vital = 0

        while self.get_user_quest_point() > decrease_vital:
            print('produce_quest_do : Go! Go! Go!')
            resp = self.http_wrapper('/produce/quest/execute/', body=self.make_request_body(
                {"eventId": event_id, "produceQuestId": produce_quest_id}))

            # Update user information
            self.user_quest_point_max = resp['maxVital']
            self.set_user_quest_recovery_time(resp['maxVitalRecoveryTime'])
            self.user_level = resp['level']

            decrease_vital = resp['decreaseVital']

            if resp['resultType'] == 'NORNAL':
                pass
            elif resp['resultType'] == 'COMMUNICATION' or resp['resultType'] == 'HIGH_TENSION_COMMUNICATION':
                print("produce_quest_do : Let's communicate!")
                self.http_wrapper('/produce/quest/communication/', body=self.make_request_body(
                    {"eventId": event_id, "produceQuestId": produce_quest_id, "produceItemType": 1}))

    def use_item(self, item_id=3, use_count=3):
        resp = self.http_wrapper('/user/item/use/',
                                 body=self.make_request_body({"itemId": item_id, "useCount": use_count}))

        if resp['effectTargetType'] == 1:
            print('use_item : QP recovered.')
            self.set_user_quest_recovery_time(resp['maxRecoveryTime'])
        else:
            print("Unknown item")

    def gacha_darw(self, gacha_machine_id=13, draw_count=10):
        print('gacha_darw : {:d} x {:d}'.format(gacha_machine_id, draw_count))
        resp = self.http_wrapper('/gacha/draw/', body=self.make_request_body(
            {"gachaMachineId": gacha_machine_id, "drawCount": draw_count}))

    def get_ranking_produce(self, event_id=398):
        ranking = self.http_wrapper('/produce/ranking/get', body=self.make_request_body({"eventId": event_id}))

        with open('/Users/ek/Dropbox/IntelliJ IDEA/grirank/ranking.json', encoding='utf-8') as fp:
            org = json.load(fp)

        with open('/Users/ek/Dropbox/IntelliJ IDEA/grirank/ranking.json', mode='w', encoding='utf-8') as fp:
            for i in range(0, 20):
                org['data'][i]['data'].append(ranking['topRankingList'][i]['pointSum'])

            json.dump(org, fp)

    def get_player_profile(self, target_user_id, force=False):
        if target_user_id <= 0:
            print('get_player_profile : target_user_id is wrong! ({:d} <= 0)'.format(target_user_id))
            return None

        col = self.db.players

        resp = col.find_one({'userStatus.userId': target_user_id})

        if resp is not None and time.time() - resp['lastModified'] < 43200 and not force:
            return resp

        resp = self.http_wrapper('/mydata/get/', body=self.make_request_body({"targetUserId": target_user_id}))

        # Clean up.
        del resp['status']
        del resp['errorTitle']
        del resp['errorMessage']
        del resp['sessionLimitDatetime']
        del resp['masterResourceVersion']
        del resp['imageResourceVersion']
        del resp['soundResourceVersion']
        del resp['ccbiResourceVersion']
        del resp['schoolResourceVersion']
        del resp['versionStatus']
        del resp['masterDataVersion']
        del resp['responseDatetime']
        del resp['token']
        del resp['targetUserId']

        # Add time stamp.
        resp['lastModified'] = time.time()

        col.update({'userStatus.userId': target_user_id}, resp, upsert=True)

        return resp

    def update_player_profile(self):
        col = self.db.players
        resp = col.find()

        for row in resp:
            self.get_player_profile(row['userStatus']['userId'], force=True)
            print('update_player_profile : {:s} updated.'.format(row['name']))

    def invite_player(self, target_user_id):
        if target_user_id <= 0:
            print('invite_player : target_user_id is wrong! ({:d} <= 0)'.format(target_user_id))
            return None

        self.http_wrapper('/guild/invite/request/', body=self.make_request_body({"targetUserId": target_user_id}))
        print('invite_player : Invite {:d}.'.format(target_user_id))

    def get_ranking_pvp(self):
        ranking = self.http_wrapper('/pvp/event/ranking/get', body=self.make_request_body())

        with open('/Users/ek/Dropbox/IntelliJ IDEA/grirank/ranking_royal2.json', encoding='utf-8') as fp:
            org = json.load(fp)

        with open('/Users/ek/Dropbox/IntelliJ IDEA/grirank/ranking_royal2.json', mode='w', encoding='utf-8') as fp:
            for i in range(0, 20):
                org['data'][i]['data'].append(ranking['topRanking'][i]['pointSum'])
            json.dump(org, fp)

    def gift_open(self, count):
        offset = 0

        while True:
            gifts = self.http_wrapper('/gift/unopened/get/', body=self.make_request_body({"offset": offset}))
            unopened_count = gifts['unopenedCount']
            target = []

            print("gift_open : {:d} of {:d} gifts are processed.".format(offset, unopened_count))

            if unopened_count == 0:
                print("gift_open : Gifts not found.")
                break

            for gift in gifts['unopenedUserGiftList']:
                if gift['giftId'] != 20010:  # クエスト8話ドロップアイテム
                    target.append(gift['userGiftId'])

            if len(target) >= 1:
                self.http_wrapper('/gift/open/', body=self.make_request_body({"userGiftIdList": target}))
                print("gift_open : {:d} gift(s) opened. [{:d}]".format(len(target), unopened_count))

            offset += 10

            if offset >= count:
                break

    def get_circle_member(self, guild_id):
        offset = 0
        members = []

        while True:
            resp = self.http_wrapper('/guild/members/get/',
                                     body=self.make_request_body({"guildId": guild_id, "offset": offset}))

            for player in resp['guildMemberList']:
                t = self.get_player_profile(player['userId'])
                if t is not None:
                    members.append(t)

            offset += 10

            if offset > resp['memberCount']:
                break

        return members
