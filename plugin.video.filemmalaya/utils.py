import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sqlite3, urlresolver, base64

from jsunpack import unpack

from StringIO import StringIO
import gzip

__scriptname__ = "filem malaya"
__author__ = "indiecrew"
__scriptid__ = "plugin.video.filemmalaya"
__credits__ = "mortael"
__version__ = "0.0.4"

List = 'aHR0cHM6Ly9nb28uZ2wvNEhsRDBN'.decode('base64')

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}

openloadhdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id=__scriptid__)

progress = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

rootDir = addon.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)
resDir = os.path.join(rootDir, 'resources')
imgDir = os.path.join(resDir, 'images')
fmicon = xbmc.translatePath(os.path.join(rootDir, 'icon.png'))

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar(xbmc.translatePath(cookiePath))
Request = urllib2.Request

if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        try:
            cj.load()
        except:
            try:
                os.remove(xbmc.translatePath(cookiePath))
                pass
            except:
                dialog.ok('Oh oh','The Cookie file is locked, please restart Kodi')
                pass
    cookie_handler = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

favoritesdb = os.path.join(profileDir, 'favorites.db')


def getHtml(url, referer='', hdr=None, NoCookie=None, data=None):
    try:
        if not hdr:
            req = Request(url, data, headers)
        else:
            req = Request(url, data, hdr)
        if len(referer) > 1:
            req.add_header('Referer', referer)
        if data:
            req.add_header('Content-Length', len(data))
        response = urlopen(req, timeout=60)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            f.close()
        else:
            data = response.read()    
        if not NoCookie:
            # Cope with problematic timestamp values on RPi on OpenElec 4.2.1
            try:
                cj.save(cookiePath)
            except: pass
        response.close()
    except urllib2.HTTPError as e:
        data = e.read()
        if e.code == 503 and 'cf-browser-verification' in data:
            data = cloudflare.solve(url,cj, USER_AGENT)
    return data


def getHtml2(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urlopen(req)
    data = response.read()
    response.close()
    return data 


def PLAYVIDEO(url, name):
    progress.create('Play video', 'Searching videofile')
    progress.update( 10, "", "Loading video page", "" )
    videosource = getHtml(url, url)
    playvideo(videosource, name, url)


def playvideo(videosource, name, url=None):
    hosts = []
    if re.search('streamin\.to/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamin')
    if re.search('videorev\.cc/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Videorev')
    if re.search('vidto\.me/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Vidto')
    if re.search('openload\.(?:co|io)?/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('uptostream\.com/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Uptostream')
    if re.search('dailymotion\.com/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Dailymotion')
    if re.search('thevideos\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Thevideos')
    if re.search('watchvideo5\.us/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Watchvideo5')
    if re.search('youtube.com', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Youtube')
    if len(hosts) == 0:
        progress.close()
        dialog.ok('Oh no','Couldn\'t find any playable video')
        return
    elif len(hosts) > 1:
        if addon.getSetting("dontask") == "true":
            vidhost = hosts[0]            
        else:
            vh = dialog.select('Videohost:', hosts)
            vidhost = hosts[vh]
    else:
        vidhost = hosts[0]
    
    if vidhost == 'Streamin':
        progress.update( 30, "", "Loading Streamin", "" )
        streaminurl = re.compile(r"//(?:www\.)?streamin\.to/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        streaminurl = chkmultivids(streaminurl)
        streaminurl = 'http://streamin.to/embed-%s-670x400.html' % streaminurl
        progress.update( 50, "", "Loading Streamin", "Sending it to urlresolver" )
        video = urlresolver.resolve(streaminurl)
        if video:
            progress.update( 80, "", "Loading Streamin", "Found the video" )
            videourl = video
    elif vidhost == 'Videorev':
        progress.update( 30, "", "Loading Videorev", "" )
        videorevurl = re.compile(r"(https?://(?:www\.)?videorev\.cc/(?:embed-)?(?:[0-9a-zA-Z]+).html)", re.DOTALL | re.IGNORECASE).findall(videosource)
        videorevurl = chkmultivids(videorevurl)
        videorevsrc = getHtml(videorevurl,'', openloadhdr)
        videorevjs = re.compile("<script[^>]+>(eval[^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(videorevsrc)
        progress.update( 80, "", "Getting video file from Videorev", "" )
        videorevujs = unpack(videorevjs[0])
        videourl = re.compile('file:\s?"([^"]+mp4)"', re.DOTALL | re.IGNORECASE).findall(videorevujs)
        videourl = videourl[0]
    elif vidhost == 'Vidto':
        progress.update( 30, "", "Loading Vidto", "" )
        vidtourl = re.compile(r"//(?:www\.)?vidto\.me/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        vidtourl = chkmultivids(vidtourl)
        vidtourl = 'http://vidto.me/embed-%s-670x400.html' % vidtourl
        progress.update( 50, "", "Loading Vidto", "Sending it to urlresolver" )
        video = urlresolver.resolve(vidtourl)
        if video:
            progress.update( 80, "", "Loading Vidto", "Found the video" )
            videourl = video
    elif vidhost == 'OpenLoad':
        progress.update( 30, "", "Loading Openload", "" )
        openloadurl = re.compile(r"//(?:www\.)?o(?:pen)?load\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadurl = chkmultivids(openloadurl)
        openloadurl1 = 'http://openload.io/embed/%s/' % openloadurl
        progress.update( 50, "", "Loading Openload", "Sending it to urlresolver" )
        try:
            video = urlresolver.resolve(openloadurl1)
            if video:
                progress.update( 80, "", "Loading Openload", "Found the video" )
                videourl = video
        except:
            notify('Oh oh','Couldn\'t find playable OpenLoad link')
            return
    elif vidhost == 'Uptostream':
        progress.update( 30, "", "Loading Uptostream", "" )
        uptostreamurl = re.compile(r"//(?:www\.)?uptostream\.com/iframe/([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        uptostreamurl = chkmultivids(uptostreamurl)
        uptostreamurl = 'http://uptostream.com/iframe/%s/' % uptostreamurl
        progress.update( 50, "", "Loading Uptostream", "Sending it to urlresolver" )
        video = urlresolver.resolve(uptostreamurl)
        if video:
            progress.update( 80, "", "Loading Uptostream", "Found the video" )
            videourl = video
    elif vidhost == 'Dailymotion':
        progress.update( 30, "", "Loading Dailymotion", "" )
        dailymotionurl = re.compile(r'//(?:www\.)?dailymotion\.com/embed/video/([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        dailymotionurl = chkmultivids(dailymotionurl)
        dailymotionurl = 'http://www.dailymotion.com/embed/video/%s' % dailymotionurl
        progress.update( 50, "", "Loading Dailymotion", "Sending it to urlresolver" )
        video = urlresolver.resolve(dailymotionurl)
        if video:
            progress.update( 80, "", "Loading Dailymotion", "Found the video" )
            videourl = video
    elif vidhost == 'Thevideos':
        progress.update( 30, "", "Loading Thevideos", "" )
        thevideosurl = re.compile(r"//(?:www\.)?thevideos\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        thevideosurl = chkmultivids(thevideosurl)
        thevideosurl = 'http://thevideos.tv/embed-%s-728x410.html' % thevideosurl
        progress.update( 50, "", "Loading Thevideos", "Sending it to urlresolver" )
        video = urlresolver.resolve(thevideosurl)
        if video:
            progress.update( 80, "", "Loading Thevideos", "Found the video" )
            videourl = video
    elif vidhost == 'Watchvideo5':
        progress.update( 30, "", "Loading Watchvideo5", "" )
        watchvideo5url = re.compile(r"//(?:www\.)?watchvideo5\.us/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        watchvideo5url = chkmultivids(watchvideo5url)
        watchvideo5url = 'http://watchvideo5.us/embed-%s.html' % watchvideo5url
        progress.update( 50, "", "Loading Watchvideo5", "Sending it to urlresolver" )
        video = urlresolver.resolve(watchvideo5url)
        if video:
            progress.update( 80, "", "Loading Watchvideo5", "Found the video" )
            videourl = video
    elif vidhost == 'Youtube':
        progress.update( 40, "", "Loading Youtube", "" )
        youtubeurl = re.compile("youtube\.com/embed/([^']+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        youtubeurl = chkmultivids(youtubeurl)
        progress.update( 80, "", "Loading Youtube", "Getting video file from Youtube" )
        videourl = "plugin://plugin.video.youtube/?action=play_video&amp;videoid=" + youtubeurl

    progress.close()
    playvid(videourl, name)


def playvid(videourl, name):
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Movies'})
    xbmc.Player().play(videourl, listitem)


def addLink(name, url, mode, iconimage, desc, stream=None, fav='add'):
    contextMenuItems = []
    if fav == 'add': favtext = "Add to"
    elif fav == 'del': favtext = "Remove from"
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    favorite = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&fav=" + fav +
         "&favmode=" + str(mode) +
         "&mode=" + str('900') +
         "&img=" + urllib.quote_plus(iconimage) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    fanart = os.path.join(rootDir, 'fanart.jpg')
    if addon.getSetting('posterfanart') == 'true':
        fanart = iconimage
        liz.setArt({'poster': iconimage})
    liz.setArt({'fanart': fanart})
    if stream:
        liz.setProperty('IsPlayable', 'true')
    if len(desc) < 1:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": desc, "plotoutline": desc})
    contextMenuItems.append(('[COLOR skyblue]' + favtext + ' Filem Malaya favourites[/COLOR]', 'xbmc.RunPlugin('+favorite+')'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, page=None, channel=None, section=None, keyword='', Folder=True):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&page=" + str(page) +
         "&channel=" + str(channel) +
         "&section=" + str(section) +
         "&keyword=" + urllib.quote_plus(keyword) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    fanart = os.path.join(rootDir, 'fanart.jpg')
    if addon.getSetting('posterfanart') == 'true':
         fanart = iconimage
         liz.setArt({'poster': iconimage})
    liz.setArt({'fanart': fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=Folder)
    return ok


def _get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
    return default  


def chkmultivids(videomatch):
    videolist = list(set(videomatch))
    if len(videolist) > 1:
        i = 1
        hashlist = []
        for x in videolist:
            hashlist.append('Video ' + str(i))
            i += 1
        mvideo = dialog.select('Multiple videos found', hashlist)
        return videolist[mvideo]
    else:
        return videomatch[0]

    
def PlayMovie(name, url):
    if 'm3u8' in url:
       PlayStream(name, url)
    else:
       progress.create('Play video', 'Searching videofile')
       progress.update( 30, "", "Loading video page", "Sending it to urlresolver" )
       source = urlresolver.HostedMediaFile(url)
       if source:
          progress.update( 80, "", "Loading video page", "Found the video" )
          streamurl = source.resolve()
          if source.resolve()==False:
             progress.close()
             xbmc.executebuiltin("XBMC.Notification(Oh no!,Link Cannot Be Resolved,5000)")          
             return
       else:
             streamurl = url
       progress.close()
       iconimage = xbmc.getInfoImage("ListItem.Thumb")
       ok = True
       listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
       listitem.setInfo(type="Video", infoLabels={ "Title": name })
       ok = xbmcplugin.addDirectoryItem(addon_handle,url=streamurl,listitem=listitem)
       try:
          xbmc.Player().play(streamurl, listitem, False)
          return ok
       except: pass


def PlayStream(name, url):
    item = xbmcgui.ListItem(name, path = url)
    xbmcplugin.setResolvedUrl(addon_handle, True, item)
    return


def notify(header=None, msg='', duration=5000):
    if header is None: header = '[COLOR skyblue]Filem Malaya[/COLOR]'
    builtin = "XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, fmicon)
    xbmc.executebuiltin(builtin)


def cleantext(text):
    text = text.replace('&#8211;','-')
    text = text.replace('&#038;','&')
    text = text.replace('&#8217;','\'')
    text = text.replace('&#8216;','\'')
    text = text.replace('&#8230;','...')
    text = text.replace('&quot;','"')
    text = text.replace('&#039;','`')
    text = text.replace('&amp;','&')
    text = text.replace('&rsquo;','\'')
    return text


def searchDir(url, mode, page=None):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM keywords")
        for (keyword,) in c.fetchall():
            name = '[COLOR white]' + urllib.unquote_plus(keyword) + '[/COLOR]'
            addDir(name, url, mode, '', page=page, keyword=keyword)
    except: pass
    addDir('[COLOR skyblue]Add Keyword[/COLOR]', url, 902, '', '', mode, Folder=False)
    addDir('[COLOR skyblue]Clear list[/COLOR]', '', 903, '', Folder=False)
    xbmcplugin.endOfDirectory(addon_handle)


def newSearch(url, mode):
    vq = _get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    addKeyword(title)
    xbmc.executebuiltin('Container.Refresh')


def clearSearch():
    delKeyword()
    xbmc.executebuiltin('Container.Refresh')


def addKeyword(keyword):
    xbmc.log(keyword)
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO keywords VALUES (?)", (keyword,))
    conn.commit()
    conn.close()


def delKeyword():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM keywords;")
    conn.commit()
    conn.close()


def STREAM():
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == 'tvmal':
           addLink(name, url, 9, img, '', True)
    xbmcplugin.endOfDirectory(addon_handle)


def RADIO():
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == 'radmal':
           addLink(name, url, 9, img, '', True)
    xbmcplugin.endOfDirectory(addon_handle)


def fnow():
    addDir('[COLOR skyblue]Filem Terbaru[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == 'Now':
           if 'm3u8' in url:
               addLink(name, url, 8, img, '', True)
           else:
               addLink(name, url, 8, img, '')
    xbmcplugin.endOfDirectory(addon_handle)


def f40():
    addDir('[COLOR skyblue]Filem 1940an[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == '40an':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def f50():
    addDir('[COLOR skyblue]Filem 1950an[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == '50an':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def f60():
    addDir('[COLOR skyblue]Filem 1960an[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == '60an':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def f70():
    addDir('[COLOR skyblue]Filem 1970an[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == '70an':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def f80():
    addDir('[COLOR skyblue]Filem 1980an[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == '80an':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)

def KAROK():
    addDir('[COLOR skyblue]Peti Nyanyi[/COLOR] | [COLOR white]Filem Malaya[/COLOR]','','',os.path.join(imgDir, 'filem.png'),'')
    listhtml = getHtml(List, '')
    match = re.compile('#EXTINF:-1, tvg-logo="(.+?)" group-title="(.+?)", (.+?)\n(.+?)\n', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, group, name, url in match:
        if group == 'Karok':
           addLink(name, url, 8, img, '')
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
