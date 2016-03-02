import xbmcplugin,xbmcgui,xbmcaddon,xbmc,os


try:
    import youtube
    ICONIMAGE = 'http://i.ytimg.com/vi/4Qs7bxkpy2g/0.jpg'
    URL   =   youtube.GetVideoInfo('4Qs7bxkpy2g')[0]['best']
    liz = xbmcgui.ListItem('Xunity Welcome', iconImage='DefaultVideo.png', thumbnailImage=ICONIMAGE)
    liz.setInfo(type='Video', infoLabels={'Title':'Xunity Welcome'})
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(URL, liz)
    xbmc.Player().play(pl)
except:pass
