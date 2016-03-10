# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64
from liveresolver.modules import client

def resolve(url):
    try:
        pageUrl = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
    
        result = client.request(url, referer=referer, headers= { 'Host': urlparse.urlparse(url).netloc} )
        file = re.findall('file=([^&]+)',result)[0]
        streamer = re.findall('streamer=([^&]+)',result)[0]
        swf = re.findall('[\"\'](.+?.swf)[\"\']',result)[0]
        url = streamer + ' playpath=' + file + ' swfUrl=' + swf + ' live=1 token=Fo5_n0w?U.rA6l3-70w47ch flashver=WIN\\2020,0,0,286 timeout=13 swfVfy=1 pageUrl=' + pageUrl
        return url
    except:
        return
