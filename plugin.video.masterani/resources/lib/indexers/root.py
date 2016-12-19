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

import sys

from resources.lib.modules import cache
from resources.lib.modules import control

# masterani_url = "http://www.masterani.me/"
from resources.lib.modules import favorites
from resources.lib.modules import masterani


def main_menu():
    lastvisited = control.setting("anime.lastvisited")
    if int(lastvisited) != 0:
        add_last_visited(lastvisited)

    add_favorites()

    items = [
        {'name': "Recent",
         'action': "recent"},

        {'name': "Anime",
         'action': "list"},

        {'name': "Search",
         'action': 'search'},

        {'name': "Clear Cache",
         'action': "clearCache"}
    ]
    add_directory(items)


def add_favorites():
    try:
        favorite = favorites.Favorites().list()
        if len(favorite) > 0:
            sysaddon = sys.argv[0]
            addon_poster = addon_banner = control.addonInfo('icon')
            addon_fanart = control.addonInfo('fanart')

            item = control.item("Favorites")
            url = '%s?action=%s' % (sysaddon, "favorites")

            item.setArt({'poster': addon_poster, 'banner': addon_banner})
            item.setProperty('Fanart_Image', addon_fanart)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
    except:
        pass

def add_last_visited(anime_id):
    try:
        c = cache.get(masterani.get_anime_details, 8, anime_id)

        sysaddon = sys.argv[0]
        addon_poster = addon_banner = control.addonInfo('icon')
        addon_fanart = control.addonInfo('fanart')

        item = control.item("Last Visited: [I]%s[/I]" % c['title'])
        poster = c['poster'][0]
        fanart = c['fanart'][0]
        item.setArt({'poster': poster})
        item.setProperty("Fanart_Image", fanart)
        url = '%s?action=get_episodes' % sysaddon
        try:
            url += '&anime_id=%s' % anime_id
        except:
            pass
        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
    except:
        pass


def add_directory(items):
    if items is None or len(items) == 0:
        return

    sysaddon = sys.argv[0]
    addon_poster = addon_banner = control.addonInfo('icon')
    addon_fanart = control.addonInfo('fanart')

    for i in items:
        item = control.item(i['name'])
        url = '%s?action=%s' % (sysaddon, i['action'])

        item.setArt({'poster': addon_poster, 'banner': addon_banner})
        item.setProperty('Fanart_Image', addon_fanart)
        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

    control.directory(int(sys.argv[1]), cacheToDisc=True)
    control.content(int(sys.argv[1]), 'files')
