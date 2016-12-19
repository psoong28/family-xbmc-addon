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

import base64
import json
import re
import sys
import urllib

import xbmc
import xbmcgui
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import masterani
from resources.lib.modules.control import progressDialog
from resources.lib.modules.watched import Watched


def play(anime_id, episode_id):
    # try:
        # content = cache.get(masterani.get_anime_details(anime_id), 2)

        l1 = "Fetching video"
        progressDialog.create(heading="MasterAni", line1="Fetching video")
        progressDialog.update(0, line1=l1, line3="Loading hosts")
        hosts = client.request("http://www.masterani.me/api/hosts")
        hosts = json.loads(hosts)

        progressDialog.update(25, line1=l1, line3="Loading episodes urls")

        videos = client.request("http://www.masterani.me/api/episode/%s?videos=1" % episode_id)
        videos = json.loads(videos)['videos']
        progressDialog.update(50, line1=l1, line3="Picking nose")

        hostlist = []

        videos = sorted(videos, key=lambda k: (int(k['quality']), int(k['type'])), reverse=True)

        autoplay = control.setting("autoplay.enabled")
        maxq = control.setting("autoplay.maxquality")
        subdub = control.setting("autoplay.subdub")

        for video in videos:
            hostname = [x['name'] for x in hosts if int(x['id']) == int(video['host_id'])][0]
            subs = 'Sub' if video['type'] is 1 else 'Dub'
            quality = video['quality']
            if 'true' in autoplay:
                if subdub in subs and int(quality) <= int(maxq):
                    hostlist.append("%s | %s | %s" % (quality, subs, hostname))
            else:
                hostlist.append("%s | %s | %s" % (quality, subs, hostname))

        if autoplay in 'false':
            hostdialog = control.dialog.select("Select host", hostlist)
        else:
            if len(hostlist) is 0:
                progressDialog.close()
                xbmcgui.Dialog().ok("Masterani", "No hosts found for autoplay.", "Change addon settings and try again.")
                hostdialog = -1
            else:
                hostdialog = 0

        if hostdialog == -1:
            progressDialog.close()
            control.execute('Dialog.Close(okdialog)')
            return

        host_id = videos[hostdialog]['host_id']
        embed_id = videos[hostdialog]['embed_id']
        if host_id is '':
            return

        prefix = ""
        suffix = ""

        for host in hosts:
            if str(host_id) in str(host['id']):
                prefix = host['embed_prefix']
                suffix = host['embed_suffix']
                break

        try:
            if suffix is not None:
                url = prefix + embed_id + suffix
            else:
                url = prefix + embed_id
        except:
            pass

        progressDialog.update(75, line1=l1, line3="Loading video")
        if 'moe' in host['name']:
            content = base64.b64decode(re.compile("atob\('(.+?)'\)").findall(client.request(url))[0])
            mp4 = re.compile("source src=\"(.+?)\"").findall(content)[0]
        if 'MP4Upload' in host['name']:
            mp4 = re.compile("\"file\": \"(.+?)\"").findall(client.request(url))[0]
        if 'Bakavideo' in host['name']:
            content = re.compile("go\((.+?)\)").findall(client.request(url))[0]
            content = content.replace("'", "").replace(", ", "/")
            content = "https://bakavideo.tv/" + content
            content = client.request(content)
            content = json.loads(content)
            content = content['content']
            content = base64.b64decode(content)
            mp4 = client.parseDOM(content, 'source', ret='src')[0]
        if 'BETA' in host['name']:
            mp4 = embed_id
        if 'Vidstream' in host['name']:
            mp4 = re.compile("source src='(.+?)'").findall(client.request(url))[0]
        if 'Aniupload' in host['name']:
            mp4 = re.compile("\(\[\{src: \"(.+?)\"").findall(client.request(url))[0]
        if 'Drive.g' in host['name']:
            mp4 = re.compile("url_encoded_fmt_stream_map\",\"(.+?)\"\]").findall(client.request(url))[0]
            mp4 = mp4.split(",")[0]
            mp4 = mp4[mp4.find("https"):]
            mp4 = urllib.unquote(mp4)

        progressDialog.close()
        control.sleep(100)
        MAPlayer().run(anime_id, episode_id, mp4)
    # except:
    #     pass


class MAPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.anime_id = 0
        self.episode_id = 0

    def run(self, anime_id, episode_id, url):
        self.anime_id = int(anime_id)
        self.episode_id = int(episode_id)

        item = control.item(path=url)

        try:
            c = cache.get(masterani.get_anime_details, 3, self.anime_id)

            ctype = c['type']
            ctype = 'video' if int(ctype) is 2 else 'episode'

            tvshowtitle = c['title']
            poster = c['poster'][0]

            item.setArt({'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})

            e = c['episodes'][self.episode_id]
            title = e['info']['title']
            season = 1
            if season is None: season = 1
            episode = e['info']['episode']
            if ctype is 'video': title = c['title']
            if title is None: title = "Episode %s" % episode

            item.setInfo(type="video",
                         infoLabels={'tvshowtitle': tvshowtitle, 'title': title, 'episode': int(episode),
                                     'season': int(season), 'mediatype': ctype})
        except:
            pass

        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')

        xbmc.Player().play(url, item)
        self.playback_checker()

        pass

    def playback_checker(self):
        for i in range(0, 300):
            if self.isPlaying():
                break
            xbmc.sleep(100)

        while self.isPlaying():
            try:
                if (self.getTime() / self.getTotalTime()) >= .8:
                    Watched().mark(self.anime_id, self.episode_id)
            except:
                pass
            xbmc.sleep(1000)

    def onPlayBackStarted(self):
        control.setSetting("anime.lastvisited", str(self.anime_id))
        pass

    def onPlayBackEnded(self):
        self.onPlayBackStopped()
        pass

    def onPlayBackStopped(self):
        control.refresh()
        pass
