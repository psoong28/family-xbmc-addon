#!/usr/bin/python

import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import re
import httplib
import urlparse
from os import path, system
from urllib2 import Request, URLError, urlopen
import xbmcaddon
import unicodedata
import json
import os
from resources.lib import xmltodict

host = "http://t.dfm2u.net/search/label/Filem"
searchURL = "http://www1.dfm2u.net/2013/05/filem.html"

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.citerkita"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
addon = xbmcaddon.Addon()
addonInfo = xbmcaddon.Addon().getAddonInfo
path = addon.getAddonInfo('path')
pic = path+"/icon.png"
picNext = path+"/resources/media/next.jpg"
picSearch = path+"/resources/media/search.jpg"
picNo = path+"/resources/media/null.jpg"
picFanart = path+"/fanart.jpg"
progress = xbmcgui.DialogProgress()

def getUrl(url, post='', referer=''):
    if post: req = urllib2.Request(url, post)
    else: req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    if referer:
      req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def playVideo(url, title, pic):
    xlistitem = xbmcgui.ListItem( title, iconImage=pic, thumbnailImage=pic, path=url)
    xlistitem.setInfo( "video", { "Title": title } )
    player = xbmc.Player()
    player.play(url, xlistitem)

def gedebug(strTxt):
    print '######################################################'
    print '### GEDEBUG: ' + str(strTxt)
    print '######################################################'
    return

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

def addSearch():
    searchStr = ''
    keyboard = xbmc.Keyboard(searchStr, 'Search')
    keyboard.doModal()
    if (keyboard.isConfirmed()==False):
      return
    searchStr=keyboard.getText()
    if len(searchStr) == 0:
      return
    else:
      return searchStr 

def showSearch():
    stext = addSearch()
    name = stext
    try:
        url = searchURL
        ok = showSearchList(url, name)
    except:
      pass

def showSearchList(url, txtSearch):
    try:
        for data in jsonData['feed']['entry']:
            title = data['title']['#text']
            title = re.sub('\sFull\sMovie', '', title)
            txtSearch = txtSearch.title()

            if txtSearch in title:
                content = data['content']['#text']
                regex = 'img.*?src=\\"(.+?)\\".*?Tahun.*?(\d{4}).*?<a.*?href=\\"(.+?)\\"'
                match = re.compile(regex).findall(content)

                for pic, year, link in match:
                    addDirectoryItem(title+' ('+year+')', {"name":title, "url":link, "mode":2, "thumbnail":pic}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)
    except:
        pass

def getMetaData(url):
    for data in jsonData['feed']['entry']:
        content = data['content']['#text']
        regex = 'img.*?src=\\"(.+?)\\".*?Tahun.*?(\d{4}).*?<a.*?href=\\"(.+?)\\"'
        match = re.compile(regex).findall(content)

        for thumbnail, year, link in match:
            if link == url:
                return {'thumbnail':thumbnail, 'year':year}
                break

def showMainMenu(url=''):  
    addDirectoryItem("[COLOR FFFFFFFF]Search[/COLOR]", {"name":"Carian", "url":searchURL, "mode":0}, picSearch)

    if not url: url = host
    content = getUrl(url)

    regex = 'post.*?name=\'\d+?\'.*?href=\'(.+?)\'>(.+?)./a'
    match = re.compile(regex, re.DOTALL).findall(content)
    for link, title in match:
        try:
            metaData = getMetaData(link)
            year = metaData['year']
            thumbnail = metaData['thumbnail']

            title = title+' ('+year+')'
        except:
            thumbnail = picNo
            pass

        addDirectoryItem(title, {"name":title, "url":link, "mode":2, "thumbnail":thumbnail}, thumbnail)

    # next page
    regex = 'blog-pager-older-link.*?href=\'(.+?)\'.*?>'
    link = re.compile(regex).findall(content)[0]
    title = '[I]Next Page[/I]'
    addDirectoryItem(title, {"name":title, "url":link, "mode":1}, picNext)

    xbmcplugin.endOfDirectory(thisPlugin)

def getSource(url, name, pic):
    content = getUrl(url)
    regex = 'forads\'>(.+?)</div'
    content = re.compile(regex, re.DOTALL).findall(content)[0]

    regex = 'iframe.*?src="(.+?)"'
    match = re.compile(regex).findall(content)

    progress.create('Progress', 'Please wait while we grab all source.')

    i = 1
    l = len(match)
    intl = str(l)+'.0'

    for link in match:
        vLink = getStream(link, name, pic)

        updateProgressBar(i, l, intl)
        if progress.iscanceled():
            progress.close()
            break

        if vLink:
            # gedebug(vLink)
            name = cleanHex(name)
            title = vLink['site'].upper()
            if not vLink['link']:
                title = '[COLOR red]'+title+'[/COLOR]'

            addDirectoryItem(title, {"name":name, "url":vLink['link'], "mode":3, "thumbnail":pic}, pic)
            i = i + 1

    xbmcplugin.endOfDirectory(thisPlugin)

def getStream(url, name, thumbnail):
    regex = '\/\/(.+?)\/'
    match = re.compile(regex).findall(url)[0]
    regex = '(?:www.|)(.+?)\.'
    site = re.compile(regex).findall(match)[0]
    if site == 'drive' or site == 'docs' : site = 'googledocs'
    if site == 'uptostream': 
        url = re.sub(r'iframe\/', '', url)
    # gedebug(url)
    try:
        urls = __import__('resources.lib.%s' % site, globals(), locals(), ['resolve'], -1)
        links = urls.resolve(url)
        link = links
        if site == 'googledocs':
            link = links[0]['url']
        if site == 'dailymotion':
            link = links[0]['url']

        return {'link':link, 'site':site}
    except:
        return

def updateProgressBar(i, l, intl):
    percent = int( ( i / float(intl) ) * 100)
    message = "Checking Available Source : " + str(i) + " out of "+str(l)
    progress.update( percent, "", message, "" )
    xbmc.sleep( 1000 )

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}  

# __init___
content = getUrl(searchURL)
regex = '\.judul-label\{.*?<\/script.*?src="(.+?)"'
match = re.compile(regex).findall(content)[0]

content = getUrl(match)
jsonData = xmltodict.parse(content)


def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="", thumbnailImage=pic)
    li.setInfo( "video", { "Title" : name, "FileName" : name} )
    li.setProperty('Fanart_Image', picFanart)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
name = urllib.unquote(name)
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))
postData =  str(params.get("postData", ""))
page =  str(params.get("page", 1))
thumbnail = str(params.get("thumbnail", ""))
thumbnail = urllib.unquote(thumbnail)

#### ACTIONS ####
if not sys.argv[2]:
    pass#print  "Here in default-py going in showContent"
    ok = showMainMenu()
else:
    if mode == str(0):
        ok = showSearch()
    if mode == str(1):
        ok = showMainMenu(url)
    if mode == str(2):
        ok = getSource(url, name, thumbnail)
    if mode == str(3):
        ok = playVideo(url, name, thumbnail)
