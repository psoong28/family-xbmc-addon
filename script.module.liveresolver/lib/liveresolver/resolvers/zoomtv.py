# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,decryptionUtils
from liveresolver.modules.log_utils import log


def resolve(url):
    try:

        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        headers = { 'referer': referer,
                                 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                 'Content-Type' :'application/x-www-form-urlencoded',
                                 'Connection' : 'keep-alive',
                                 'Host' : 'www.zoomtv.me',
                                 'Origin' : urlparse.urlparse(referer).netloc,
                                 'User-Agent' : client.agent()
                                 }
        fid = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
        pid = urlparse.parse_qs(urlparse.urlparse(url).query)['pid'][0]
        url = 'http://www.zoomtv.me/embed.php?v=%s&vw=660&vh=450'%fid
        page = url
        post_data = 'uagent=uagent&pid='+pid
        result = client.request(url, post=post_data,headers = headers)
        result = decryptionUtils.doDemystify(result)
        var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
        
        for v in var:
            if 'm3u8' in v[1]:
                m3u8 = v[1]
            if 'file' in v[1]:
                file = v[1]
        url = m3u8 + file
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': page,'X-Requested-With':'ShockwaveFlash/20.0.0.286'})

        return url
    except:
        return