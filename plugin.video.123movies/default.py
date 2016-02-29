#!/usr/bin/python
HY=int
Hv=str
Hz=False
Hj=len
HI=id
Hu=float
Hs=xrange
Hy=True
Hp=list
HG=eval
HE=None
HL=dict
Hq=repr
HP=range
Qb=file
import xbmc,xbmcplugin
Hc=xbmc.translatePath
Hw=xbmcplugin.endOfDirectory
HD=xbmc.getCondVisibility
Ht=xbmc.PlayList
HW=xbmcplugin.addDirectoryItem
Hd=xbmc.sleep
Hl=xbmcplugin.setContent
Hk=xbmc.Player
HF=xbmc.Keyboard
HS=xbmc.executebuiltin
HN=xbmcplugin.setResolvedUrl
Hr=xbmc.PLAYLIST_VIDEO
Hx=xbmc.executeJSONRPC
import xbmcgui
HR=xbmcgui.ListItem
HM=xbmcgui.Dialog
Hh=xbmcgui.DialogProgress
import sys
HC=sys.argv
import urllib,urllib2
HT=urllib2.Request
He=urllib2.urlopen
Ho=urllib.unquote
HA=urllib.quote_plus
HK=urllib.urlencode
import time
import re,base64
Hi=re.DOTALL
HX=re.compile
Hf=re.sub
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
HV=urlparse.parse_qsl
from os import path,system
import socket
from urllib2 import Request,URLError,urlopen
from urlparse import parse_qs
from urllib import unquote_plus
import xbmcaddon
Hn=xbmcaddon.Addon
import json
HJ=json.dumps
Hg=json.loads
import xbmcvfs
HO=xbmcvfs.File
Hm=xbmcvfs.mkdir
import os
HB=os.path
try:
 from sqlite3 import dbapi2 as database
except:
 from pysqlite2 import dbapi2 as database
pass
b="http://123movies.to"
U=HY(HC[1])
H=Hn()
Q=H.getAddonInfo('path')
a=Q+"/icon.png"
c=Q+"/next.png"
k=Q+"/fanart.jpg"
F=Hh()
d=Hn().getAddonInfo
t=Hm
r=Hc(d('profile')).decode('utf-8')
S=HB.join(r,'favourites.db')
D=HB.join(r,'meta.db')
x="http://123movies.to"
w=x+"/movie/filter"
def Uo(e,referrer=''):
 l=HT(e)
 l.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
 if referrer:
  l.add_header('Referer',referer)
 N=He(l,timeout=5)
 W=N.read()
 N.close()
 return W
def UA(e,T,a,subtitle=''):
 h=T
 R=Hk()
 try:
  M=HR(h,iconImage=a,thumbnailImage=a,path=e)
 except:
  M=HR(h,iconImage=a,thumbnailImage=a)
 if subtitle:
  C=[subtitle]
  M.setSubtitles(C)
 M.setInfo("video",{"Title":h})
 R.play(e,M)
def UK(strTxt):
 print '##################################################################################################'
 print '### GEDEBUG: '+Hv(strTxt)
 print '##################################################################################################'
 return
def UT():
 o=''
 A=HF(o,'Search')
 A.doModal()
 if(A.isConfirmed()==Hz):
  return
 o=A.getText()
 if Hj(o)==0:
  return
 else:
  return o
def Ue():
 K=UT()
 T=K
 try:
  e=x+"/movie/search/"+K.replace(' ','%20')
  ok=UJ('','','','','','','',e)
 except:
  pass
def Uf():
 HQ("Featured",{"name":"Featured","url":x,"mode":1,"section":"movie-featured"},a)
 HQ("Movies",{"name":"Movies","url":x,"mode":4,"section":"movie"},a)
 HQ("TV-Series",{"name":"TV-Series","url":x,"mode":4,"section":"series"},a)
 HQ("Latest Movies",{"name":"Latest Movies","url":x,"mode":1,"section":"mlw-latestmovie"},a)
 HQ("Latest TV-Series",{"name":"Latest TV-Series","url":x,"mode":1,"section":"mlw-featured"},a)
 HQ("Requested",{"name":"Requested","url":x,"mode":1,"section":"mlw-requested"},a)
 HQ("Top Viewed Today",{"name":"Top Viewed Today","url":x,"mode":1,"section":"topview-today"},a)
 HQ("Most Favourite",{"name":"Most Favourite","url":x,"mode":1,"section":"top-favorite"},a)
 HQ("Top Rating",{"name":"Top Rating","url":x,"mode":1,"section":"top-rating"},a)
 HQ("Top IMDb",{"name":"Top IMDb","url":x,"mode":1,'imdb':'topimdb'},a)
 HQ("[COLOR FF00FFFF]My Favourites[/COLOR]",{"name":"My Favourites","url":x,"mode":5},a)
 HQ("[COLOR FF00FFFF]Search[/COLOR]",{"name":"Search","url":x,"mode":99},a)
 Hw(U)
def UX(Ux):
 HQ("Most Viewed",{"name":"Most Viewed","url":x,"mode":1,"section":Ux,"sortby":"view"},a)
 HQ("Most Favourite",{"name":"Most Favourite","url":x,"mode":1,"section":Ux,"sortby":"favorite"},a)
 HQ("Top Rating",{"name":"Top Rating","url":x,"mode":1,"section":Ux,"sortby":"rating"},a)
 HQ("Genre",{"name":"Genre","url":x,"mode":41,"section":Ux,"filters":"genre"},a)
 HQ("Country",{"name":"Country","url":x,"mode":41,"section":Ux,"filters":"country"},a)
 HQ("Year",{"name":"Year","url":x,"mode":41,"section":Ux,"filters":"year"},a)
 Hw(U)
def Ui(Ux,Uh):
 e=w+'/'+Ux
 if Uh=='genre':
  f=UV(e)
 elif Uh=='country':
  f=Un(e)
 elif Uh=='year':
  f=Ug(e)
 for X,h in f:
  h=Hf(r"\s$",'',h)
  HQ(h,{"name":h,"url":x,"mode":1,"section":Ux,"sortby":"all",Uh:X},a)
 if Uh=='year':
  h="Older"
  X="older-2011"
  HQ(h,{"name":h,"url":x,"mode":1,"section":Ux,"sortby":"all",Uh:X},a)
 Hw(U)
def UV(e):
 i=Uo(e)
 V='value="(.+?)".*?name="genres\[\]"\n*\s*.*>(.+?)</label>'
 n=HX(V).findall(i)
 return n
def Un(e):
 i=Uo(e)
 V='value="(.+?)".*?name="countries\[\]"\n*\s*.*>(.+?)</label>'
 n=HX(V).findall(i)
 return n
def Ug(e):
 i=Uo(e)
 V='value="(.+?)".*?name="year"\n*\s*.*>(.+?)</label>'
 n=HX(V).findall(i)
 return n
def UJ(section='all',sortby='latest',genre='all',country='all',year='all',other='all',page='',search='',imdb=''):
 e=w+'/'+section+'/'+sortby+'/'+genre+'/'+country+'/'+year+'/'+other+'/'+page
 search=search.replace('%3a',':').replace('%2f','/')
 if not page:page=1
 if search:
  e=search+'/'+Hv(page)
 if imdb:
  e=b+'/movie/'+imdb+'/'+Hv(page)
 if section=='movie-featured' or section=='mlw-latestmovie' or section=='mlw-featured' or section=='mlw-requested':
  e=x
 if section=='topview-today' or section=='top-favorite' or section=='top-rating':
  e=b+'/site/ajaxContentBox/'+section
 i=Uo(e)
 if section=='movie-featured' or section=='mlw-latestmovie' or section=='mlw-featured' or section=='mlw-requested':
  V='<.*'+section+'.*?\n\s*(.+?)<scrip'
  i=HX(V,Hi).findall(i)[0]
 if section=='topview-today' or section=='top-favorite' or section=='top-rating':
  J=Hg(i)
  i=J['content']
 V='<.*ml-item.*\n*\s*<a href="(.+?)"\n*\s*data-url="(.+?)".*\n*\s*.*\n*\s*title="(.+?)".*\n*\s*(<.).*\n*\s*.*data-original="(.+?)"'
 n=HX(V).findall(i)
 m='files'
 for e,info,h,O,a in n:
  if O=='<s':
   O=3
   m='tvshows'
   B='tv'
   Y='TV Show Information'
  else:
   O=2
   m='movies'
   B='movie'
   Y='Movie Information'
  v=Um(e)
  v['mode']=O
  v['txtinfo']=Y
  v['part']=m
  v['media_type']=B
  v['thumbnail']=a
  z=HY(HC[1])
  try:
   Hl(z,v['part'])
  except:
   Hl(z,'files')
  h=Hf(r'\s\(\d{4}\)','',h)
  j=h+' ('+Hv(v['year'])+')'
  HQ(j,{"name":h,"url":e,"mode":O},a,v)
 I=HY(page)+1
 u=w+'/'+section+'/'+sortby+'/'+genre+'/'+country+'/'+year+'/'+other+'/'+Hv(I)
 if search:
  u=search+'/'+Hv(I)
  HQ("[I]Next Page[/I]",{"name":"Next Page","url":u,"mode":1,"page":I,"search":search},c)
 elif imdb:
  u=b+'/movie/'+imdb+'/'+Hv(I)
  HQ("[I]Next Page[/I]",{"name":"Next Page","url":u,"mode":1,"page":I,"imdb":imdb},c)
 elif section=='movie-featured' or section=='mlw-latestmovie' or section=='mlw-featured' or section=='topview-today' or section=='top-favorite' or section=='top-rating' or section=='mlw-requested':
  pass
 else:
  HQ("[I]Next Page[/I]",{"name":"Next Page","url":u,"mode":1,"section":section,"sortby":sortby,"genre":genre,"country":country,"year":year,"other":other,"page":I,"search":search},c)
 Hw(U)
def Um(e):
 HI=HX('film\/(.+?)\/').findall(e)[0]
 i=Uo(e)
 h=HX('<meta property="og:title" content="(.+?)"/>').findall(i)[0]
 try:
  s=HX('div\sclass="desc">\n\s*(.+?)[\n|<]').findall(i)[0]
 except:s=''
 try:
  y=HX('Release:.*\s(\d{4})</p>').findall(i)[0]
  y=HY(y)
 except:y=''
 try:
  p=HX('background-image:\surl\((.+?)\)').findall(i)[0]
 except:p=''
 try:
  G=HX('<p>\n\s*.*Genre:.*\s\n*\s*(.+?)</p>').findall(i)[0]
  G=HX('">(.+?)</',Hi).findall(G)
  E=' / '.join(G)
 except:E=''
 try:
  L=HX('<p>\n\s*.*Actor:.*\s\n*\s*(.+?)</p>').findall(i)[0]
  L=HX('">(.+?)</',Hi).findall(L)
 except:L=[]
 try:
  q=HX('Director:.*\s\n*\s*.*">(.+?)</a>').findall(i)[0]
 except:q=''
 try:
  P=HX('Country:.*\s\n*\s*.*">(.+?)</a>').findall(i)[0]
 except:P=''
 try:
  bU=HX('Duration:.*\s(\d.+?)\smin</p>').findall(i)[0]
  bU=HY(bU)*60
 except:bU=0
 try:
  bH=HX('Quality:.*\s<.*>(.+?)</.*></p>').findall(i)[0]
 except:bH=''
 try:
  bQ=HX('IMDb:.*\s(.+?)</p>').findall(i)[0]
 except:bQ=''
 try:
  ba=HX('Episode:.*\s(\d{1,2})\seps</').findall(i)[0]
  ba=HY(ba)
 except:ba=''
 W=e
 bc={'link':W,'title':h,'id':HI,'plot':s,'year':y,'fanart':p,'genre':E,'cast':L,'director':q,'country':P,'duration':bU,'quality':bH,'rating':bQ,'episode':ba}
 return bc
def UO(e,T,library='false'):
 e=e+'watching.html'
 i=Uo(e)
 V='<.*movie-id="(.+?)"\n*\s*.*="(.+?)"'
 n=HX(V).findall(i)[0]
 bk=n[0]
 bF=n[1]
 bd='9'
 V='<meta property="og:image" content="(.+?)"/>'
 a=HX(V).findall(i)[0]
 y=HX('Release:.*\s(\d{4})</p>').findall(i)[0]
 F.create('Progress','Please wait while we grab all source.')
 J=[]
 try:
  T=T+' '+y
  i=Uo(b+'/movie/loadepisodes/'+bk)
  V='id="server-(.+?)"'
  n=HX(V).findall(i)
  V='episode-id="(.+?)".*\n.*\n.*\n.*>(.+?)</'
  n=HX(V).findall(i)
  if Hj(n)>1:
   i=0
   l=Hj(n)
   bt=Hv(l)+'.0'
   for br,bH in n:
    Uv(i,l,bt)
    if F.iscanceled():
     F.close()
     break
    i=i+1
    bd=Hv(i)
    if library=='true':
     J.extend(Uu(T,br,bd,a,quality=bH,library='true'))
    else:
     Uu(T,br,bd,a,quality=bH)
  else:
   bd='1'
   br=n[0][1]
   if library=='true':
    J.append(Uu(T,br,bd,a,quality=bH,library='true'))
   else:
    Uu(T,br,bd,a,quality=bH)
 except:
  pass
 F.close()
 if library=='true':
  return J
 else:
  Hw(U)
def UB(e,T):
 e=e+'watching.html'
 i=Uo(e)
 V='<meta property="og:image" content="(.+?)"/>'
 a=HX(V).findall(i)[0]
 V='<.*movie-id="(.+?)"\n*\s*.*="(.+?)"'
 n=HX(V).findall(i)[0]
 bk=n[0]
 bF=n[1]
 bd='9'
 bS=Uz(bk)
 for ba in bS:
  HQ(ba,{"name":ba,"url":e,"mode":31,'mvID':bk,'mvToken':bF,'thumbnail':a,'tvTitle':T},a)
 Hw(U)
def UY(T,bM,UW,bD,thumbnail='',library='false'):
 bk=bM
 bF=UW
 a=thumbnail
 T=Ho(T)
 F.create('Progress','Please wait while we grab all source.')
 try:
  i=Uo(b+'/movie/loadepisodes/'+bk)
  bD=Ho(bD)
  V='Ep.*\s(\d{1,2})|:\s'
  bx=HX(V).findall(bD)[0]
  V='"Ep.*\s('+bx+')\W.*\n\s*.*episode-id="(.+?)"'
  n=HX(V).findall(i)
  J=[]
  if Hj(n)>1:
   i=0
   l=Hj(n)
   bt=Hv(l)+'.0'
   for bd,br in n:
    Uv(i,l,bt)
    if F.iscanceled():
     F.close()
     break
    i=i+1
    bd=Hv(i)
    try:
     if library=='true':
      J.extend(Uu(T,br,bd,a,bD,library='true'))
     else:
      Uu(T,br,bd,a,bD)
    except:pass
  else:
   bd='1'
   br=n[0][1]
   try:
    if library=='true':
     J.extend(Uu(T,br,bd,a,bD,library='true'))
    else:
     Uu(T,br,bd,a,bD)
   except:pass
 except:
  pass
 F.close()
 if library=='true':
  return J
 Hw(U)
def Uv(i,l,bt):
 bw=HY((i/Hu(bt))*100)
 bl="Server found : "+Hv(i)+" out of "+Hv(l)
 F.update(bw,"",bl,"")
 Hd(1000)
def Uz(bk):
 i=Uo(b+'/movie/loadepisodes/'+bk)
 try:
  V='Server\s9\s*..\w*.\s*..\w*.\n\s*.\w*\s\w*="les-content">\n*\s*(.*?)\n*\s*</div>'
  n=HX(V,Hi).findall(i)[0]
 except:
  for x in Hs(1,10):
   try:
    V='Server\s'+Hv(x)+'\s*..\w*.\s*..\w*.\n\s*.\w*\s\w*="les-content">\n*\s*(.*?)\n*\s*</div>'
    n=HX(V,Hi).findall(i)[0]
    break
   except:pass
 V='title="(.*?)"'
 n=HX(V).findall(n)
 return n
def Uj(T,e,episode='false'):
 bN=Ht(Hr)
 bN.clear()
 bW=HN
 bh=HR
 bW(HY(HC[1]),Hy,bh(path=''))
 bR=HS
 bR('Dialog.Close(okdialog)')
 try:
  if episode=='false':
   bH=UO(e,T,'true')
  elif episode=='true':
   bM,UW,bD=e[0],e[1],e[2]
   bH=UY(T,bM,UW,bD,'','true')
  Hp=[]
  W=[]
  bC=[]
  bo=[]
  C=[]
  for J in bH:
   Hp.append(J['label'])
   W.append(J['url'])
   bC.append(J['thumbnail'])
   bo.append(J['vTitle'])
   C.append(J['subtitle'])
  bA=UI(Hp,T)
  if bA==-1:return
  e=W[bA]
  T=bo[bA]
  a=bC[bA]
  bK=C[bA]
  UA(e,T,a,bK)
 except:
  UP('No stream available')
def UI(Hp,heading=d('name')):
 bT=HM()
 return bT.select(heading,Hp)
def Uu(T,br,bd,pic='',epName='',quality='',library='false'):
 e=b+'/movie/load_episode/'+br
 i=Uo(e)
 if epName:
  V='</title>\n*\s*(.+?)\n*\s*</item>'
  i=HX(V,Hi).findall(i)[0]
 else:
  q=quality
  if q=='TS' or q=='CAM':
   quality='  |  '+q
  else:
   quality=''
 V='source.*\n*\s*file="(.+?)"\n*\s*label="(.+?)"'
 n=HX(V).findall(i)
 try:
  V='track.*\n*\s*file="(.+?)"\n*\s*label=".*"'
  bK=HX(V).findall(i)[0]
 except:bK=''
 J=[]
 for e,label in n:
  V='=m(.+)'
  n=HX(V).findall(e)[0]
  if n=='18':label='SD'
  elif n=='22':label='HD'
  elif n=='37':label='1080p'
  else:label='SD'
  h='Server '+bd+'  |  '+label+quality
  T=Ho(Ho(T))
  try:
   be=HX('Season\s(.+?)').findall(T)[0]
   be='S'+Hv(be.zfill(2))
   bf=HX('Ep.*?\s(\d{1,3})|\s|:').findall(epName)[0]
   bf='E'+Hv(bf.zfill(2))
   T=HX('(.+?) -').findall(T)[0]
   T=Ho(T)
   T=T.replace(' ','.')
   T=T+'.'+be+bf
  except:
   T=T.replace(' ','.')
  if library=='true':
   J.append({'url':e,'label':h,'thumbnail':pic,"vTitle":T,'subtitle':bK})
  else:
   HQ(h,{"name":h,"url":e,"mode":69,"thumbnail":pic,"vTitle":T,'subtitle':bK},pic)
 if library=='true':return J
def Us():
 HQ("Favourite Movies",{"name":"Favourite Movies","url":x,"mode":51,'fav_type':'movies'},a)
 HQ("Favourite TV-Series",{"name":"Favourite TV-Series","url":x,"mode":51,'fav_type':'tvshows'},a)
 Hw(U)
def Uy(UM):
 bX=Up(UM)
 J=[i[1]for i in bX]
 for i in J:
  h=i['title']+' ('+Hv(i['year'])+')'
  T=i['title']
  a=i['thumbnail']
  W=i['link']
  O=i['mode']
  bi=i['txtinfo']
  m=i['part']
  B=i['media_type']
  v=Um(W)
  v['mode']=O
  v['txtinfo']=bi
  v['part']=m
  v['media_type']=B
  v['thumbnail']=a
  z=HY(HC[1])
  try:
   Hl(z,v['part'])
  except:
   Hl(z,'files')
  HQ(h,{"name":T,"url":W,"mode":O},a,v)
 Hw(U)
def Up(i,HI=''):
 if HI:
  try:
   bV=database.connect(S)
   bn=bV.cursor()
   bn.execute("SELECT * FROM %s WHERE id = '%s'"%(i,HI))
   bX=bn.fetchall()
  except:bX=[]
 else:
  try:
   bV=database.connect(S)
   bn=bV.cursor()
   bn.execute("SELECT * FROM %s"%(i))
   bX=bn.fetchall()
   bX=[(i[0].encode('utf-8'),HG(i[1].encode('utf-8')))for i in bX]
  except:bh=[]
 return bX
def UG(bc,i,query=HE):
 try:
  bh=HL()
  bc=Hg(bc)
  try:HI=bc['id']
  except:HI=bc['id']
  if 'id' in bc:h=bh['id']=bc['id']
  if 'title' in bc:h=bh['title']=bc['title']
  if 'thumbnail' in bc:thumnbail=bh['thumbnail']=bc['thumbnail']
  if 'year' in bc:bh['year']=bc['year']
  if 'link' in bc:bh['link']=bc['link']
  if 'fanart' in bc:bh['fanart']=bc['fanart']
  if 'mode' in bc:bh['mode']=bc['mode']
  if 'txtinfo' in bc:bh['txtinfo']=bc['txtinfo']
  if 'media_type' in bc:bh['media_type']=bc['media_type']
  if 'part' in bc:bh['part']=bc['part']
  t(r)
  bV=database.connect(S)
  bn=bV.cursor()
  bn.execute('''CREATE TABLE IF NOT EXISTS %s (id TEXT, items TEXT, UNIQUE(id));'''%i)
  bn.execute("DELETE FROM %s WHERE id = '%s'"%(i,HI))
  bn.execute("INSERT INTO %s Values (?, ?)"%i,(HI,Hq(bh)))
  bV.commit()
  if query==HE:UL()
  UP("Added to Favourites",heading=h)
 except:
  return
def UE(bc,i):
 try:
  bc=Hg(bc)
  if 'title' in bc:h=bc['title']
  try:
   bV=database.connect(S)
   bn=bV.cursor()
   try:bn.execute("DELETE FROM %s WHERE id = '%s'"%(i,bc['id']))
   except:pass
   bV.commit()
  except:
   pass
  UL()
  UP('Removed from Favourites',heading=h)
 except:
  return
def UL():
 bR=HS
 return bR('Container.Refresh')
def Uq():
 bJ=Hc(d('path'))
 bm=Hn().getSetting
 bO=bm('appearance').lower()
 if bO in['-','']:return d('icon')
 else:return HB.join(bJ,'resources','media',bO,'icon.png')
def UP(bl,heading=d('name'),icon=Uq(),time=5000):
 bT=HM()
 try:bT.notification(heading,bl,icon,time,sound=Hz)
 except:bR("Notification(%s,%s, %s, %s)"%(heading,bl,time,icon))
def Hb(bc,i):
 bB=HD
 bY='true'
 bv='false'
 bz='true'
 bj=Hx
 bR=HS
 bI=Hz
 bc=Hg(bc)
 T=bc['title']
 h=bc['title']
 y=bc['year']
 if not bB('Window.IsVisible(infodialog)')and not bB('Player.HasVideo'):
  UP('Adding to library...',time=10000000)
  bI=Hy
 try:
  HU(HJ(bc))
 except:
  pass
 if HP==Hy:return
 if bI==Hy:
  UP('Process Complete',time=1)
 if not bB('Library.IsScanningVideo'):
  bR('UpdateLibrary(video)')
def HU(i):
 bs=Hc
 by=HB.join(bs('special://userdata/addon_data/plugin.video.123movies/Movies'),'')
 bp=HB.join(bs('special://userdata/addon_data/plugin.video.123movies/TVShows'),'')
 bG=HO
 i=Hg(i)
 try:
  T=h=i['title']
  e=i['link']
  bC=i['thumbnail']
  y=i['year']
  sysname,systitle=HA(T),HA(h)
  W=e+'watching.html'
  i=Uo(W)
  V='<.*movie-id="(.+?)"\n*\s*.*="(.+?)"'
  n=HX(V).findall(i)[0]
  bk=n[0]
  bF=n[1]
  bd='9'
  if i['part']=='movies':
   bE=by
   bL=Hv(T).translate(HE,'\/:*?"<>|').strip('.')
   bL=bL+' ('+Hv(y)+')'
   i='%s?mode=getQualityMovies&url=%s&vTitle=%s&year=%s&movieID=%s&movieToken=%s&server=%s'%(HC[0],e,systitle,y,bk,bF,bd)
   t(bE)
   bq=HB.join(bE,bL)
   t(bq)
   bP=HB.join(bq,bL+'.strm')
   Qb=bG(bP,'w')
   Qb.write(Hv(i))
   Qb.close()
  elif i['part']=='tvshows':
   bE=bp
   Ub=HX(r'\s-\sSeason\s(\d{1,3})').findall(T)[0]
   T=Hf(r'\s-\sSeason\s\d{1,3}','',T)
   bL=Hv(T).translate(HE,'\/:*?"<>|').strip('.')
   bL=bL+' ('+Hv(y)+')'
   UH='Season %s'%(Ub)
   t(bE)
   bq=HB.join(bE,bL)
   t(bq)
   bq=HB.join(bq,UH)
   t(bq)
   bS=Uz(bk)
   e=1
   for ba in bS:
    i='%s?mode=getQualityTVShows&url=%s&vTitle=%s&year=%s&movieID=%s&movieToken=%s&server=%s&season=%s&episode=%s&epName=%s'%(HC[0],e,systitle,y,bk,bF,bd,Ub,e,ba)
    UQ=bL+' S%sE%s'%(Ub,e)
    bP=HB.join(bq,UQ+'.strm')
    Qb=bG(bP,'w')
    Qb.write(Hv(i))
    Qb.close()
    e=e+1
 except:
  pass
Ua={'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-us,en;q=0.5'}
def HQ(T,parameters={},pic="",meta=''):
 li=HR(T,iconImage=pic,thumbnailImage=pic)
 li.setInfo("video",{"Title":T,"FileName":T})
 if meta:
  try:
   import HTMLParser
   Uc=HTMLParser.HTMLParser()
   meta['plot']=Uc.unescape(meta['plot'])
  except:
   pass
  li.setInfo("video",meta)
  pic=meta['fanart']
  Uk=Up(meta['part'],meta['id'])
  UF=HA(HJ(meta))
  cm=[]
  cm.append((meta['txtinfo'],'Action(Info)'))
  if Uk:
   cm.append(('Delete from Favourites','RunPlugin(%s?mode=delfromFavourite&meta=%s&content=%s)'%(HC[0],UF,meta['part'])))
  else:
   cm.append(('Add to Favourites','RunPlugin(%s?mode=addtoFavourite&meta=%s&content=%s)'%(HC[0],UF,meta['part'])))
  cm.append(('Add to Library','RunPlugin(%s?mode=addtoLibrary&meta=%s&content=%s)'%(HC[0],UF,meta['part'])))
  li.addContextMenuItems(cm,replaceItems=Hy)
 if pic==Q+"/icon.png" or pic==Q+"/next.png":pic=k
 li.setProperty('Fanart_Image',pic)
 e=HC[0]+'?'+HK(parameters)
 return HW(handle=HY(HC[1]),url=e,listitem=li,isFolder=Hy)
def Ha(parameters):
 Ud={}
 if parameters:
  Ut=parameters[1:].split("&")
  for Ur in Ut:
   US=Ur.split('=')
   if(Hj(US))==2:
    Ud[US[0]]=US[1]
 return Ud
UD=Ha(HC[2])
T=Hv(UD.get("name",""))
e=Hv(UD.get("url",""))
e=Ho(e)
O=Hv(UD.get("mode",""))
Ux=Hv(UD.get("section",""))
Uw=Hv(UD.get("sortby","latest"))
E=Hv(UD.get("genre","all"))
P=Hv(UD.get("country","all"))
y=Hv(UD.get("year","all"))
Ul=Hv(UD.get("other","all"))
UN=Hv(UD.get("page",""))
bM=Hv(UD.get("mvID",""))
UW=Hv(UD.get("mvToken",""))
Uh=Hv(UD.get("filters",""))
g=Hv(UD.get("search",""))
bQ=Hv(UD.get("imdb",""))
bC=Hv(UD.get("thumbnail",""))
bC=Ho(bC)
UR=Hv(UD.get("tvTitle",""))
bo=Hv(UD.get("vTitle",""))
UM=Hv(UD.get("fav_type",""))
bK=Hv(UD.get("subtitle",""))
bK=Ho(bK)
if not HC[2]:
 pass
 ok=Uf()
else:
 if O==Hv(1):
  ok=UJ(Ux,Uw,E,P,y,Ul,UN,g,bQ)
 elif O==Hv(2):
  ok=UO(e,T)
 elif O==Hv(3):
  ok=UB(e,T)
 elif O==Hv(31):
  ok=UY(UR,bM,UW,T,bC)
 elif O==Hv(4):
  ok=UX(Ux)
 elif O==Hv(41):
  ok=Ui(Ux,Uh)
 elif O==Hv(99):
  ok=Ue()
 elif O==Hv(69):
  ok=UA(e,bo,bC,bK)
 elif O==Hv(5):
  ok=Us()
 elif O==Hv(51):
  ok=Uy(UM)
 elif O=="addtoFavourite":
  UC=HL(HV(HC[2].replace('?','')))
  bc=UC['meta']
  i=UC['content']
  ok=UG(bc,i)
 elif O=="delfromFavourite":
  UC=HL(HV(HC[2].replace('?','')))
  bc=UC['meta']
  i=UC['content']
  ok=UE(bc,i)
 elif O=="addtoLibrary":
  UC=HL(HV(HC[2].replace('?','')))
  bc=UC['meta']
  i=UC['content']
  ok=Hb(bc,i)
 elif O=="getQualityMovies":
  UC=HL(HV(HC[2].replace('?','')))
  T=UC['vTitle']
  e=UC['url']
  bk=UC['movieID']
  bF=UC['movieToken']
  bd=UC['server']
  ok=Uj(T,e)
 elif O=="getQualityTVShows":
  UC=HL(HV(HC[2].replace('?','')))
  T=UC['vTitle']
  e=UC['url']
  bk=UC['movieID']
  bF=UC['movieToken']
  bd=UC['server']
  Ub=UC['season']
  ba=UC['episode']
  bD=UC['epName']
  J=[bk,bF,bD]
  ok=Uj(T,J,'true')

