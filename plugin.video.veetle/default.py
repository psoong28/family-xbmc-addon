'''
    veetle.com XBMC Plugin
    Copyright (C) 2011 t0mm0

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
	
	Category support added by rrattani
'''

import os
import simplejson as json
import time
import urllib, urllib2
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import base64

addon = xbmcaddon.Addon()
akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path') + "/akamaiSecureHD.py")
pluginUrl = sys.argv[0]
pluginHandle = int(sys.argv[1])
pluginQuery = sys.argv[2]
__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

BASE_URL = 'http://www.veetle.com'

CATEGORIES = [('All', '0'),
          ('Animation', '60'),
          ('Comedy', '50'),
          ('Education', '90'),
          ('Gaming', '40'),
          ('Mobile', '110'),
          ('Entertainment', '10'),
          ('Shows', '20'),
          ('Sports', '80'),
          ('Music', '70'),
          ('News', '30'),
          ('Religion', '100')]

def get_ajax_json(url):
    response = urllib2.urlopen(url)
    print 'getting: ' + url
    try:
        stream_json = json.loads(response.read())    
    except ValueError, error_info:
        stream_json = {'success': False, 'payload': str(error_info)}
    if stream_json['success']:
        print stream_json
        return stream_json['payload']
    else:
        print 'Problem getting info from: ' + url
        print 'Error returned: ' + stream_json['payload']
        return False

def get_stream_url(channel_id):
    return get_ajax_json(BASE_URL + '/index.php/channel/ajaxStreamLocation/' + 
                         channel_id + '/flash')

def get_cat_url(cat_id):
	return get_ajax_json(BASE_URL + '/index.php/listing/ajaxStreamByCategory/' +
						cat_id + '/0/-1/0')
	
def get_channel_info(channel_id):
    try:
        return json.loads(get_ajax_json(BASE_URL + 
                                        '/index.php/channel/ajaxInfo/' + 
                                        channel_id))
    except Exception, error_info:
        print 'Problem getting channel info: ' + channel_id
        print 'Error returned: ', error_info
        return {'title': 'unknown',
                'description': 'not available',
                'logo': {'sm': '', 'lg': ''},
                'programme': {'success': False}
                } 

class VeetleSchedule:
    def __init__(self, json_playlist, start_time, reference_clock):
        self.start_time = start_time
        self.playlist = self.populate_playlist(json_playlist, reference_clock)
                
    def get_now_playing(self):
        now = time.time()
        for item in self.playlist:
            if now >= item['start'] and now < item['end']:
                return time.strftime('(%H:%M) ',
                                     time.localtime(item['start'])
                                    ) + item['title']
        return '' 
        
    def get_schedule(self):
        now = time.time()
        schedule = ''
        for item in self.playlist:
            if now < item['end']: 
                schedule = schedule + time.strftime('(%H:%M) ',
                           time.localtime(item['start'])) + item['title'] + '\n'
        return schedule
        
    def populate_playlist(self, json_playlist, reference_clock):
        playlist = []
        now = time.time()
        t = self.start_time - (now - reference_clock)
        for item in sorted(json_playlist, key=lambda i: i['playOrder']):
            playlist.append({'title': item['title'],
                             'description': item['description'],
                             'duration': item['durationInSeconds'],
                             'start': t,
                             'end': t + item['durationInSeconds']})
            t = t + item['durationInSeconds']
        return playlist

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
        response = urllib2.urlopen(req, timeout=30)
        link = response.read()
        response.close()
        return link
    
try:
  getUrl("http://127.0.0.1:64653/version")
  proxyIsRunning = True
except:
  proxyIsRunning = False
if not proxyIsRunning:
  xbmc.executebuiltin('RunScript(' + akamaiProxyServer + ')')
  
if pluginQuery.startswith('?play='):
    #Play a stream with the given channel id
    channel_id = pluginQuery[6:].strip()
    print 'veetle.com Channel ID: ' + channel_id
    stream_url = get_stream_url(channel_id)
    VIDb64 = base64.encodestring(stream_url).replace('\n', '')
    fullUrl = 'http://127.0.0.1:64653/veetle/%s' % (VIDb64)
    if stream_url:        
        #xbmcplugin.setResolvedUrl(pluginHandle, True,
        #                          xbmcgui.ListItem(path=stream_url))
        xbmcplugin.setResolvedUrl(pluginHandle, True,
                                  xbmcgui.ListItem(path=fullUrl))
    else:
        xbmcplugin.setResolvedUrl(pluginHandle, False,
                                  xbmcgui.ListItem())
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__language__(30000), __language__(30001))   		
elif pluginQuery.startswith('?cat='):
    cat_id = pluginQuery[5:].strip()	
    channels = get_cat_url(cat_id)

    print 'Total veetle.com Channels: %d' % len(channels)

    #only list channels we can stream
    #channels = [channel for channel in channels if channel.get('flashEnabled',
    #                                                          False)]
                                                               
    print 'Flash Enabled veetle.com Channels: %d' % len(channels)

    do_grab = False #__settings__.getSetting('grab_schedule')
    for channel in channels:
        url = pluginUrl + '?play=' + channel['channelId']
        sm = channel['thumbnailUrlSmall']
        lg = channel['thumbnailUrl']
        if lg:
            thumb = lg
        else:
            thumb = sm

        if do_grab == 'true':
            channel_info = get_channel_info(channel['channelId'])            
            if channel_info['programme']['success']:
                schedule = VeetleSchedule(channel_info['programme']['payload'],
                                          channel_info['broadcastStartedTime'],
                                          channel_info['referenceClock'])
                channel['title'] += ' ' + schedule.get_now_playing()
                channel['description'] += '\n' + schedule.get_schedule()
        
        listitem = xbmcgui.ListItem(channel['title'], iconImage=thumb,
                                    thumbnailImage=thumb)
        infoLabels = {'title': channel['title']}
        listitem.setInfo('video', infoLabels)
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginHandle, url, listitem,
                                    isFolder=False, totalItems=len(channels))
    xbmcplugin.endOfDirectory(pluginHandle)
else:
    #Load the categories
    for category, categoryId in CATEGORIES:
        url = pluginUrl + '?cat=' + categoryId
        title = category
        listitem = xbmcgui.ListItem(title, iconImage="DefaultFolder.png",
                        thumbnailImage='')
        listitem.setInfo( type="Video", infoLabels={ "Title": title, "Plot": ""} )
        xbmcplugin.addDirectoryItem(pluginHandle, url, listitem,
                                    isFolder=True)
    xbmcplugin.endOfDirectory(pluginHandle)
		
