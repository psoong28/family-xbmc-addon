# -*- coding: utf-8 -*-

import re,urlparse,json
from liveresolver.modules import client
from liveresolver.modules.log_utils import log



def resolve(url):
    try:
        url = (urlparse.urlparse(url).path).split('/')[1]

        result = client.request('http://lancer.streamup.com/api/channels/%ss-stream/playlists'%url.lower())
        js = json.loads(result)
        hls = js['hls']
        mpd = js['mpd']
        hls+='|%s' % urllib.urlencode('User-agent':client.agent())
        return hls

       
    except:
       return


