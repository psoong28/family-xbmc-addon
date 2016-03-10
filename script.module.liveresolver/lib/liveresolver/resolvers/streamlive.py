# -*- coding: utf-8 -*-


import re,urlparse,json,requests
from liveresolver.modules import client
from liveresolver.modules.log_utils import log
import urllib,sys

from addon.common.addon import Addon
addon = Addon('script.module.liveresolver', sys.argv)

def resolve(url):
    
    try:
        page = url
        user,passw = addon.get_setting('streamlive_user'),addon.get_setting('streamlive_pass')

        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except: referer = url


        session = start_session()
        post_data = 'username=%s&password=%s&accessed_by=web&submit=Login'%(user,passw)
        resp = session.post('http://www.streamlive.to/login.php', data=post_data, headers = {'referer':'http://www.streamlive.to/login', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()})
        if resp.status_code!=200:
          addon.show_small_popup(title='Streamlive.to', msg='Failed to login')
        result = session.get(url).text
        if '"na_msg">This channel is a Premium channel.<' in result:
          addon.show_small_popup(title='Streamlive.to', msg='Premium channel. Upgrade your account to watch it!')
          return 

        html = result        
        if 'captcha' in html:
            try:
                answer = re.findall('Question\:.+?\:(.+?)<',html)[0].strip()
            except:
                answer = eval(re.findall('Question\:(.+?)<',html)[0].replace('=?',''))
            
            post = urllib.urlencode({"captcha":answer})
            html = session.post(page, data=post, headers={'referer':referer, 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to'}).text
        result = html
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]
        log(result)

        file = re.compile('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=WIN\\2019,0,0,226 live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        
        return url
    except:
        return


def start_session():
    s = requests.Session()
    html = s.get('http://www.streamlive.to', headers={'referer':'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()}).text
    if 'captcha' in html:
        try:
            answer = re.findall('Question\:.+?\:(.+?)<',html)[0].strip()
        except:
            answer = eval(re.findall('Question\:(.+?)<',html)[0].replace('=?',''))
        
        post = urllib.urlencode({"captcha":answer})
        html = s.post('http://www.streamlive.to', data=post, headers={'referer': 'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()}).text
        
    return s