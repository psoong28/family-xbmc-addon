import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

def Main():
    utils.addDir('[COLOR skyblue]Telefilem Terbaru[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(utils.imgDir, 'telefilem.png'),'')
    # utils.addDir('[COLOR skyblue]Search[/COLOR]','http://www.layandrama.net/?s=',33,'','')
    List('http://www.layandrama.net/category/telemovie/page/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh no','It looks like this website is under maintenance')
        return None
    match = re.compile('<ul class="carousel-list">(.*?)<div class="carousel-prev">', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile(r'<a class="clip-link" data-id=".*?" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    for name, videopage, img in match1:
        name = utils.cleantext(name)
        utils.addLink(name, videopage, 32, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def Playvid(url, name):
    utils.PLAYVIDEO(url, name)

def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 33)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)