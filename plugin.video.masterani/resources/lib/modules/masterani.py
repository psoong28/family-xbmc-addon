# -*- coding: utf-8 -*-

'''
    MasterAni Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json
import os
import sqlite3

from resources.lib.modules import client
from resources.lib.modules import control


def get_anime_details(anime_id):
    # print "Getting anime details: %s" % url
    try:
        result = client.request("http://www.masterani.me/api/anime/%s/detailed" % anime_id, timeout=60)
        result = json.loads(result)

        info = result['info']


        anime_id = info['id']
        title = info['title']
        type = info['type']
        plot = info['synopsis'] if 'synopsis' in info else ''
        premiered = info['started_airing_date'] if 'started_airing_date' in info else ''
        rating = info['score'] if 'score' in info else 0
        episode_count = info['episode_count'] if 'episode_count' in info else 0
        age_rating = info['age_rating'] if 'age_rating' in info else ''
        tvdb = info['tvdb_id'] if 'tvdb_id' in info else 0
        genre = [g['name'] for g in result['genres']]
        genre = ' / '.join(genre)

        status = info['status'] if 'status' in info else 0
        duration = info['episode_length'] if 'episode_length' in info else 24
        if duration is None or duration is 0: duration = 24

        episodes = result['episodes']
        fanart = [f['file'] for f in result['wallpapers']]
        poster = result['poster'] if 'poster' in result else None
        episodes2 = dict()

        for episode in episodes:
            episodes2[episode['info']['id']] = episode

        return (
            {'title': title, 'anime_id': anime_id, 'plot': plot, 'poster': poster, 'premiered': premiered,
             'rating': rating, 'type': type, 'episode_count': episode_count, 'age_rating': age_rating, 'tvdb': tvdb,
             'genre': genre, 'status': status, 'duration': duration, 'episodes': episodes2, 'fanart': fanart})

    except:
        pass


def get_by_genre_id(genre_id, anime_offset=0, limit=100, lsort=True, asc=True):
    path = os.path.join(control.addonPath + "/resources/resources.db")
    dbconn = sqlite3.connect(path)
    sortby = "title" if 'True' in lsort else "score"
    asc = "ASC" if 'True' in asc else "DESC"
    print "%s, %s, %s" % (sortby, lsort, asc)
    dbcur = dbconn.execute(
        "SELECT anime_id,status FROM anime WHERE anime_id IN(SELECT anime_id FROM genremapping WHERE genre_id = '%s') ORDER BY %s %s LIMIT '%d'" % (
            genre_id, sortby, asc, limit))
    match = dbcur.fetchall()
    # match = [tuple(g)[0] for g in match]
    dbconn.close()
    return match


def get_by_select(genre=[], limit=5000, sort=0, status=0, stype=[]):
    try:
        sort = eval(sort)
    except:
        pass
    try:
        status = eval(status)
    except:
        pass
    try:
        genre = eval(genre)
    except:
        pass
    try:
        stype = eval(stype)
    except:
        pass

    mainsql = "SELECT anime_id, status FROM anime WHERE "

    genresql = ''
    if len(genre) > 0:
        genresql = " anime_id IN(SELECT anime_id FROM genremapping WHERE %s)" % ' OR '.join(
            ["genre_id = %s" % str(x) for x in genre])

    statussql = "status != 2 "
    if status is not None:
        statussql = "status = '%s' " % status

    typesql = ""
    if len(stype) > 0:
        typesql += "type IN(%s)" % ",".join(str(x) for x in stype)

    sortsql = ""
    if sort is 0:
        sortsql = " ORDER BY score ASC"
    if sort is 1:
        sortsql = " ORDER BY score DESC"
    if sort is 2:
        sortsql = " ORDER BY title ASC"
    if sort is 3:
        sortsql = " ORDER BY title DESC"

    if len(genresql) > 0:
        genresql += " AND "

    if len(typesql) > 0:
        typesql = " AND " + typesql

    sql = mainsql + genresql + statussql + typesql + sortsql
    print sql
    path = os.path.join(control.addonPath + "/resources/resources.db")
    dbconn = sqlite3.connect(path)
    dbcur = dbconn.execute(sql + " LIMIT '%d'" % limit)
    match = dbcur.fetchall()
    # match = [tuple(g)[0] for g in match]
    dbconn.close()
    print "Matches found: %s" % len(match)
    return match


def get_by_search(search):
    path = os.path.join(control.addonPath + "/resources/resources.db")
    dbconn = sqlite3.connect(path)
    dbcur = dbconn.execute("SELECT anime_id,status FROM anime WHERE title LIKE '%" + str(search) + "%'")
    match = dbcur.fetchall()
    # match = [tuple(g)[0] for g in match]
    dbconn.close()
    return match


get_anime_details(1)