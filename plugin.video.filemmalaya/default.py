import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs, utils, favorites
import telefilem

socket.setdefaulttimeout(60)

xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)

progress = utils.progress
dialog = utils.dialog

imgDir = utils.imgDir
rootDir = utils.rootDir

cachedir = 'special://profile/addon_data/plugin.video.filemmalaya/cache'

def INDEX():
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem[/COLOR]','',4,os.path.join(rootDir, 'icon.png'),'')
    # utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Drama[/COLOR]','',50,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Siaran TV[/COLOR]','',2,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Siaran Radio[/COLOR]','',3,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Peti Nyanyi[/COLOR]','',7,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR=900C3F]---[/COLOR]','','',os.path.join(rootDir, 'icon.png'),'')
    # utils.addDir('[COLOR grey]Favourites[/COLOR]: [COLOR skyblue]My List[/COLOR]','',901,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR grey]Tetapan[/COLOR]: [COLOR skyblue]Peribadi[/COLOR]','',904,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR grey]Twitter[/COLOR]: [COLOR skyblue]@MRNetworkTV[/COLOR]','','',os.path.join(rootDir, 'icon.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def FILEM():
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem Terbaru[/COLOR]','',13,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Telefilem Terbaru[/COLOR]','',30,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem 1940an[/COLOR]','',14,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem 1950an[/COLOR]','',15,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem 1960an[/COLOR]','',16,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem 1970an[/COLOR]','',17,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem 1980an[/COLOR]','',18,os.path.join(rootDir, 'icon.png'),'')
    # utils.addDir('[COLOR skyblue]Filem Malaya[/COLOR] | [COLOR white]Filem (1990an-2020an)[/COLOR]','',19,os.path.join(rootDir, 'icon.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle)

if 'disclaimer' in sys.argv[0]:
    try:
        f = xbmcvfs.File('special://home/addons/plugin.video.filemmalaya/disclaimer.txt')
        text = f.read() ; f.close()
        label = '[COLOR skyblue]Disclaimer[/COLOR]'
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(100)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                win.getControl(1).setLabel(label)
                win.getControl(5).setText(text)
                retry = 0
            except:
                retry -= 1
    except:
        pass

if 'clearcache' in sys.argv[0]:
    dirs, files = xbmcvfs.listdir(cachedir)
    for f in files:
        xbmcvfs.delete(cachedir + f)
    dialog = xbmcgui.Dialog()
    dialog.notification('[COLOR skyblue]Filem Malaya[/COLOR]', 'Clearing cache...', xbmcgui.NOTIFICATION_INFO, 5000)
    quit()

def Settings():
    addon.openSettings(sys.argv[0])
    sys.exit()

if not addon.getSetting('already_shown') == 'true':
    shown = dialog.yesno('This addon contains copyright material','You may enter only if you agree with our disclaimer', nolabel='Exit', yeslabel='Enter')
    addon.setSetting('already_shown', 'true')

def getParams():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

params = getParams()
url = None
name = None
mode = None
img = None
page = 1
fav = None
favmode = None
channel = None
keyword = None

try: url = urllib.unquote_plus(params["url"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass
try: page = int(params["page"])
except: pass
try: img = urllib.unquote_plus(params["img"])
except: pass
try: fav = params["fav"]
except: pass
try: favmode = int(params["favmode"])
except: pass
try: channel = int(params["channel"])
except: pass
try: keyword = urllib.unquote_plus(params["keyword"])
except: pass

if mode is None: INDEX()

elif mode == 2: utils.STREAM()
elif mode == 3: utils.RADIO()
elif mode == 4: FILEM()
elif mode == 5: TELEFILEM()
elif mode == 6: DRAMA()
elif mode == 7: utils.KAROK()
elif mode == 8: utils.PlayMovie(name, url)
elif mode == 9: utils.PlayStream(name, url)

elif mode == 10: flatest.Main()
elif mode == 11: flatest.List(url)
elif mode == 12: flatest.Playvid(url, name)
elif mode == 13: utils.fnow()
elif mode == 14: utils.f40()
elif mode == 15: utils.f50()
elif mode == 16: utils.f60()
elif mode == 17: utils.f70()
elif mode == 18: utils.f80()

elif mode == 30: telefilem.Main()
elif mode == 31: telefilem.List(url)
elif mode == 32: telefilem.Playvid(url, name)
elif mode == 33: telefilem.Search(url, keyword)

elif mode == 900: favorites.Favorites(fav,favmode,name,url,img)
elif mode == 901: favorites.List()
elif mode == 902: utils.newSearch(url, channel)
elif mode == 903: utils.clearSearch()
elif mode == 904: Settings()
   
xbmcplugin.endOfDirectory(utils.addon_handle)