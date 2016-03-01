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


def resolve(url):
    try:
        url = re.sub(r'(?:http:|)\/\/', 'http://', url)
        # result = client.request(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

        response = urllib2.urlopen(req)
        result=response.read()
        response.close()
        regex = 'source.*?src=\'(.+?)\'.*?data-res=\'(.+?)\''
        match = re.compile(regex).findall(result)

        data = {}
        for url, quality in match:
            data['url'] = url
            data['quality'] = quality

        return 'http:'+data['url']

    except:
        return




