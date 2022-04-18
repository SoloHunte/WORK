"""# -*- coding: utf8 -*-"""
import os
# import re
import sys
# import json
import brotli
# import hashlib
import requests
import traceback
import configobj
import mysql.connector
from datetime import datetime


def get_config():
    appPath = os.path.abspath(os.path.dirname(os.path.join(sys.argv[0])))
    inifile = os.path.dirname(appPath) + "/ini/config.ini"
    return configobj.ConfigObj(inifile)


def connect():
    global conn
    global cur
    er = True
    try:
        config = get_config()
        conn = mysql.connector.connect(host=config['host'], database=config['database'], user=config['user'],
                                       password=config['password'])
        if conn.is_connected():
            cur = conn.cursor()
            er = False
    except Exception as ere:
        print(ere)
    return er


def user_agent_rand():
    sql = "SELECT name FROM user_agent ORDER BY RAND() LIMIT 1"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    return row[0][0]


def get_actual_url(bk_name):
    sql = f"SELECT link FROM bukmeker WHERE name='{bk_name}'"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    row_str = row[0][0]
    link = row_str.replace('https://www.', '')
    return link


def proxy():
    sql = "SELECT id, ip, port, user, pass, type FROM proxy WHERE active = 1"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    return row


def uid_str(stroka):
    uid_str = 0
    for i in range(len(stroka)):
        uid_str += ord(stroka[i])
    return uid_str


def start_session():
    global session
    session = requests.Session()


def close_session():
    session.close()


def scaner_data_json(link, headers, timeout, proxies=None):
    if proxies is None:
        proxies = {}
    try:
        er = True
        d = {}
        if len(proxies) > 1:
            response = session.get(link, headers=headers, timeout=timeout, proxies=proxies)
        else:
            response = session.get(link, headers=headers, timeout=timeout)
        if response.status_code == requests.codes.ok:
            if 'json' in response.headers['content-type']:
                try:
                    if 'br' in response.headers['content-encoding']:
                        encoded = brotli.decompress(response.content)
                except:
                    pass
                d = response.json()
                if len(d) > 0:
                    er = False
    except:
        pass
    data = {'error': er, 'data': d}
    return data


def scaner_data_html(link, headers, timeout, proxies=None):
    if proxies is None:
        proxies = {}
    try:
        er = True
        d = ''
        if len(proxies) > 1:
            response = session.get(link, headers=headers, timeout=timeout, proxies=proxies)
        else:
            response = session.get(link, headers=headers, timeout=timeout)
        if response.status_code == requests.codes.ok:
            if 'html' in response.headers['content-type']:
                d = response.text
                if len(d) > 0:
                    er = False
        else:
            if response.status_code > 500:
                try:
                    ip = proxies['http'].split('@')[1]
                    ip = ip.split(':')[0]
                    sql = "UPDATE proxy SET " + bk + " = -1 WHERE ip='" + ip + "'"
                    query = sql
                    cur.execute(query)
                    conn.commit()
                except:
                    pass
    except:
        print(traceback.format_exc())
    data = {'error': er, 'data': d}
    return data


def get_bk_id(bk_name):
    sql = "SELECT id FROM bukmeker WHERE name='" + bk_name + "' and active = 1"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    return str(row[0][0])


def get_domain(bk_name):
    sql = f"SELECT link FROM bukmeker WHERE name='{bk_name}'"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    return str(row[0][0])


def active_sport(bk_name):
    sql = "SELECT id, " + bk_name + " FROM `sport` WHERE active = 1 AND " + bk_name + "!='0'"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    s = {}
    for n in row:
        s[n[1]] = n[0]
    return s


def active_sport_names(bk_name):
    sql = "SELECT id, name_rus FROM `sport` WHERE active = 1"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    s = {}
    for n in row:
        s[n[0]] = n[1]
    return s


def add_liga(info_match, bk_id):
    sql = "SELECT skill_id FROM liga_info WHERE bk_id=" + bk_id + " and live_is = 1"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    d_sql = ''
    for i in row:
        d_sql += "'" + i[0] + "',"

    w_sql = ''
    for ins in info_match:
        w_sql += "('" + ins + "', '" + info_match[ins]['liga'].replace("'", "\\'") + "', " + info_match[ins][
            'sport_id'] + ", " + bk_id + ", " + str(info_match[ins]['bk_id_liga']) + ", 1),"
        d_sql = d_sql.replace("'" + ins + "',", "")
    w_sql = w_sql[0:-1]
    sql = "INSERT INTO liga_info (skill_id, name, sport_id, bk_id, bk_liga_id, live_is) VALUES " + w_sql + \
          " ON DUPLICATE KEY UPDATE name = VALUES(name), sport_id = VALUES(sport_id), bk_id" \
          " = VALUES(bk_id), bk_liga_id = VALUES(bk_liga_id), live_is = VALUES(live_is)"
    query = sql
    cur.execute(query)
    conn.commit()
    if len(d_sql) > 1:
        d_sql = d_sql[0:-1]
        sql = "UPDATE liga_info SET live_is = 0 WHERE skill_id IN (" + d_sql + ") and bk_id = " + bk_id
        query = sql
        cur.execute(query)
        conn.commit()


def add_gamer(info_gamer, bk_id, bk_name):
    sql = "SELECT skill_id FROM gamer_live WHERE bk_id=" + bk_id
    query = (sql)
    cur.execute(query)
    row = cur.fetchall()
    d_sql = ''
    for i in row:
        d_sql += "'" + i[0] + "',"

    i_sql = ''
    l_sql = ''
    for ins in info_gamer:
        try:
            liga_info = info_gamer[ins]['id_liga_hash']
            bk_id_gamer1 = str(info_gamer[ins]['bk_id_gamer1'])
            bk_id_gamer2 = str(info_gamer[ins]['bk_id_gamer2'])
            gamer1 = info_gamer[ins]['gamer1'].replace("'", "\\'")
            gamer2 = info_gamer[ins]['gamer2'].replace("'", "\\'")
            name = gamer1 + ' - ' + gamer2
            time_game = info_gamer[ins]['time_game']
            score = info_gamer[ins]['score']
            period = info_gamer[ins]['period']
            started_at = str(datetime.utcfromtimestamp(info_gamer[ins]['started_at']).strftime('%Y-%m-%d %H:%M:%S'))
            sport = info_gamer[ins]['sport_id']
            link = (info_gamer[ins]['link']).replace("'", "\\'")
            gamer_id_bk = str(info_gamer[ins]['game_id'])
            gamer_info_1 = info_gamer[ins]['gamer_info_1']
            gamer_info_2 = info_gamer[ins]['gamer_info_2']
            i_sql += "('" + gamer_info_1 + "', '" + gamer1 + "'," + bk_id + ", '" + liga_info + "'," + bk_id_gamer1 + "),"
            i_sql += "('" + gamer_info_2 + "', '" + gamer2 + "'," + bk_id + ", '" + liga_info + "'," + bk_id_gamer2 + "),"
            l_sql += "('" + ins + "', '" + gamer_id_bk + "', '" + liga_info + "', " + bk_id + ", '" + name + "', '" + gamer_info_1 + "', '" + gamer_info_2 + "', '" + time_game + "', '" + score + "', '" + period + "', '" + link + "', '" + started_at + "'),"
            d_sql = d_sql.replace("'" + ins + "',", "")
        except:
            continue

    i_sql = i_sql[0:-1]
    sql = "INSERT INTO gamer_info (skill_id, name, bk_id, liga_info, bk_id_gamer) VALUES " + i_sql + "ON DUPLICATE " \
                                                                                                     "KEY UPDATE name " \
                                                                                                     "= VALUES(name), " \
                                                                                                     "bk_id = VALUES(" \
                                                                                                     "bk_id), " \
                                                                                                     "liga_info = " \
                                                                                                     "VALUES(" \
                                                                                                     "liga_info), " \
                                                                                                     "bk_id_gamer = " \
                                                                                                     "VALUES(" \
                                                                                                     "bk_id_gamer) "
    query = sql
    cur.execute(query)
    conn.commit()

    l_sql = l_sql[0:-1]
    sql = "INSERT INTO gamer_live (skill_id, gamer_id_bk, liga_info, bk_id, name, gamer_info_1, gamer_info_2, " \
          "time_game, score, period, link, started_at) VALUES " + l_sql + " ON DUPLICATE KEY UPDATE liga_info = " \
                                                                          "VALUES(liga_info), bk_id = VALUES(bk_id), " \
                                                                          "name = VALUES(name), gamer_info_1 = " \
                                                                          "VALUES(gamer_info_1), gamer_info_2 = " \
                                                                          "VALUES(gamer_info_2), time_game = VALUES(" \
                                                                          "time_game), score = VALUES(score), " \
                                                                          "period = VALUES(period), comment = VALUES(" \
                                                                          "comment), link = VALUES(link), started_at " \
                                                                          "= VALUES(started_at), update_at = NOW() "
    query = sql
    cur.execute(query)
    conn.commit()

    if len(d_sql) > 1:
        d_sql = d_sql[0:-1]
        sql = "DELETE FROM gamer_live WHERE skill_id IN (" + d_sql + ") and bk_id = " + bk_id
        query = sql
        cur.execute(query)
        conn.commit()
        sql = "DELETE FROM koef WHERE game_live IN (" + d_sql + ") and bk_id = " + bk_id
        query = sql
        cur.execute(query)
        conn.commit()


def clear_koef(bk_name):
    sql = "DELETE FROM koef WHERE bk_id IN (SELECT id FROM bukmeker WHERE name='" + bk_name + "' and active = 1)"
    query = sql
    cur.execute(query)
    conn.commit()
    sql = "DELETE FROM gamer_live WHERE bk_id IN (SELECT id FROM bukmeker WHERE name='" + bk_name + "' and active = 1)"
    query = sql
    cur.execute(query)
    conn.commit()
    sql = "UPDATE liga_info SET live_is = '0' WHERE bk_id IN (SELECT id FROM bukmeker WHERE name='" \
          + bk_name + "' and active = 1)"
    query = sql
    cur.execute(query)
    conn.commit()


def add_koef(koef_skill, bk_id):
    sql = "SELECT short_name FROM name_koef WHERE bk_id=" + bk_id + " and name <> ''"
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    koef_det = []
    for n in row:
        koef_det.append(n[0])

    sql = "SELECT skill_id FROM koef WHERE bk_id=" + bk_id
    query = sql
    cur.execute(query)
    row = cur.fetchall()
    d_sql = ''
    for i in row:
        d_sql += "'" + i[0] + "',"

    n_sql = ''
    k_sql = ''
    for ins in koef_skill:
        try:
            if koef_skill[ins]['short_name'] not in koef_det:
                comment = koef_skill[ins]['name'].replace("'", "\\'")
                name_hash = koef_skill[ins]['name_hash']
                short_name = koef_skill[ins]['short_name']
                n_sql += f"('{name_hash}', '{bk_id}', '{short_name}', '{comment}'),"
            else:
                dop = str(koef_skill[ins]['dop']).replace("'", '"')
                game_live = koef_skill[ins]['game_live']
                game_orig = koef_skill[ins]['game_orig']
                name = koef_skill[ins]['name']
                short_name = koef_skill[ins]['short_name']
                param = koef_skill[ins]['param']
                if param not in ['NULL', 'null']:
                    param = "'" + param + "'"
                name_hash = koef_skill[ins]['name_hash']
                k_sql += f"('{ins}', '{game_live}', {bk_id}, '{game_orig}', '{name}', '{short_name}'," \
                         f" {koef_skill[ins]['koef']}, {param}, '{dop}', '{name_hash}'),"
            d_sql = d_sql.replace("'" + ins + "',", "")
        except:
            continue
    n_sql = n_sql[0:-1]
    if n_sql != '':
        sql = "INSERT INTO name_koef (skill_id, bk_id, short_name, comment) VALUES " + \
              n_sql + " ON DUPLICATE KEY UPDATE short_name = VALUES(short_name), comment = VALUES(comment)"
        query = sql
        cur.execute(query)
        conn.commit()
    k_sql = k_sql[0:-1]
    if k_sql != '':
        sql = "INSERT INTO koef (skill_id, game_live, bk_id, game_orig, name, short_name, koef, param, dop, " \
              "name_koef_id) VALUES " + k_sql + " ON DUPLICATE KEY UPDATE game_live = VALUES(game_live), game_live = " \
                                                "VALUES(game_live), bk_id = VALUES(bk_id), game_orig = VALUES(" \
                                                "game_orig), name = VALUES(name), short_name = VALUES(short_name), " \
                                                "koef = VALUES(koef), param = VALUES(param), dop = VALUES(dop), " \
                                                "name_koef_id = VALUES(name_koef_id), update_at = NOW() "
        query = sql
        cur.execute(query)
        conn.commit()

    if len(d_sql) > 1:
        d_sql = d_sql[0:-1]
        sql = "DELETE FROM koef WHERE skill_id IN (" + d_sql + ") and bk_id = " + bk_id
        query = sql
        cur.execute(query)
        conn.commit()
        sql = "DELETE FROM vil WHERE koef_id_1 IN (" + d_sql + ") or koef_id_2 IN (" + d_sql + ")"
        query = sql
        cur.execute(query)
        conn.commit()
