#!/usr/bin/python3
# -*- coding: utf8 -*-

import datetime
import hashlib
import random
import time
import skill_scaner
import skill_scaner as skill

names_koefs = []

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


def funk_for_short_name(sport, kof_nam, kof_param, gamer1, gamer2):
    div_kof_name = kof_nam.split(':')
    if len(div_kof_name[0].split(' ')) > 1:
        if div_kof_name[0].split(' ')[1] in ['сет', "гейм", "четверть", "половина", "тайм", "период"]:
            new_name_kof = ''
            for i in range(1, len(div_kof_name)):
                new_name_kof = new_name_kof + f'{div_kof_name[i]}:'
            peri = div_kof_name[0]
        else:
            new_name_kof = kof_nam
            peri = 'Match'
    else:
        new_name_kof = kof_nam
        peri = 'Match'
    if '(' in new_name_kof:
        kof_nam_div = kof_nam.split('(')
        if len(kof_nam_div) <= 2:
            ferst_koef_nam = kof_nam.split('(')[0] + '('
            second_koef_nam = ')' + kof_nam.split(')')[1]
            kof_nam_new = ferst_koef_nam + second_koef_nam
        else:
            next_kof_nam = kof_nam.split(':')
            if len(next_kof_nam) == 2:
                try:
                    ferst_koef_nam = next_kof_nam[0].split('(')[0] + '('
                    second_koef_nam = ')' + next_kof_nam[0].split(')')[1] + ':'
                    tree_koef_nam = next_kof_nam[1].split('(')[0] + '('
                    four_koef_nam = ')' + next_kof_nam[1].split(')')[1]
                    kof_nam_new = ferst_koef_nam + second_koef_nam + tree_koef_nam + four_koef_nam
                except Exception as er:
                    print(next_kof_nam)
                    print(er)
            else:
                try:
                    ferst_koef_nam = next_kof_nam[1].split('(')[0] + '('
                    second_koef_nam = ')' + next_kof_nam[1].split(')')[1] + ':'
                    tree_koef_nam = next_kof_nam[2].split('(')[0] + '('
                    four_koef_nam = ')' + next_kof_nam[2].split(')')[1]
                    kof_nam_new = ferst_koef_nam + second_koef_nam + tree_koef_nam + four_koef_nam
                except Exception as er:
                    print(next_kof_nam)
                    print(er)
    else:
        kof_nam_new = new_name_kof
    if 'Ком.1' in kof_nam_new:
        kof_nam_new = kof_nam_new.replace('Ком.1', 'Команда1')
    elif 'Ком.2' in kof_nam_new:
        kof_nam_new = kof_nam_new.replace('Ком.2', 'Команда2')

    # print(f'{kof_nam}\n {kof_nam_new}')
    # print('+' * 100)
    # with open('rez_koef.csv', 'a', encoding='utf-8') as fw:
    #     fw.write(kof_nam + '\n')
    #     fw.write(kof_nam_new + '\n')
    #     fw.write('+' * 100 + '' + '\n')
    kof_nam_new = kof_nam_new.replace(peri, '')
    kof_nam = kof_nam.replace(peri, '')
    short_name = f'{sport}.{peri}.{kof_nam_new}'
    comment = f'{sport}.{peri}.{kof_nam}.'
    return short_name, comment


def right_score(ss, hos, aws, num):
    if int(num) > 1:
        ss = ", ".join(ss.split(',')[:int(num)])
    else:
        ss = ", ".join(ss.split(',')[:1])

    return f'{hos}:{aws} ({ss})'


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
timeout = 50
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
        name_koef = {}
        koef_skill = {}

        for voc in data:
            kolGame += int(voc['EC'])
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
                                    # print(sportNameThis)
                                    # print(gameInfo['N'])
                                    # print(str(gameInfo['Id']))
                                    gamer1 = gameInfo['HT']
                                    gamer2 = gameInfo['AT']
                                    game_id = gameInfo['Id']
                                    id_game_hash = hashlib.md5(
                                        (str(gameInfo['Id']) + bk_name).encode('utf-8')).hexdigest()

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
                                # Изменим формирование, добавим id_gamer
                                gamer_info_1 = hashlib.md5(
                                    (str(bk_id_gamer1) + bk_name + id_gamer1).encode('utf-8')).hexdigest()
                                gamer_info_2 = hashlib.md5(
                                    (str(bk_id_gamer2) + bk_name + id_gamer2).encode('utf-8')).hexdigest()
                                time_game = gameInfo['PT']
                                started_at = str(datetime.datetime.now())
                                sport_id = sportid_my
                                num_period = str(gameInfo['CP'])
                                scoreSS = str(gameInfo['SS']).replace('-', ',').replace(' ', '')
                                scoreHS = str(gameInfo['HS'])
                                scoreAS = str(gameInfo['AS'])
                                score = right_score(scoreSS, scoreHS, scoreAS, num_period)
                                try:
                                    periodName = period(score, voc_sports[sportIdThis])
                                except Exception:
                                    pass
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
                                for typ_kof in koefInfo:
                                    for koef_stakes in typ_kof['Stakes']:
                                        kof_hash = hashlib.md5(
                                            (active_sport_name[int(sport_id)] + str(koef_stakes['Id']) + koef_stakes[
                                                'N'] + str(koef_stakes['A']) + bk_name).encode('utf-8')).hexdigest()
                                        name_hash = hashlib.md5(
                                            (active_sport_name[int(sport_id)] + koef_stakes['N'] + bk_name).encode(
                                                'utf-8')).hexdigest()

                                        sport = active_sport_name[int(sport_id)]
                                        per = gameInfo["ES"]
                                        kof_nam = koef_stakes["SFN"]
                                        kof_param = str(koef_stakes["A"])
                                        scor = gameInfo["SS"]

                                        comment = funk_for_short_name(sport, kof_nam,
                                                                      kof_param, gamer1, gamer2)[1]
                                        koef_Tot = funk_for_short_name(sport, kof_nam,
                                                                       kof_param, gamer1, gamer2)[0]

                                        dop = {"sport": info_gamer[id_game_hash]["name_sport"],
                                               "game_id": str(info_gamer[id_game_hash]["game_id"]),
                                               "comment": comment,
                                               "url_game": link,
                                               "koef": str(koef_stakes["SFN"].replace("'", "\\'"))

                                               }

                                        dop = str(dop).replace("'", '"')
                                        koef_stakes_a = str(koef_stakes['F'])
                                        param = str(koef_stakes['A'])
                                        game_orig = str(info_koef[id_game_hash]['game_id'])
                                        
                                        name_hash = hashlib.md5(
                                            (active_sport_name[int(sport_id)] + koef_Tot + bk_name).encode(
                                                'utf-8')).hexdigest()
                                        
                                        koef_skill[kof_hash] = {'game_live': id_game_hash,
                                                                'game_orig': game_orig,
                                                                'name_hash': name_hash, 'name': comment,
                                                                'short_name': koef_Tot, 'koef': koef_stakes_a,
                                                                'param': param, 'dop': dop}

        bk_id = '19'
        skill.add_liga(info_liga, bk_id)
        skill.add_gamer(info_gamer, bk_id, bk_name)
        skill.add_koef(koef_skill, bk_id)
        print('=' * 100)
        # for ko in names_koefs:
        #     line = f'{ko["sport"]};{ko["per"]};{ko["kof_nam"]};{ko["kof_param"]};{ko["gamer1"]};{ko["gamer2"]}\n'
        #     with open('kof.csv', 'a', encoding='utf-8') as wr:
        #         wr.write(line)
        # names_koefs = []
        # data_short = {
        #     'sport': '',
        #     'per': '',
        #     'kof_nam': '',
        #     'kof_param': '',
        #     'gamer1': '',
        #     'gamer2': ''
        # }
        time.sleep(3)
except KeyboardInterrupt:
    print('Принудиловка')
    skill.close_session()
    skill.cur.close()
    skill.conn.close()
