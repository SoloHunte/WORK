#!/usr/bin/python3
# -*- coding: utf8 -*-

import datetime
import hashlib
import time
import skill_scaner
import skill_scaner as skill

headers = {
    'Host': 'sport.betboom.ru',

    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://sport.betboom.ru/SportsBook/Overview/',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'countryCode': 'RU',
}


def score(gameInfo['SS'], sport_id):
    # SCORE
    try:
        # Футбол, Киберфутбол, Футзал, Гандбол
        if (sport_id in ['1', '7', '14', '15']):
            if (time_game != ''):
                time_game = str(int(time_game) // 60)
            else:
                time_game = '0'
            if ('ИТОГ' not in state):
                if ('(' in state):
                    dop_score = state.split('(')
                    dop_score = dop_score[1].split(')')
                    dop_score = dop_score[0].strip()
                    dop_score = dop_score.replace('-', ':')
                    sc1 = int(dop_score.split(':')[0])
                    sc2 = int(dop_score.split(':')[1])
                    score1 = int(score.split(':')[0])
                    score2 = int(score.split(':')[1])
                    dop_score = dop_score + ', ' + str(score1 - sc1) + ':' + str(score2 - sc2)
                else:
                    dop_score = score
            else:
                dop_score = state.replace(' ИТОГ', '')
                dop_score = dop_score.replace('-', ':')
                arrD = dop_score.split(' ')
                dop_score = dop_score.replace(' ', ', ')
                if (len(arrD) > 1):
                    if ('(' in state):
                        dop_score = state.split('(')
                        dop_score = dop_score[1].split(')')
                        dop_score = dop_score[0].strip()
                        dop_score = dop_score.replace('-', ':')
                        try:
                            sc1 = int(dop_score.split(':')[0])
                            sc2 = int(dop_score.split(':')[1])
                            score1 = int(score.split(':')[0])
                            score2 = int(score.split(':')[1])
                            dop_score = dop_score + ', ' + str(score1 - sc1) + ':' + str(score2 - sc2)
                        except:
                            dop_score = dop_score.replace(' ', ', ')
                    else:
                        dop_score = score
                else:
                    dop_score = dop_score.replace('(', ' ')
                    dop_score = dop_score.replace(')', ' ')
            score = score + ' (' + dop_score + ')'
        # Теннис
        if (sport_id == '2'):
            time_game = 'None'
            if (score == ''):
                score = '0:0'
            state = state.replace('-', ':')
            state = state.strip()
            state = state.replace(' ', ', ')
            state = state.replace('),', ')')
            score = score + ' ' + state
        # Настольный теннис, Волейбол, Бадминтон, Керлинг
        if (sport_id in ['3', '5', '11', '16']):
            time_game = 'None'
            if (score == ''):
                score = '0:0'
            if ('(' in state):
                state = state.split('(')
                state = state[1].split(')')
                state = state[0].strip()
                state = '(' + state.replace('-', ':') + ')'
                state = state.replace(' ', ', ')
                score = score + ' ' + state
                score = score.replace('*', '')
            else:
                score = score + ' (' + score + ')'
        # Баскетбол
        if (sport_id in ['4', '9', '12']):
            if (time_game != ''):
                time_game = str(int(time_game) // 60)
                if '0' in time_game:
                    time_game = 'Break'
            else:
                time_game = '0'
            if ('(' in state):
                state = state.split('(')
                state = state[1].split(')')
                state = state[0].strip()
                state = '(' + state.replace('-', ':') + ')'
                state = state.replace(' ', ', ')
                score = score + ' ' + state
            else:
                score = score + ' (' + score + ')'
        # Хоккей
        if (sport_id in ['6', '10']):
            if (time_game != ''):
                time_game = str(int(time_game) // 60)
                if '0' in time_game:
                    time_game = 'Break'
            else:
                time_game = '0'
            if ('(' in state):
                dop_score = state.split('(')
                dop_score = dop_score[1].split(')')
                dop_score = dop_score[0].strip()
                dop_score = dop_score.replace('-', ':')
                arrSt = dop_score.split(' ')
                score1 = int(score.split(':')[0])
                score2 = int(score.split(':')[1])
                for iR in arrSt:
                    sc1 = int(iR.split(':')[0])
                    sc2 = int(iR.split(':')[1])
                    score1 -= sc1
                    score2 -= sc2
                dop_score = dop_score + ' ' + str(score1) + ':' + str(score2)
                dop_score = dop_score.replace(' ', ', ')
                score = score + ' (' + dop_score + ')'
            else:
                score = score + ' (' + score + ')'
        # Киберспорт
        if (sport_id == '8'):
            time_game = 'None'
            if ('(' in state):
                state = state.split('(')
                state = state[1].split(')')
                state = state[0].strip()
                state = '(' + state.replace('-', ':') + ')'
                state = state.replace(' ', ', ')
                score = score + ' ' + state
                score = score.replace('*', '')
            else:
                score = score + ' (' + score + ')'

        if ('Break' in state) or ('Таймаут' in state):
            time_game = 'Break'
        if ('Match has not started' in state) or ('Матч не начался' in state):
            time_game = 'Not start'
        if ('END' in state) or ('FINISHED' in state) or ('ИТОГ' in state):
            time_game = 'Closed'
    except:
        print(sport_id)
        print(score)
        print(state)
        print(time_game)
        print(traceback.format_exc())
    # END_SCORE


def period(score, sport):
    try:
        s = ''
        if sport in ['1', '7', '14', '15']:
            g = score.split(':')
            s = str(len(g) - 2) + ' time'
        if (sport == '2'):
            g = score.split(' (')[0]
            g = g.split(':')
            g = int(g[0]) + int(g[1]) + 1
            s = str(g) + ' set '
            g = score.split(' (')[1]
            g = g.split(' ')
            g = g[len(g) - 1]
            g = g.replace(')', '')
            g = g.split(':')
            g = int(g[0].replace(',', '')) + int(g[1].replace(',', '')) + 1
            s += str(g) + ' game'
        if (sport == '3'):
            g = score.split(' (')[0]
            g = g.split(':')
            g = int(g[0]) + int(g[1]) + 1
            s = str(g) + ' set'
        if (sport in ['4', '9', '12']):
            g = score.split(':')
            s = str(len(g) - 2) + ' quarter'
        if (sport == '5'):
            g = score.split(' (')[0]
            g = g.split(':')
            g = int(g[0]) + int(g[1]) + 1
            s = str(g) + ' set'
        if (sport in ['6', '10', '17']):
            g = score.split(':')
            s = str(len(g) - 2) + ' period'
        if (sport == '8'):
            g = score.split(':')
            s = str(len(g) - 2) + ' map'
        if (sport == '11'):
            g = score.split(' (')[0]
            g = g.split(':')
            g = int(g[0]) + int(g[1]) + 1
            s = str(g) + ' set'
        if (sport == '16'):
            g = score.split(' (')[1]
            g = len(g.split(':')) - 1
            s = str(g) + ' end'
    except:
        s = ''
    return (s)


while skill.connect():
    time.sleep(60)
cur = skill.cur
conn = skill.conn
timeout = 30
bk_name = 'bet_boom'

voc_sports = {1: '1', 3: '2', 15: '3', 4: '4', 12: '5', 10: '6', 94: '7', 53: '8', 95: '9', 96: '10', 17: '14',
              13: '15'}
# session = requests.Session()
try:
    while True:
        skill.start_session()
        link = 'https://sport.betboom.ru/Live/Sports?langId=1&partnerId=147&countryCode=RU'

        data = skill.scaner_data_json(link, headers, timeout)
        kolGame = 0
        sportActive = {}
        info_liga = {}
        info_gamer = {}
        info_koef = {}
        name_kof_skill = {}
        koef_skill = {}

        for voc in data:
            kolGame += voc['EC']
            sportActive[voc['Id']] = voc['N']
        print(kolGame)
        gamerAll = {}
        for sportID in sportActive:
            link = f'https://sport.betboom.ru/Live/GetLiveEvents?sportId={sportID}&checkIsActiveAndBetStatus=false&stakeTypes=All&partnerId=147&languageId=1&countryCode=RU&langId=1'

            skill.start_session()
            data = skill.scaner_data_json(link, headers, timeout)
            if 'CNT' in data:
                for country in data['CNT']:
                    if 'CL' in country:
                        for ligaInfo in country['CL']:
                            sportIdThis = ligaInfo['SID']
                            sportNameThis = ligaInfo['SN']
                            ligaName = ligaInfo['N']
                            bk_id_liga = ligaInfo['CGId']
                            if 'E' in ligaInfo:
                                for gameInfo in ligaInfo['E']:
                                    gamerAll[gameInfo['Id']] = gameInfo['N']
                                    koefAll = 0
                                    koefInfo = gameInfo['StakeTypes']
                                    print(sportNameThis)
                                    print(gameInfo['N'])
                                    print(str(gameInfo['Id']))
                                    gamer1 = gameInfo['HT']
                                    gamer2 = gameInfo['AT']
                                    game_id = gameInfo['Id']
                                    periodName = period(gameInfo['ES'], voc_sports[sportIdThis])
                                    # started_at = gameInfo['D']
                                    id_game_hash = hashlib.md5(
                                        (str(gameInfo['Id']) + bk_name).encode('utf-8')).hexdigest()
                                    for koef in koefInfo:
                                        if 'Stakes' in koef:
                                            koefAll += len(koef['Stakes'])
                                    print(koefAll)
                                    print('-' * 50)
                                    try:
                                        sportid_my = voc_sports[sportIdThis]
                                    except Exception as _erspid:
                                        sportid_my = '0'
                                        continue
                            id_liga_hash = hashlib.md5((str(bk_id_liga) + bk_name).encode('utf-8')).hexdigest()
                            if sportid_my == '0':
                                continue
                            else:
                                cur = skill.connect
                                id_gamer1 = hashlib.md5(
                                    (str(gamer1) + str(sportid_my) + bk_name).encode('utf-8')).hexdigest()
                                id_gamer2 = hashlib.md5(
                                    (str(gamer2) + str(sportid_my) + bk_name).encode('utf-8')).hexdigest()
                                bk_id_gamer1 = '0'
                                bk_id_gamer2 = '0'
                                gamer_info_1 = hashlib.md5((str(bk_id_gamer1) + bk_name).encode('utf-8')).hexdigest()
                                gamer_info_2 = hashlib.md5((str(bk_id_gamer2) + bk_name).encode('utf-8')).hexdigest()
                                time_game = gameInfo['PT']
                                started_at = str(datetime.datetime.now())
                                sport_id = sportid_my
                                score = score(gameInfo['SS'], sportid_my)

                                active_sport_name = skill_scaner.active_sport_names(bk_name)
                                info_liga[id_liga_hash] = {'ligaName': ligaName, 'sport_Id': sportid_my,
                                                           'bk_id_liga': bk_id_liga}
                                info_gamer[id_game_hash] = {'bk_name': bk_name, 'id_liga_hash': id_liga_hash,
                                                            'bk_id_gamer1': bk_id_gamer1, 'bk_id_gamer2': bk_id_gamer2,
                                                            'gamer1': gamer1, 'gamer2': gamer2, 'time_game': time_game,
                                                            'score': score, 'started_at': started_at,
                                                            'sport_id': sport_id,
                                                            'name_sport': active_sport_name[int(sport_id)],
                                                            'link': link,
                                                            'game_id': game_id, 'gamer_info_1': gamer_info_1,
                                                            'gamer_info_2': gamer_info_2, 'period': periodName}
                                info_koef[id_game_hash] = {'game_id': game_id}
        print(len(gamerAll))
        print(len(info_liga))
        bk_id = '19'
        skill.add_liga(info_liga, bk_id)
        skill.add_gamer(info_gamer, bk_id, bk_name)
        skill.add_koef(koef_skill, bk_id)
        print('=' * 100)
        time.sleep(4)
except KeyboardInterrupt:
    print('Принудиловка')
    skill.close_session()
    skill.cur.close()
    skill.conn.close()
