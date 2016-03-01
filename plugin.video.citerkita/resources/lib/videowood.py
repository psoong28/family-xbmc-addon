# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import re, urllib2
from resources.lib import client
from resources.lib import jsunpack

def getContent(url, post=''):
    if post: req = urllib2.Request(url, post)
    else: req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', url)
    response = urllib2.urlopen(req)
    result=response.read()
    response.close()
    return result

def resolve(url):
    # try:
        urls = re.sub(r'(?:http:|)\/\/', 'http://', url)
        # result = client.request(urls, referer=urls)
        result = getContent(urls)

        packed = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', result)

        unpacked = None
        if packed:
            # change radix before trying to unpack, 58-61 seen in testing, 62 worked for all
            packed = re.sub(r"(.+}\('.*', *)\d+(, *\d+, *'.*?'\.split\('\|'\))", "\g<01>62\g<02>", packed.group(1))
            unpacked = jsunpack.unpack(packed)
        if unpacked:
            r = re.search('.+["\']file["\']\s*:\s*["\'](.+?/video\\\.+?)["\']', unpacked)
            if r:
                stream_url = r.group(1).replace('\\', '')
        if stream_url:
            return stream_url
        
    # except:
    #     return




