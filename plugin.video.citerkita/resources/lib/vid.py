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

def resolve(url):
    try:
        result = client.request(url, referer=url)

        for match in re.finditer('(eval\(function.*?)</script>', result, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            r = re.search('file\s*:\s*"([^"]+)', js_data)
            if r:
                return r.group(1)
        
        r = re.search('file\s*:\s*"([^"]+)', html)
        if r:
            return r.group(1)
        
    except:
        return




