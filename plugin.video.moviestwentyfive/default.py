import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcaddon,os,base64,cookielib
from addon.common.addon import Addon
from addon.common.net import Net
import silent


#www.movie25.so - by The_Silencer 2016 v0.20

#Global
addon_id = 'plugin.video.moviestwentyfive'
local = xbmcaddon.Addon(id=addon_id)
movie25path = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = movie25path+'/art'
net = Net()
custurl = local.getSetting('custurl')
custurl1 = custurl+'/'
custurltv = local.getSetting('custurltv')
cookie_path = os.path.join(datapath)
cookiejar = os.path.join(cookie_path,'watchseries.lwp')


#Watchseries Login for tv shows
def LoginStartup():
        watchseries_account = local.getSetting('watchseries-account')
        hide_message = local.getSetting('hide-successful-login-messages')
        loginurl = custurltv+'/login'
        if watchseries_account == 'true':
                login = local.getSetting('watchseries-username')
                password = local.getSetting('watchseries-password')
                data = net.http_POST(loginurl,{'email' : login, 'password' : password}).content
                success=re.compile('<li>Hi, (.+?)</li>',re.DOTALL).findall(data)
                if success:
                        net.save_cookies(cookiejar)
                        if hide_message == 'false':
                                print 'WatchSeries Account: login successful'
                                silent.Notify('small','WatchSeries Account:', 'login successful.',6000)
                if not success:
                        print 'WatchSeries  Account: login failed'
                        silent.Notify('big','WatchSeries Account:','Login failed: check your username and password', '')
                        
#Kid Mode Menu
def KIDMODE():
        addDir('Parent View',custurl1,46,os.path.join(art,'PARENT_VIEW.png'),None,None)
        addDir('Kid Movies',custurl1,44,os.path.join(art,'KIDS_MOVIES.png'),None,None)
        addDir('Kid TV Shows',custurl1,45,os.path.join(art,'KIDS_TV.png'),None,None)

def PARENTS():
        Password = local.getSetting('parent-password')
        keyb = xbmc.Keyboard('', 'Please Enter the Parent Password',True)
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)  
                if encode != Password:
                        addDir('Sorry wrong password please try again',url,46,'',None,None)
                else:
                        addDir('Movies',custurl1,16,os.path.join(art,os.path.join(art,'MOVIES.png')),None,None)
                        addDir('TV',custurl1,17,os.path.join(art,os.path.join(art,'TV_SHOWS.png')),None,None)
                        addDir('Settings',custurl1,18,os.path.join(art,os.path.join(art,'SETTINGS.png')),None,None)

def KIDMOVIES():
        MYFAVS = silent.getFavoritesKIDMOVIE()
        try:
                for name,url,year in MYFAVS:
                        addFAVDir(name,url,year)
        except:
                pass

def KIDTV():
        MYFAVS = silent.getFavoritesKIDTV()
        try:
                for name,url,types in MYFAVS:
                        addFAVDirTV(name,url,types)
        except:
                pass

#Urlresolver setttings
def ResolverSettings():
        urlresolver.display_settings()


def SETTINGS():
        addDir('Add-on Settings',custurl1,42,os.path.join(art,'ADDON.png'),None,None)
        addDir('Resolver Settings',custurl1,43,os.path.join(art,'RESOLVER.png'),None,None)

#Redirect Check for movies
def URLCHECK():
        setadd = custurl1
        url='http://movie25.com'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        resp = urllib2.urlopen(req)
        url2 = resp.geturl()
        print setadd
        print url2
        if setadd == url2:
                URLCHECK2()
        else:
                addDir('Movie25 address has changed',custurl1,16,os.path.join(art,''),None,None)
                addDir('Please change custom address in settings from:',custurl1,17,os.path.join(art,''),None,None)
                addDir(setadd,custurl1,17,os.path.join(art,''),None,None)
                addDir('Change to:',custurl1,17,os.path.join(art,''),None,None)
                addDir(url2,custurl1,17,os.path.join(art,''),None,None)
                addDir('Please dont add the / at the end of the url.',custurl1,17,os.path.join(art,''),None,None)

#Redirect Check for TV shows        
def URLCHECK2():
        setadd2 = custurltv+'/'
        url='http://watchseries.to'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        resp = urllib2.urlopen(req)
        url2 = resp.geturl()
        print setadd2
        print url2
        if setadd2 == url2:
                CATEGORIES()
        else:
                addDir('TV Shows address has changed',custurl1,16,os.path.join(art,''),None,None)
                addDir('Please change custom address in settings from:',custurl1,17,os.path.join(art,''),None,None)
                addDir(setadd2,custurl1,17,os.path.join(art,''),None,None)
                addDir('Change to:',custurl1,17,os.path.join(art,''),None,None)
                addDir(url2,custurl1,17,os.path.join(art,''),None,None)
                addDir('Please dont add the / at the end of the url.',custurl1,17,os.path.join(art,''),None,None)

#Main menu
def CATEGORIES():
        LoginStartup()
        KidMode = local.getSetting('kid-mode')
        if KidMode == 'true':
                KIDMODE()
        else:
                addDir('Movies',custurl1,16,os.path.join(art,'MOVIES.png'),None,None)
                addDir('TV',custurl1,17,os.path.join(art,'TV_SHOWS.png'),None,None)
                addDir('Settings',custurl1,18,os.path.join(art,'SETTINGS.png'),None,None)

#Menu for Movies
def MOVIES():
        MYFAVS = silent.getFavoritesKIDMOVIE2()
        addDir('Top 9',custurl1,51,os.path.join(art,'featured1.png'),None,None)
        addDir('Featured',custurl1+'/featured/',1,os.path.join(art,'featured1.png'),None,None)
        addDir('New Releases',custurl1+'/new-release/',1,os.path.join(art,'NEW_RELEASES.png'),None,None)
        addDir('Latest Added',custurl1+'/latest-added/',1,os.path.join(art,'LATEST_ADDED.png'),None,None)
        addDir('Latest HD',custurl1+'/latest-hd/',1,os.path.join(art,'latesthd.png'),None,None)
        addDir('Most Viewed',custurl1+'/most-popular/',1,os.path.join(art,'MOST_VIEWED.png'),None,None)
        addDir('Most Voted',custurl1+'movies/most-voted/',1,os.path.join(art,'MOST_VOTED.png'),None,None)
        addDir('A-Z',custurl1,5,os.path.join(art,'A_Z.png'),None,None)
        addDir('Genres',custurl1,8,os.path.join(art,'GENRE.png'),None,None)
        addDir('Year',custurl1,13,os.path.join(art,'year1.png'),None,None)
        addDir('Search',custurl1,6,os.path.join(art,'search1.png'),None,None)
        addDir('Favorites',custurl1,7,os.path.join(art,'FAVORITE.png'),None,None)
        if MYFAVS:
                addDir('Kid Movies',custurl1,44,os.path.join(art,'KIDS_MOVIES.png'),None,None)
                

#List of Years
def YEAR():
        addDir('2017',custurl1+'search.php?year=2017',1,'',None,None)
        addDir('2016',custurl1+'search.php?year=2016',1,'',None,None)
        addDir('2015',custurl1+'search.php?year=2015',1,'',None,None)
        addDir('2014',custurl1+'search.php?year=2014',1,'',None,None)
        addDir('2013',custurl1+'search.php?year=2013',1,'',None,None)
        addDir('2012',custurl1+'search.php?year=2012',1,'',None,None)
        addDir('2011',custurl1+'search.php?year=2011',1,'',None,None)
        addDir('2010',custurl1+'search.php?year=2010',1,'',None,None)
        addDir('2009',custurl1+'search.php?year=2009',1,'',None,None)
        addDir('2008',custurl1+'search.php?year=2008',1,'',None,None)
        addDir('2007',custurl1+'search.php?year=2007',1,'',None,None)
        addDir('2006',custurl1+'search.php?year=2006',1,'',None,None)
        addDir('2005',custurl1+'search.php?year=2005',1,'',None,None)
        addDir('2004',custurl1+'search.php?year=2004',1,'',None,None)
        addDir('2003',custurl1+'search.php?year=2003',1,'',None,None)
        addDir('2002',custurl1+'search.php?year=2002',1,'',None,None)
        addDir('2001',custurl1+'search.php?year=2001',1,'',None,None)
        addDir('2000',custurl1+'search.php?year=2000',1,'',None,None)
        addDir('1999',custurl1+'search.php?year=1999',1,'',None,None)
        addDir('1998',custurl1+'search.php?year=1998',1,'',None,None)
        addDir('1997',custurl1+'search.php?year=1997',1,'',None,None)
        addDir('1996',custurl1+'search.php?year=1996',1,'',None,None)
        addDir('1995',custurl1+'search.php?year=1995',1,'',None,None)
        addDir('1994',custurl1+'search.php?year=1994',1,'',None,None)
        addDir('1993',custurl1+'search.php?year=1993',1,'',None,None)
        addDir('1992',custurl1+'search.php?year=1992',1,'',None,None)
        addDir('1991',custurl1+'search.php?year=1991',1,'',None,None)
        addDir('1990',custurl1+'search.php?year=1990',1,'',None,None)
        addDir('1989',custurl1+'search.php?year=1989',1,'',None,None)
        addDir('1988',custurl1+'search.php?year=1988',1,'',None,None)
        addDir('1987',custurl1+'search.php?year=1987',1,'',None,None)
        addDir('1986',custurl1+'search.php?year=1986',1,'',None,None)
        addDir('1985',custurl1+'search.php?year=1985',1,'',None,None)
        addDir('1984',custurl1+'search.php?year=1984',1,'',None,None)
        addDir('1983',custurl1+'search.php?year=1983',1,'',None,None)
        addDir('1982',custurl1+'search.php?year=1982',1,'',None,None)
        addDir('1981',custurl1+'search.php?year=1981',1,'',None,None)
        addDir('1980',custurl1+'search.php?year=1980',1,'',None,None)
        addDir('1979',custurl1+'search.php?year=1979',1,'',None,None)
        addDir('1978',custurl1+'search.php?year=1978',1,'',None,None)
        addDir('1977',custurl1+'search.php?year=1977',1,'',None,None)
        addDir('1976',custurl1+'search.php?year=1976',1,'',None,None)
        addDir('1975',custurl1+'search.php?year=1975',1,'',None,None)
        addDir('1974',custurl1+'search.php?year=1974',1,'',None,None)
        addDir('1973',custurl1+'search.php?year=1973',1,'',None,None)
        addDir('1972',custurl1+'search.php?year=1972',1,'',None,None)
        addDir('1971',custurl1+'search.php?year=1971',1,'',None,None)
        addDir('1970',custurl1+'search.php?year=1970',1,'',None,None)
        
########
#TV Menu
########
def TV():
        watchseries_account = local.getSetting('watchseries-account')
        MYFAVS = silent.getFavoritesKIDTV2()
        if watchseries_account == 'true':
                addDirTV('My Watch List',custurltv+'/my-watchlist',53,os.path.join(art,'FAVORITE.png'),None)
                addDirTV('My TV Listings',custurltv+'/my-tv-listings',57,os.path.join(art,'FAVORITE.png'),None)
        addDirTV('Most Popular',custurltv+'/new',36,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Newest Episodes',custurltv+'/latest',36,os.path.join(art,'NEW_EPISODES.png'),None)
        addDirTV('A-Z',custurltv+'/letters/09',33,os.path.join(art,'A_Z.png'),None)
        addDirTV('Genres',custurltv+'/genres/drama',35,os.path.join(art,'GENRE.png'),None)
        addDirTV('TV Schedule',custurltv+'/tvschedule',38,os.path.join(art,'TV_SCHEDULE.png'),None)
        addDirTV('Search',custurltv,37,os.path.join(art,'search1.png'),None)
        addDirTV('Favorites',custurltv,39,os.path.join(art,'FAVORITE.png'),None)
        if MYFAVS:
                addDir('Kid TV Shows',custurl1+'',45,os.path.join(art,'KIDS_TV.png'),None,None)
                
#My Tracked List - login intergration
def MYTRACKED(url):
        net.set_cookies(cookiejar)
        match = re.compile('<div style="width: 158px;">(.+?)</div>').findall(net.http_GET(url).content)
        for name in match:
                addDirTV(name,url,58,'',None)

def MYTRACKED2(name,url):
        print url
        net.set_cookies(cookiejar)
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<div style="width:.+?">'+name+'</div></a>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li title="(.+?) - Season (.+?) Episode (.+?),.+?">.+?<a href="(.+?)"'
        match = re.findall(pattern,str(data))

        data2=re.compile('<div style="width:.+?">'+name+'</div></a>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern2 = '<div style="text-align: center; font-size: small; line-height: 17px;">(.+?)</div>'
        match2 = re.findall(pattern2,str(data2))
        for name,season,episode,url in match:
                nono = '</a>'
                name = silent.CLEAN(name)
                if nono not in name:
                        if EnableMeta == 'true':
                                addDirTV('%s - Seas. %s : Ep. %s' %(name,season,episode),custurltv+url+'@'+name+'@'+season+'@'+episode,31,'','new')
                        if EnableMeta == 'false':
                                addDirTV(name,custurltv+url,31,'',None)
        for name in match2:
                addDirTV('Sorry no tracked show for this day',custurltv+url,31,'',None)

#MY Watchlist - login intergration
def MYWATCHLIST(url):
        net.set_cookies(cookiejar)
        match=re.compile('<a href="(.+?)"><b>(.+?) \(.+?\)</b></a> &nbsp;<a class="remove-tracker-show-link deTrackTvShowEvent" href="javascript:setTrackedStatus\((.+?),.+?"').findall(net.http_GET(url).content)
        for url,name,showid in match:
                addDirTV(name,custurltv+url,55,'','tvshow')

#Remove title from your tracked list - login intergration
def REMOVETRACKED(name,url):
        print name
        url = custurltv+'/my-watchlist'
        net.set_cookies(cookiejar)
        match = re.search('<a href=".+?"><b>'+name+' \(.+?\)</b></a> &nbsp;<a class="remove-tracker-show-link deTrackTvShowEvent" href="javascript:setTrackedStatus\((.+?),.+?"',(net.http_GET(url).content))
        showid = match.group(1)
        print 'This is show id from match:'
        print showid
        loginurl = custurltv+'/set-tracked-show'
        net.http_POST(loginurl,{'show_id' : showid, 'action' : 'set-untracked'}).content
        
        xbmc.executebuiltin("XBMC.Container.Refresh")

#Add title to your tracked list - login intergration
def ADDTRACKED(name,url):
        print name
        print url
        url = url.split('@')[0]
        print url
        net.set_cookies(cookiejar)
        match = re.search('<a href="javascript:setTrackedStatus\((.+?),\'set-tracked\'\)"',(net.http_GET(url).content))
        showid = match.group(1)
        print 'This is show id from match:'
        print showid
        loginurl = custurltv+'/set-tracked-show'
        net.http_POST(loginurl,{'show_id' : showid, 'action' : 'set-tracked'}).content
        silent.Notify('small',name+':', 'successfully added to your track list.',6000)
        

#MY Watchlist view - login intergration
def MYWATCHLIST2(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        try:
                episode = url.split('@')[3]
        except:
                episde = ''
        try:
                season = url.split('@')[2]
        except:
                season = ''
        try:
                title = url.split('@')[1]
        except:
                title = ''
        try:
                url = url.split('@')[0]
        except:
                url = ''
        match=re.compile('<h2 class="lists" >.+?<a href="(.+?)" itemprop="url"><span itemprop="name">(.+?)</span>',re.DOTALL).findall(net.http_GET(url).content)
        for url,name in match:
                if EnableMeta == 'true':
                        addDirTV(name,url+'@'+title,32,'','season')
                if EnableMeta == 'false':
                        addDirTV(name,url+'@'+title,32,'',None)
                
#Popular TV menu
def POPULAR():
        addDirTV('Popular this week',custurltv+'new',22,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Series',custurltv,26,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Cartoons',custurltv,27,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Documentaries',custurltv,28,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Shows',custurltv,29,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Sports',custurltv,30,os.path.join(art,'MOST_POPULAR.png'),None)

#TV Schedule menu
def SCHEDULE(url):
        match=re.compile('<div style="width: 153px;">(.+?)</div>').findall(net.http_GET(url).content)
        for name in match:
                addDirTV(name,url,52,'',None)
                        
#A-Z TV list
def AZTV(url):
        match=re.compile('<li><a href="(.+?)".+?>(.+?)</a></li>').findall(net.http_GET(url).content)
        for url,name in match:
                icon = os.path.join(art,name+'.png')
                ok = ['09','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
                if name in ok:
                        addDirTV(name,custurltv+url,34,icon,None)

#Genres TV list
def GENRESTV(url):
        match=re.compile('<a href="(.+?)" class="sr-header" title=".+?">(.+?)</a>').findall(net.http_GET(url).content)
        for url,name in match:
                nono = ['How To Watch', 'DMCA', 'Contact Us', 'Home', 'New Releases', 'Latest Added', 'Featured Movies', 'Latest HD Movies', 'Most Viewed', 'Most Viewed', 'Most Voted', 'Genres', 'Submit Links']
                if name not in nono:
                        addDirTV(name,custurltv+url,34,'',None)

#Search for Movies
def SEARCHTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search TV Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                print encode
                url = custurltv+'/search/'+encode
                print url
                match=re.compile('<div valign="top" style="padding-left: 10px;">.+?<a href="(.+?)" title="(.+?)"',re.DOTALL).findall(net.http_GET(url).content) 
                for url,name in match:
                        name = silent.CLEAN(name)
                        if EnableMeta == 'true':
                               addDirTV(name,custurltv+url+'@'+name,31,'','tvshow')
                        if EnableMeta == 'false':
                               addDirTV(name,custurltv+url,31,'',None)

def LIST(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<li><a href="(.+?)" title=".+?">(.+?)<span class="epnum">(.+?)</span></a></li>').findall(net.http_GET(url).content)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

def NEWLINKS(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<li><a href="(.+?)">(.+?) Seas. (.+?) Ep. (.+?) \(.+?\).+?</li>',re.DOTALL).findall(net.http_GET(url).content)
        for url,name,season,episode in match:
                nono = '</a>'
                name = silent.CLEAN(name)
                if nono not in name:
                        if EnableMeta == 'true':
                                addDirTV('%s - Seas. %s : Ep. %s' %(name,season,episode),custurltv+url+'@'+name+'@'+season+'@'+episode,23,'','new')
                        if EnableMeta == 'false':
                                addDirTV(name,custurltv+url,23,'',None)

def NEWLINKS2(url,name):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<div style="width:.+?">'+name+'</div></a>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li title="(.+?) - Season (.+?) Episode (.+?),.+?"><a href="(.+?)"'
        match = re.findall(pattern,str(data))
        for name,season,episode,url in match:
                nono = '</a>'
                name = silent.CLEAN(name)
                if nono not in name:
                        if EnableMeta == 'true':
                                addDirTV('%s - Seas. %s : Ep. %s' %(name,season,episode),custurltv+url+'@'+name+'@'+season+'@'+episode,31,'','new')
                        if EnableMeta == 'false':
                                addDirTV(name,custurltv+url,31,'',None)

def INDEXTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<ul class="listings">(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li><a href="(.+?)">(.+?) Seas..+?</a></li>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,23,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,23,'',None)

def INDEX2(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Series\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

def INDEX3(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Cartoons\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

def INDEX4(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Documentaries\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

def INDEX5(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Shows\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

def INDEX6(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular  Sports\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,custurltv+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,custurltv+url,31,'',None)

#Find Seasons for shows
def SEASONS(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        try:
                episode = url.split('@')[3]
        except:
                episde = ''
        try:
                season = url.split('@')[2]
        except:
                season = ''
        try:
                title = url.split('@')[1]
        except:
                title = ''
        try:
                url = url.split('@')[0]
        except:
                url = ''
        match=re.compile('<h2 class="lists" >.+?<a href="(.+?)" itemprop="url"><span itemprop="name">(.+?)</span>',re.DOTALL).findall(net.http_GET(url).content)
        for url,name in match:
                if EnableMeta == 'true':
                        addDirTV(name,url+'@'+title,32,'','season')
                if EnableMeta == 'false':
                        addDirTV(name,url+'@'+title,32,'',None)

#Find Episodes for shows
def EPISODES(name,url):
        title = url.split('@')[1]
        url = url.split('@')[0]
        season = name
        print url
        match=re.compile('<a href="(.+?)".+?<span class="" itemprop=".+?">(.+?)&nbsp;&nbsp;&nbsp;(.+?) </span>\n\t\t\t\t\t\t\t<span class=".+?"  style=".+?"><b>.+?</b> <span itemprop=".+?">(.+?)</span>',re.DOTALL).findall(net.http_GET(url).content)                                      
        for url,episode,name,date in match:
                print episode
                name = silent.CLEAN(name)
                addDirTV('%s    :    %s   :   %s' %(episode,date,name),custurltv+url+'@'+title+'@'+season+'@'+episode,23,'','new')

#First page with Hosters
def VIDEOLINKSTV(url):
        episode = url.split('@')[3]
        print 'Episode = '+episode
        season = url.split('@')[2]
        print 'Season = '+season
        title = url.split('@')[1]
        print 'Title = '+title
        url = url.split('@')[0]
        print 'Url = '+url
        url = url.replace('https://twitter.com/share','')
        print 'Url ='+url
        match=re.compile('<a target="_blank"  href="(.+?)" class="buttonlink" title="(.+?)"').findall(net.http_GET(url).content)
        match2=re.compile('<p><strong>Sorry, there are no links available for this (.+?).</strong></p>').findall(net.http_GET(url).content)
        for url,name in match:
                nono = ['Sponsored']
                if name not in nono:
                        addDirTV(name,custurltv+url+'@'+title+'@'+season+'@'+episode,24,'',None)
        for name in match2:
                addDirTV('[B][COLOR yellow]Sorry, no links available yet[/COLOR][/B]',custurltv+url,24,'',None)

#Get the Final Hoster link
def VIDEOLINKS2TV(name,url):
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        print 'URL = '+url
        encoded = url.replace('http://thewatchseries.to/cale.html?r=', '')
        print 'THIS IS ENCODED FROM THE URL'
        print encoded
        decoded = base64.b64decode(encoded)
        print 'THIS IS THE DECODE PRINT OUT'
        print decoded
        STREAMTV(name,decoded+'@'+title+'@'+season+'@'+episode)

#Pass url to urlresolver
def STREAMTV(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETATV(name,url,'new')
                try: img = infoLabels['cover_url']
                except: img= iconimage
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        print 'URL going to urlresolver'
        print url
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                print streamlink
                addLinkTV(name,streamlink+'@'+title+'@'+season+'@'+episode,img)
        except:
                silent.Notify('small','Sorry Link Removed:', 'Please try another one.',9000)

def addLinkTV(name,url,iconimage):
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        season = season.replace('Season ', '')
        episode = episode.replace('Episode ', '')
        ok=True
        liz=xbmcgui.ListItem('%s (%sx%s)' %(title,season,episode), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": '%s (%sx%s)' %(title,season,episode) } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def addDirTV(name,url,mode,iconimage,types):
        EnableFanArt = local.getSetting('Enable-Fanart')
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETATV(name,url,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        contextMenuItems = []
        if mode == 31:
                contextMenuItems = []
                contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
                contextMenuItems.append(('Add to My Tracked Shows', 'XBMC.RunPlugin(%s?mode=56&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=40&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                contextMenuItems.append(('Add to Kids TV', 'XBMC.RunPlugin(%s?mode=49&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if mode == 55:
                contextMenuItems = []
                contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
                contextMenuItems.append(('Remove From My Tracked Shows', 'XBMC.RunPlugin(%s?mode=54&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addFAVDirTV(name,url,types):
        EnableFanArt = local.getSetting('Enable-Fanart')
        mode = 31
        iconimage = ''
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETATV(name,url,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library Context Menu
        contextMenuItems = []
        contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
        contextMenuItems.append(('Remove from Favorites', 'XBMC.RunPlugin(%s?mode=41&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
        contextMenuItems.append(('Remove from Kids TV', 'XBMC.RunPlugin(%s?mode=50&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
        
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ##############################
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

########
########
########

#Return Favorites List *temp need to fix in silent*
def GETMYFAVS():
        MYFAVS = silent.getFavorites()
        try:
                for name,url,year in MYFAVS:
                        addFAVDir(name,url,year)
        except:
                pass

def GETMYFAVSTV():
        MYFAVS = silent.getFavoritesTV()
        try:
                for name,url,types in MYFAVS:
                        addFAVDirTV(name,url,types)
        except:
                pass

#Search for movies by year selected
def YEARFIND(url):
        EnableMeta = local.getSetting('Enable-Meta')
        pages=re.compile('found&nbsp;&nbsp;&nbsp;&nbsp;(.+?)/(.+?)&nbsp;Page').findall(net.http_GET(url).content)
        match=re.compile('<h1><a href="(.+?)" target="_blank">\n\t\t\t\t\t  (.+?) \(([\d]{4})\)\t\t\t\t\t  </a></h1>').findall(net.http_GET(url).content)
        nextpage=re.compile('<font color=\'#FF3300\'>.+?</font>&nbsp;<a href=\'(.+?)\' >.+?</a>').findall(net.http_GET(url).content)
        for current,last in pages:
                addDir('[B][COLOR yellow]Page  %s  of  %s[/COLOR][/B]'%(current,last),custurl+url,2,'',None,None)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDir(name,custurl+url,2,'','Movie',year)
                if EnableMeta == 'false':
                        addDir(name,custurl+url,2,'',None,None)
        if nextpage:
                print nextpage
                url = str(nextpage)
                print url
                url = url.replace('[u\'','')
                url = url.replace(']','')
                url = url.replace('\'','')
                url = '/'+url
                print url
                if EnableMeta == 'true':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',custurl+url,12,'',None,None)
                if EnableMeta == 'false':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',custurl+url+url,12,'',None,None)
                        
#A-Z list
def AZ(url):
        match=re.compile('<li><a href="(.+?)" title=".+? Movies">(.+?)</a></li>').findall(net.http_GET(url).content)
        for url,name in match:
                ok = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
                A = ['A']
                if name in ok:
                        icon = os.path.join(art,name+'.png')
                        addDir(name,url,1,icon,None,None)

#Genres list
def GENRES(url):
        match=re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a></li>').findall(net.http_GET(url).content)
        for url,name in match:
                nono = ['Top Rated', 'Popular Today', 'Most Popular', 'Latest HD', 'TV Shows', 'Featured', 'Home', 'New Releases', 'Latest Added', 'Featured Movies', 'Latest HD Movies', 'Most Viewed', 'Most Viewed', 'Most Voted', 'Genres', 'Submit Links']
                yes = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Magical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
                if name in yes:
                        addDir(name,url,1,'',None,None)

#Search for Movies
def SEARCH(url):
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search Movie25')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                encode = encode.replace('%20', '+')
                print encode
                url = custurl1+'search.php?key='+encode+'&submit='
                print url
                match=re.compile('<div class="movie_about">\n\t\t\t\t<h1><a href="(.+?)" target="_self" title="(.+?)\(([\d]{4})\)">').findall(net.http_GET(url).content)
                for url,name,year in match:
                        name = silent.CLEAN(name)
                        if EnableMeta == 'true':
                               addDir(name,url,2,'','Movie',year)
                        if EnableMeta == 'false':
                               addDir(name,url,2,'',None,None)

def INDEX(url):
        EnableMeta = local.getSetting('Enable-Meta')
        pages=re.compile('found&nbsp;&nbsp;&nbsp;&nbsp;(.+?)/(.+?)&nbsp;Page').findall(net.http_GET(url).content)
        match=re.compile('<div class="movie_about">\n\t\t\t\t<h1><a href="(.+?)" target="_self" title="Watch (.+?)\(([\d]{4})\) Online Free">',re.DOTALL).findall(net.http_GET(url).content)
        nextpage=re.compile('<font color=\'#FF3300\'>.+?</font>&nbsp;<a href=\'(.+?)\' >.+?</a>').findall(net.http_GET(url).content)
        for current,last in pages:
                addDir('[B][COLOR yellow]Page  %s  of  %s[/COLOR][/B]'%(current,last),custurl+url,2,'',None,None)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDir(name,url,2,'','Movie',year)
                if EnableMeta == 'false':
                        addDir(name,url,2,'',None,None)

        if nextpage:
                print nextpage
                url = str(nextpage)
                print url
                url = url.replace('[u\'','')
                url = url.replace(']','')
                url = url.replace('\'','')
                print url
                if EnableMeta == 'true':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',custurl+url,1,'',None,None)
                if EnableMeta == 'false':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',custurl+url,1,'',None,None)

#Regex for TOP9
def TOP9(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<div class=pic_top_movie><a href="(.+?)" title=".+?"><img src=".+?" alt="(.+?)\(([\d]{4})\)"',re.DOTALL).findall(net.http_GET(url).content)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDir(name,url,2,'','Movie',year)
                if EnableMeta == 'false':
                        addDir(name,url,2,'',None,None)

#First page with Hosters
def VIDEOLINKS(name,url,year):
        EnableMeta = local.getSetting('Enable-Meta')
        iconimage = ''
        name2 = name
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETA(name2,year)
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match2=re.compile('<h1 >Links - Quality\n\t\t  (.+?)\t\t</h1>').findall(net.http_GET(url).content)
        match=re.compile('<li id="link_name">\n\t\t\t\t  (.+?)\t\t\t\t</li>\n\t\t\t\t\t\t\t\t<li id="playing_button"><a href="(.+?)"').findall(net.http_GET(url).content)
        if match2:
                quality = str(match2).replace('[','').replace(']','').replace("'",'').replace(' ','').replace('u','')
        else:
                quality = 'Not Specified'
        List=[]; ListU=[]; c=0
        for name,url in match:
                url = url+'@'+name2
                c=c+1; List.append(str(c)+'.)  '+name); ListU.append(url)
        dialog=xbmcgui.Dialog()
        rNo=dialog.select('Select A Host........Quality = %s'%quality, List)
        if rNo>=0:
                rName=List[rNo]
                rURL=ListU[rNo]
                VIDEOLINKS2(rName,rURL,year)
        else:
                pass
                
#Get the Final Hoster link
def VIDEOLINKS2(name,url,year):
        EnableMeta = local.getSetting('Enable-Meta')
        name2 = url.split('@')[1]
        url = url.split('@')[0]
        iconimage = ''
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETA(name2,year)
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match=re.compile('type="button" onclick="location.href=\'(.+?)\'"').findall(net.http_GET(url).content)
        for url in match:
                nono = [custurl1+'watch/']
                if url not in nono:
                        STREAM(name,url+'@'+name2,img)

#Pass url to urlresolver
def STREAM(name,url,img):
        download_enabled = local.getSetting('movies25-download')
        name2 = url.split('@')[1]
        url2 = url.split('@')[0]
        print url2
        try:
                req = urllib2.Request(url2)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                addLink(name2,streamlink,img)
        except:
                silent.Notify('small','Sorry Link Removed:', 'Please try another one.',9000)
                

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        download_enabled = local.getSetting('movies25-download')
        print url
        ok=True
        try: addon.resolve_url(streamlink)
        except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        ###Download Context Menu
        contextMenuItems = []
        if download_enabled == 'true':
                contextMenuItems = []
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=9&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
                ########################
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,types,year):
        EnableFanArt = local.getSetting('Enable-Fanart')
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETA(name,year)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library and Favorites Context Menu
        contextMenuItems = []
        if mode == 2:
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                
                contextMenuItems.append(('Add to Library', 'XBMC.RunPlugin(%s?mode=10&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
        
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))

                contextMenuItems.append(('Add to Kid Movies', 'XBMC.RunPlugin(%s?mode=47&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ##############################
        ##############################
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        if mode == 20000:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addFAVDir(name,url,year):
        EnableFanArt = local.getSetting('Enable-Fanart')
        mode = 2
        types = 'Movie'
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETA(name,year)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library Context Menu
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        contextMenuItems.append(('Remove from Favorites', 'XBMC.RunPlugin(%s?mode=15&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
        
        contextMenuItems.append(('Remove from Kids Movies', 'XBMC.RunPlugin(%s?mode=48&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ##############################
        if mode == 20000:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

    
params=get_params()
url=None
name=None
mode=None
year=None
types=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        year=urllib.unquote_plus(params["year"])
except:
        pass
try:
        types=urllib.unquote_plus(params["types"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print ""
        URLCHECK()
        
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        VIDEOLINKS(name,url,year)

elif mode==3:
        print ""+url
        VIDEOLINKS2(name,url,year)

elif mode==4:
        print ""+url
        STREAM(name,url)

elif mode==5:
        print ""+url
        AZ(url)

elif mode==6:
        print ""+url
        SEARCH(url)

elif mode==7:
        print ""+url
        GETMYFAVS()

elif mode==8:
        print ""+url
        GENRES(url)

elif mode==9:
        print ""+url
        silent.DOWNLOAD(name,url)

elif mode==10:
        print ""+url
        silent.AddToLibrary(name,url)

elif mode==11:
        print ""+url
        silent.LIBRARYPLAY(name,url)

elif mode==12:
        print ""+url
        YEARFIND(url)

elif mode==13:
        print ""+url
        YEAR()

elif mode==14:
        print ""+url
        silent.addFavorite(name,url,year)

elif mode==15:
        print ""+url
        silent.removeFavorite(name,url,year)

elif mode==16:
        print ""+url
        MOVIES()

elif mode==17:
        print ""+url
        TV()

elif mode==18:
        print ""+url
        SETTINGS()

elif mode==21:
        POPULAR()

elif mode==22:
        print ""+url
        INDEXTV(url)

elif mode==23:
        print ""+url
        VIDEOLINKSTV(url)

elif mode==24:
        print ""+url
        VIDEOLINKS2TV(name,url)

elif mode==25:
        print ""+url
        STREAMTV(name,url)

elif mode==26:
        print ""+url
        INDEX2(url)

elif mode==27:
        print ""+url
        INDEX3(url)

elif mode==28:
        print ""+url
        INDEX4(url)

elif mode==29:
        print ""+url
        INDEX5(url)

elif mode==30:
        print ""+url
        INDEX6(url)

elif mode==31:
        print ""+url
        SEASONS(name,url)

elif mode==32:
        print ""+url
        EPISODES(name,url)

elif mode==33:
        print ""+url
        AZTV(url)

elif mode==34:
        print ""+url
        LIST(url)

elif mode==35:
        print ""+url
        GENRESTV(url)

elif mode==36:
        print ""+url
        NEWLINKS(url)

elif mode==37:
        print ""+url
        SEARCHTV(url)

elif mode==38:
        print ""+url
        SCHEDULE(url)

elif mode==39:
        print ""+url
        GETMYFAVSTV()

elif mode==40:
        print ""+url
        silent.addFavoriteTV(name,url,types)

elif mode==41:
        print ""+url
        silent.removeFavoriteTV(name,url,types)

elif mode==42:	addon.addon.openSettings()

elif mode==43:
        ResolverSettings()

elif mode==44:
        KIDMOVIES()

elif mode==45:
        KIDTV()

elif mode==46:
        PARENTS()

elif mode==47:
        print ""+url
        silent.addFavoriteKIDMOVIE(name,url,year)

elif mode==48:
        print ""+url
        silent.removeFavoriteKIDMOVIE(name,url,year)

elif mode==49:
        print ""+url
        silent.addFavoriteKIDTV(name,url,types)

elif mode==50:
        print ""+url
        silent.removeFavoriteKIDTV(name,url,types)

elif mode==51:
        print ""+url
        TOP9(url)
        
elif mode==52:
        print ""+url
        NEWLINKS2(url,name)

elif mode==53:
        print ""+url
        MYWATCHLIST(url)

elif mode==54:
        print ""+url
        REMOVETRACKED(name,url)

elif mode==55:
        print ""+url
        MYWATCHLIST2(name,url)

elif mode==56:
        print ""+url
        ADDTRACKED(name,url)

elif mode==57:
        print ""+url
        MYTRACKED(url)

elif mode==58:
        print ""+url
        MYTRACKED2(name,url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
