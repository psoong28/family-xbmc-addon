# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        url = url.replace(referer,'').replace('?referer=', '')
        result = client.request(url, referer = referer)
        swf='http://www.janjuaplayer.com' + re.compile('SWFObject\(\"(.+?)".*?').findall(result)[0]
        vars = re.compile('id=(\d+)&s=([^&\'"]+).*?&pk=([^&\'"]+).*').findall(result)[0]
        id,channel,pk=vars[0],vars[1],vars[2]
        page2='http://www.janjuapublisher.com:1935/loadbalancer?' + channel
        result = client.request(page2, referer='http://www.janjuaplayer.com/resources/scripts/eplayer.swf')
        ip = re.compile(".*redirect=([\.\d]+).*").findall(result)[0]
        rtmp='rtmp://%s/live/'%ip
        url='%s playPath=%s?id=%s&pk=%s swfVfy=1 timeout=10 conn=S:OK live=true swfUrl=%s flashver=WIN\\2019,0,0,226 pageUrl=%s'%(rtmp,channel,id,pk,swf,url)
        return url
    except:
        return
