
import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sqlite3

import utils

dialog = utils.dialog
favoritesdb = utils.favoritesdb

conn = sqlite3.connect(favoritesdb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS favorites (name, url, mode, image);")
    c.executescript("CREATE TABLE IF NOT EXISTS keywords (keyword);")
except:
    pass
conn.close()


def List():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM favorites")
        for (name, url, mode, img) in c.fetchall():
            utils.addLink(name, url, int(mode), img, '', '', 'del')
        conn.close()
        xbmcplugin.endOfDirectory(utils.addon_handle)
    except:
        conn.close()
        utils.notify('No Favourites','No Favourites found')
        return


def Favorites(fav,mode,name,url,img):
    if fav == "add":
        delFav(url)
        addFav(mode, name, url, img)
        utils.notify('Favourite added','Video added to the favourites')
    elif fav == "del":
        delFav(url)
        utils.notify('Favourite removed','Video removed from the favourites')
        xbmc.executebuiltin('Container.Refresh')


def addFav(mode,name,url,img):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO favorites VALUES (?,?,?,?)", (name, url, mode, img))
    conn.commit()
    conn.close()


def delFav(url):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE url = '%s'" % url)
    conn.commit()
    conn.close()


