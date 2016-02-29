'''
    onedrive XBMC Plugin
    Copyright (C) 2013-2014 ddurdle

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

# cloudservice - required python modules
import sys
import urllib
import cgi
import re
import os

# cloudservice - standard XBMC modules
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs


# global variables
PLUGIN_NAME = 'onedrive'



# cloudservice - helper methods
def log(msg, err=False):
    if err:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg, xbmc.LOGERROR)
    else:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg, xbmc.LOGDEBUG)

# cloudservice - helper methods
def parse_query(query):
    queries = cgi.parse_qs(query)
    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    q['mode'] = q.get('mode', 'main')
    return q

#*** migrate
def addMediaFile(service, package):

    listitem = xbmcgui.ListItem(package.file.title, iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail)

    if package.file.type == package.file.AUDIO:
        infolabels = decode_dict({ 'title' : package.file.title })
        listitem.setInfo('Music', infolabels)
        playbackURL = '?mode=audio'
    elif package.file.type == package.file.VIDEO:
        infolabels = decode_dict({ 'title' : package.file.title , 'plot' : package.file.plot })
        listitem.setInfo('Video', infolabels)
        playbackURL = '?mode=video'
    elif package.file.type == package.file.PICTURE:
        infolabels = decode_dict({ 'title' : package.file.displayTitle() , 'plot' : package.file.plot })
        listitem.setInfo('Pictures', infolabels)
        playbackURL = '?mode=photo'
    else:
        infolabels = decode_dict({ 'title' : package.file.title , 'plot' : package.file.plot })
        listitem.setInfo('Video', infolabels)
        playbackURL = '?mode=video'

    listitem.setProperty('IsPlayable', 'true')
    listitem.setProperty('fanart_image', package.file.fanart)
    cm=[]

    try:
        url = package.getMediaURL()
        cleanURL = re.sub('---', '', url)
        cleanURL = re.sub('&', '---', cleanURL)
    except:
        cleanURL = ''

#    url = PLUGIN_URL+'?mode=streamurl&instance='+service.instanceName+'&title='+package.file.title+'&url='+cleanURL
    url = PLUGIN_URL+playbackURL+'&instance='+service.instanceName+'&title='+package.file.title+'&url='+cleanURL+'&filename='+package.file.id+'&folder='+package.folder.id
    #generate STRM
    cm.append(( addon.getLocalizedString(30042), 'XBMC.RunPlugin('+PLUGIN_URL+'?mode=buildstrm&username='+str(service.authorization.username)+'&title='+package.file.title+'&filename='+package.file.id+')', ))

#    cm.append(( addon.getLocalizedString(30042), 'XBMC.RunPlugin('+PLUGIN_URL+'?mode=buildstrm&title='+package.file.title+'&filename='+package.file.id+')', ))
#    cm.append(( addon.getLocalizedString(30042), 'XBMC.RunPlugin('+PLUGIN_URL+'?mode=buildstrm&title='+package.file.title+'&streamurl='+cleanURL+')', ))
#    cm.append(( addon.getLocalizedString(30046), 'XBMC.PlayMedia('+playbackURL+'&title='+ package.file.title + '&directory='+ package.folder.id + '&filename='+ package.file.id +'&playback=0)', ))
#    cm.append(( addon.getLocalizedString(30047), 'XBMC.PlayMedia('+playbackURL+'&title='+ package.file.title + '&directory='+ package.folder.id + '&filename='+ package.file.id +'&playback=1)', ))
#    cm.append(( addon.getLocalizedString(30048), 'XBMC.PlayMedia('+playbackURL+'&title='+ package.file.title + '&directory='+ package.folder.id + '&filename='+ package.file.id +'&playback=2)', ))
    #cm.append(( addon.getLocalizedString(30032), 'XBMC.RunPlugin('+PLUGIN_URL+'?mode=download&title='+package.file.title+'&filename='+package.file.id+')', ))

#    listitem.addContextMenuItems( commands )
    if cm:
        listitem.addContextMenuItems(cm, False)
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem,
                                isFolder=False, totalItems=0)

    return url

#*** migrate
def addDirectory(service, folder):
    listitem = xbmcgui.ListItem(decode(folder.title), iconImage='', thumbnailImage='')
    fanart = addon.getAddonInfo('path') + '/fanart.jpg'

    if folder.id != '':
        cm=[]
        cm.append(( addon.getLocalizedString(30042), 'XBMC.RunPlugin('+PLUGIN_URL+'?mode=buildstrm&title='+folder.title+'&username='+str(service.authorization.username)+'&folderID='+str(folder.id)+')', ))
        listitem.addContextMenuItems(cm, False)
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(plugin_handle, service.getDirectoryCall(folder), listitem,
                                isFolder=True, totalItems=0)

# cloudservice - helper methods
def addMenu(url,title):
    listitem = xbmcgui.ListItem(decode(title), iconImage='', thumbnailImage='')
    fanart = addon.getAddonInfo('path') + '/fanart.jpg'

    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem,
                                isFolder=True, totalItems=0)

# cloudservice - helper methods
#http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

# cloudservice - helper methods
def decode(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data).strip()

# cloudservice - helper methods
def decode_dict(data):
    for k, v in data.items():
        if type(v) is str or type(v) is unicode:
            data[k] = decode(v)
    return data


# cloudservice - helper methods
def getParameter(key,default=''):
    try:
        value = plugin_queries[key]
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return value
    except:
        return default

# cloudservice - helper methods
def getSetting(key,default=''):
    try:
        value = addon.getSetting(key)
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return value
    except:
        return default

# cloudservice - helper methods
def numberOfAccounts(accountType):

    count = 1
    max_count = int(getSetting(accountType+'_numaccounts',10))

    actualCount = 0
    while True:
        try:
            if getSetting(accountType+str(count)+'_username') != '':
                actualCount = actualCount + 1
        except:
            break
        if count == max_count:
            break
        count = count + 1
    return actualCount



#global variables
PLUGIN_URL = sys.argv[0]
plugin_handle = int(sys.argv[1])
plugin_queries = parse_query(sys.argv[2][1:])

addon = xbmcaddon.Addon(id='plugin.video.onedrive')
#addon = xbmcaddon.Addon(id='plugin.video.onedrive-testing')

addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )



#*** testing - onedrive
from resources.lib import onedrive
from resources.lib import onedrive_api
##**

# cloudservice - standard modules
from resources.lib import cloudservice
from resources.lib import authorization
from resources.lib import folder
from resources.lib import file
from resources.lib import package
from resources.lib import mediaurl
from resources.lib import crashreport
from resources.lib import gPlayer
from resources.lib import settings
from resources.lib import cache
from resources.lib import gSpreadsheets




# cloudservice - standard debugging
try:

    remote_debugger = addon.getSetting('remote_debugger')
    remote_debugger_host = addon.getSetting('remote_debugger_host')

    # append pydev remote debugger
    if remote_debugger == 'true':
        # Make pydev debugger works for auto reload.
        # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
        import pysrc.pydevd as pydevd
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace(remote_debugger_host, stdoutToServer=True, stderrToServer=True)
except ImportError:
    log(addon.getLocalizedString(30016), True)
    sys.exit(1)
except :
    pass


# retrieve settings
user_agent = getSetting('user_agent')
#obsolete, replace, revents audio from streaming
#if user_agent == 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)':
#    addon.setSetting('user_agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.38 Safari/532.0')

# cloudservice - create settings module
settings = settings.settings(addon)

mode = getParameter('mode','main')

# make mode case-insensitive
mode = mode.lower()


log('plugin url: ' + PLUGIN_URL)
log('plugin queries: ' + str(plugin_queries))
log('plugin handle: ' + str(plugin_handle))


instanceName = ''
try:
    instanceName = (plugin_queries['instance']).lower()
except:
    pass


# cloudservice - sorting options
xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_SIZE)


#if mode == 'main':
#    addMenu(PLUGIN_URL+'?mode=options&instance='+instanceName,'<<'+addon.getLocalizedString(30043)+'>>')

#*** onedrive
#if mode != 'main' and instanceName == '':
#    instanceName = 'onedrive1'
##**

# cloudservice - content type
contextType = getParameter('content_type')

    #contentType
    #video context
    # 0 video
    # 1 video and music
    # 2 everything
    #
    #music context
    # 3 music
    # 4 everything
    #
    #photo context
    # 5 photo
    # 6 music and photos
    # 7 everything

try:
      contentType = 0
      contentTypeDecider = int(getSetting('context_video'))

      if contextType == 'video':
        if contentTypeDecider == 2:
            contentType = 2
        elif contentTypeDecider == 1:
            contentType = 1
        else:
            contentType = 0

      elif contextType == 'audio':
        if contentTypeDecider == 1:
            contentType = 4
        else:
            contentType = 3

      elif contextType == 'image':
        if contentTypeDecider == 2:
            contentType = 7
        elif contentTypeDecider == 1:
            contentType = 6
        else:
            contentType = 5

      # show all (for encfs)
      elif contextType == 'all':
            contentType = 8

except:
      contentType = 2


# cloudservice - utilities
#clear the authorization token(s) from the identified instanceName or all instances
if mode == 'clearauth':


    #*** needs to be re-written
    xbmcplugin.endOfDirectory(plugin_handle)


# enroll a new account
elif mode == 'enroll':


        invokedUsername = getParameter('username')
        code = getParameter('code')

        count = 1
        loop = True
        while loop:
            instanceName = PLUGIN_NAME+str(count)
            try:
                username = getSetting(instanceName+'_username')
                if username == invokedUsername or username == "":
                    addon.setSetting(instanceName + '_type', str(1))
                    addon.setSetting(instanceName + '_code', str(code))
                    addon.setSetting(instanceName + '_username', str(invokedUsername))
                    xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30118), invokedUsername)
                    loop = False
            except:
                pass

            if count == numberOfAccounts:
                #fallback on first defined account
                addon.setSetting(instanceName + '_type', str(1))
                addon.setSetting(instanceName + '_code', code)
                addon.setSetting(instanceName + '_username', invokedUsername)
                xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30118), invokedUsername)
                loop = False

            count = count + 1

#create strm files
elif mode == 'buildstrm':

    silent = getParameter('silent', getSetting('strm_silent',0))
    if silent == '':
        silent = 0

    try:
        path = addon.getSetting('strm_path')
    except:
        path = xbmcgui.Dialog().browse(0,addon.getLocalizedString(30026), 'files','',False,False,'')
        addon.setSetting('strm_path', path)

    if path == '':
        path = xbmcgui.Dialog().browse(0,addon.getLocalizedString(30026), 'files','',False,False,'')
        addon.setSetting('strm_path', path)

    if silent == 0 and path != '':
        returnPrompt = xbmcgui.Dialog().yesno(addon.getLocalizedString(30000), addon.getLocalizedString(30027) + '\n'+path +  '?')


    if path != '' and (silent != 0 or returnPrompt):

        if silent != 2:
            try:
                pDialog = xbmcgui.DialogProgressBG()
                pDialog.create(addon.getLocalizedString(30000), 'Building STRMs...')
            except:
                pass

        url = getParameter('streamurl')
        url = re.sub('---', '&', url)
        title = getParameter('title')

        if url != '':

                filename = path + '/' + title+'.strm'
                strmFile = xbmcvfs.File(filename, "w")

                strmFile.write(url+'\n')
                strmFile.close()
        else:

            folderID = getParameter('folder')
            filename = getParameter('filename')
            title = getParameter('title')
            invokedUsername = getParameter('username')

            if folderID != '':

                count = 1
                loop = True
                while loop:
                    instanceName = PLUGIN_NAME+str(count)
                    try:
                        username = getSetting(instanceName+'_username')
                        if username == invokedUsername:

                            #let's log in
                            if ( int(getSetting(instanceName+'_type',0))==0):
                                service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                            else:
                                service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)

                            loop = False
                    except:
                        break

                    if count == numberOfAccounts:
                        try:
                            service
                        except NameError:
                            #fallback on first defined account
                            if ( int(getSetting(instanceName+'_type',0))==0):
                                service = onedrive.onedrive(PLUGIN_URL,addon,PLUGIN_NAME+'1', user_agent, settings)
                            else:
                                service = onedrive_api.onedrive(PLUGIN_URL,addon,PLUGIN_NAME+'1', user_agent, settings)
                        break
                    count = count + 1

                service.buildSTRM(path + '/'+title,folderID, contentType=contentType, pDialog=pDialog)

            elif filename != '':
                            values = {'title': title, 'filename': filename, 'username': invokedUsername}
                            url = PLUGIN_URL+'?mode=video&'+urllib.urlencode(values)
                            filename = path + '/' + title+'.strm'
                            strmFile = xbmcvfs.File(filename, "w")
                            strmFile.write(url+'\n')
                            strmFile.close()

            else:

                count = 1
                while True:
                    instanceName = PLUGIN_NAME+str(count)
                    username = getSetting(instanceName+'_username')

                    if username != '' and username == invokedUsername:
                        if ( int(getSetting(instanceName+'_type',0))==0):
                                service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                        else:
                            service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)

                        service.buildSTRM(path + '/'+username, contentType=contentType, pDialog=pDialog)

                    if count == numberOfAccounts:
                        #fallback on first defined account
                        try:
                            service
                        except NameError:
                            #fallback on first defined account
                            if ( int(getSetting(instanceName+'_type',0))==0):
                                    service = onedrive.onedrive(PLUGIN_URL,addon,PLUGIN_NAME+'1', user_agent, settings)
                            else:
                                service = onedrive_api.onedrive(PLUGIN_URL,addon,PLUGIN_NAME+'1', user_agent, settings)
                        break
                    count = count + 1

        if silent != 2:
            try:
                pDialog.update(100)
                pDialog.close()
            except:
                pass
        if silent == 0:
            xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30028))
    xbmcplugin.endOfDirectory(plugin_handle)

numberOfAccounts = numberOfAccounts(PLUGIN_NAME)

invokedUsername = getParameter('username')

# show list of services
if numberOfAccounts > 1 and instanceName == '' and invokedUsername == '' and mode == 'main':
        mode = ''
        count = 1
        while True:
            instanceName = PLUGIN_NAME+str(count)
            try:
                username = getSetting(instanceName+'_username')
                if username != '':
                    addMenu(PLUGIN_URL+'?mode=main&content_type='+str(contextType)+'&instance='+str(instanceName),username)
            except:
                break
            if count == numberOfAccounts:
                break
            count = count + 1

#        spreadshetModule = getSetting('library', False)
#        libraryAccount = getSetting('library_account')

 #       if spreadshetModule:
 #           addMenu(PLUGIN_URL+'?mode=kiosk&content_type='+str(contextType)+'&instance='+PLUGIN_NAME+str(libraryAccount),'[kiosk mode]')

    # show index of accounts
elif instanceName == '' and invokedUsername == '' and numberOfAccounts == 1:

        count = 1
        options = []
        accounts = []

        for count in range (1, numberOfAccounts+1):
            instanceName = PLUGIN_NAME+str(count)
            try:
                username = getSetting(instanceName+'_username')
                if username != '':
                    options.append(username)
                    accounts.append(instanceName)

                if username != '':

                    #let's log in
                    if ( int(getSetting(instanceName+'_type',0))==0):
                            service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                    else:
                        service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                    break
            except:
                break

        try:
                    service
        except NameError:
                    ret = xbmcgui.Dialog().select(addon.getLocalizedString(30120), options)

                    #fallback on first defined account
                    if ( int(getSetting(instanceName+'_type',0))==0):
                            service = onedrive.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)
                    else:
                        service = onedrive_api.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)


# no accounts defined and url provided; assume public
elif numberOfAccounts == 0 and mode=='streamurl':
    service = onedrivesapi.onedrivesapi(PLUGIN_URL,addon,'', user_agent, authenticate=False)

    # no accounts defined
elif numberOfAccounts == 0:

        #legacy account conversion
        try:
            username = getSetting('username')

            if username != '':
                addon.setSetting(PLUGIN_NAME+'1_username', username)
                addon.setSetting(PLUGIN_NAME+'1_password', getSetting('password'))
                addon.setSetting(PLUGIN_NAME+'1_auth_writely', getSetting('auth_writely'))
                addon.setSetting(PLUGIN_NAME+'1_auth_wise', getSetting('auth_wise'))
                addon.setSetting('username', '')
                addon.setSetting('password', '')
                addon.setSetting('auth_writely', '')
                addon.setSetting('auth_wise', '')
            else:
                xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30015))
                log(addon.getLocalizedString(30015), True)
                xbmcplugin.endOfDirectory(plugin_handle)
        except :
            xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30015))
            log(addon.getLocalizedString(30015), True)
            xbmcplugin.endOfDirectory(plugin_handle)

        #let's log in
        if ( int(getSetting(instanceName+'_type',0))==0):
                service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
        else:
            service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)


    # show entries of a single account (such as folder)
elif instanceName != '':

        #let's log in
        if ( int(getSetting(instanceName+'_type',0))==0):
                service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
        else:
            service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)


elif invokedUsername != '':

        options = []
        accounts = []
        for count in range (1, numberOfAccounts+1):
            instanceName = PLUGIN_NAME+str(count)
            try:
                username = getSetting(instanceName+'_username')
                if username != '':
                    options.append(username)
                    accounts.append(instanceName)

                if username == invokedUsername:

                    #let's log in
                    if ( int(getSetting(instanceName+'_type',0))==0):
                        service = onedrive.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                    else:
                        service = onedrive_api.onedrive(PLUGIN_URL,addon,instanceName, user_agent, settings)
                    break
            except:
                break

        #fallback on first defined account
        try:
                    service
        except NameError:
                    ret = xbmcgui.Dialog().select(addon.getLocalizedString(30120), options)

                    #fallback on first defined account
                    if ( int(getSetting(instanceName+'_type',0))==0):
                        service = onedrive.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)
                    else:
                        service = onedrive_api.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)
#prompt before playback
else:

        options = []
        accounts = []
        for count in range (1, numberOfAccounts+1):
            instanceName = PLUGIN_NAME+str(count)
            try:
                username = getSetting(instanceName+'_username',10)
                if username != '':
                    options.append(username)
                    accounts.append(instanceName)
            except:
                break

        # url provided; provide public option
        if mode=='streamurl':
            options.append('public')
            accounts.append('public')

        ret = xbmcgui.Dialog().select(addon.getLocalizedString(30120), options)

        #fallback on first defined account
        if accounts[ret] == 'public':
            service = onedrive_api.onedrive(PLUGIN_URL,addon,'', user_agent, authenticate=False)
        elif ( int(getSetting(instanceName+'_type',0))==0):
            service = onedrive.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)
        else:
            service = onedrive_api.onedrive(PLUGIN_URL,addon,accounts[ret], user_agent, settings)

# override playback
try:
    if settings.integratedPlayer:
        service.integratedPlayer = True
except: pass



#if mode == 'options' or mode == 'buildstrm' or mode == 'clearauth':
#    addMenu(PLUGIN_URL+'?mode=clearauth','<<'+addon.getLocalizedString(30018)+'>>')
#    addMenu(PLUGIN_URL+'?mode=buildstrm','<<'+addon.getLocalizedString(30025)+'>>')
#    addMenu(PLUGIN_URL+'?mode=folder_enc&instance='+instanceName,'<<encryption>>')



#dump a list of videos available to play
if mode == 'main' or mode == 'folder' or mode == 'index':

    folderName = getParameter('folder', False)

    #** onedrive specific
    if mode == 'main':
        addMenu(PLUGIN_URL+'?mode=search&instance='+instanceName+'&content_type='+str(contextType),'['+addon.getLocalizedString(30111)+']')

        if (service.protocol == 2 and contextType == 'image'):
            addMenu(PLUGIN_URL+'?mode=folder&folder=CAMERA_ROLL&instance='+instanceName+'&content_type='+str(contextType),'['+addon.getLocalizedString(30225)+']')
            addMenu(PLUGIN_URL+'?mode=folder&folder=DOCUMENTS&instance='+instanceName+'&content_type='+str(contextType),'['+addon.getLocalizedString(30226)+']')
            addMenu(PLUGIN_URL+'?mode=folder&folder=PHOTOS&instance='+instanceName+'&content_type='+str(contextType),'['+addon.getLocalizedString(30227)+']')
        elif (service.protocol == 2 and contextType == 'audio'):
            addMenu(PLUGIN_URL+'?mode=folder&folder=MUSIC&instance='+instanceName+'&content_type='+str(contextType),'['+addon.getLocalizedString(30228)+']')

    ##**

#        encfs_target = getSetting('encfs_target')
#        if encfs_target != '':
#                service.addDirectory(None, contextType, localPath=encfs_target)

    # cloudservice - validate service
    try:
        service
    except NameError:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30051), addon.getLocalizedString(30052))
        log(addon.getLocalizedString(30050)+ 'oc-login', True)
        xbmcplugin.endOfDirectory(plugin_handle)


    mediaItems = service.getMediaList(folderName,contentType=contentType)

    if mediaItems:
            for item in mediaItems:

                    if item.file is None:
                        service.addDirectory(item.folder, contextType=contextType)
                    else:
                        service.addMediaFile(item, contextType=contextType)

    service.updateAuthorization(addon)

#*** testing - onedrive
#dump a list of videos available to play
elif mode == 'folder_enc' or mode == 'index_enc':

    folderName=''
    if (mode == 'folder'):
        folderName = plugin_queries['directory']
    else:
        pass

    pathSource = ''
    try:
        pathSource = addon.getSetting('encfs_source')
    except:
        pass

    pathTarget = ''
    try:
        pathTarget = addon.getSetting('encfs_target')
    except:
        pass


    try:
        service
    except NameError:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30051), addon.getLocalizedString(30052))
        log(addon.getLocalizedString(30050)+ 'oc-login', True)
        xbmcplugin.endOfDirectory(plugin_handle)

    mediaItems = service.getMediaList(folderName,0)

    import xbmcvfs

    if mediaItems:
        for item in mediaItems:

            if item.file is None:
#                addDirectory(service, item.folder)
                xbmcvfs.mkdir(pathSource + '/'+item.folder.title)
            else:
                addMediaFile(service, item)

    dirs, files = xbmcvfs.listdir(pathTarget + '/')

    for dir in dirs:
        print xbmcvfs.Stat(pathTarget + '/'+dir).st_ino()


    service.updateAuthorization(addon)

##**


elif mode == 'photo':

    title = getParameter('title',0)
    docid = getParameter('filename')
    folder = getParameter('folder',0)


    path = getSetting('photo_folder')

    if not xbmcvfs.exists(path):
        path = ''

    while path == '':
        path = xbmcgui.Dialog().browse(0,addon.getLocalizedString(30038), 'files','',False,False,'')
        if not xbmcvfs.exists(path):
            path = ''
        else:
            addon.setSetting('photo_folder', path)

    if (not xbmcvfs.exists(str(path) + '/'+str(folder) + '/')):
        xbmcvfs.mkdir(str(path) + '/'+str(folder))
#    try:
#        xbmcvfs.rmdir(str(path) + '/'+str(folder)+'/'+str(title))
#    except:
#        pass

    # don't redownload if present already
    if (not xbmcvfs.exists(str(path) + '/'+str(folder)+'/'+str(title))):
        url = service.getDownloadURL(docid)
        service.downloadPicture(url, str(path) + '/'+str(folder) + '/'+str(title))

    xbmc.executebuiltin("XBMC.ShowPicture("+str(path) + '/'+str(folder) + '/'+str(title)+")")
    item = xbmcgui.ListItem(path=str(path) + '/'+str(folder) + '/'+str(title))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, item)


elif mode == 'slideshow':

    folder = getParameter('folder',0)
    title = getParameter('title',0)

    path = getSetting('photo_folder')

    if not xbmcvfs.exists(path):
        path = ''


    if (not xbmcvfs.exists(str(path) + '/'+str(folder) + '/')):
        xbmcvfs.mkdir(str(path) + '/'+str(folder))

    while path == '':
        path = xbmcgui.Dialog().browse(0,addon.getLocalizedString(30038), 'files','',False,False,'')
        if not xbmcvfs.exists(path):
            path = ''
        else:
            addon.setSetting('photo_folder', path)

    mediaItems = service.getMediaList(folderName=folder, contentType=5)

    xbmc.executebuiltin("XBMC.SlideShow("+str(path) + '/'+str(folder)+"/)")

    if mediaItems:
                for item in mediaItems:
                    if item.file is not None:
                        service.downloadPicture(item.mediaurl.url,str(path) + '/'+str(folder)+ '/'+item.file.title)
                        xbmc.executebuiltin("XBMC.SlideShow("+str(path) + '/'+str(folder)+"/)")


###
# for audio files
###
elif mode == 'audio':

    title = getParameter('title')
    filename = getParameter('filename')
    folderID = getParameter('folder')
    if folderID == 'False':
            folderID = 'SEARCH'

    try:
        service
    except NameError:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30051), addon.getLocalizedString(30052))
        log(addon.getLocalizedString(30050)+ 'gdrive-login', True)
        xbmcplugin.endOfDirectory(plugin_handle)



    playbackMedia = True
    #if we don't have the docid, search for the video for playback
    if (filename != ''):
        mediaFile = file.file(filename, title, '', service.MEDIA_TYPE_MUSIC, '','')
        mediaFolder = folder.folder(folderID,'')
        (mediaURLs,package) = service.getPlaybackCall(package=package.package(mediaFile,mediaFolder))
    else:
        if mode == 'search':

            if title == '':

                try:
                    dialog = xbmcgui.Dialog()
                    title = dialog.input(addon.getLocalizedString(30110), type=xbmcgui.INPUT_ALPHANUM)
                except:
                    xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30100))
                    title = 'test'

            mediaItems = service.getMediaList(title=title, contentType=contentType)
            playbackMedia = False

            options = []
            urls = []

            if mediaItems:
                for item in mediaItems:
                    if item.file is None:
                        service.addDirectory(item.folder, contextType=contextType)
                    else:
                        options.append(item.file.title)
                        urls.append(service.addMediaFile(item, contextType=contextType))

            #search from STRM
            if contextType == '':

                ret = xbmcgui.Dialog().select(addon.getLocalizedString(30112), options)
                playbackURL = urls[ret]

                item = xbmcgui.ListItem(path=playbackURL+'|' + service.getHeadersEncoded())
                # for unknown reasons, for remote music, if Music is tagged as Music, it errors-out when playing back from "Music", doesn't happen when labeled "Video"
                item.setInfo( type="Video", infoLabels={ "Title": options[ret] } )
                if settings.integratedPlayer:
                    player = gPlayer.gPlayer()
                    player.play(playbackURL+'|' + service.getHeadersEncoded(), item)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                else:
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        else:
            (mediaURLs,package) = service.getPlaybackCall(None,title=title)


    if playbackMedia:
        cache = cache.cache(package)
        service.cache = cache

        (localResolutions,localFiles) = service.cache.getFiles()
        if len(localFiles) > 0:
            mediaURL = mediaurl.mediaurl(str(localFiles[0]), 'offline', 0, 0)
        else:
            mediaURL = mediaURLs[0]
            if not settings.download:
                mediaURL.url =  mediaURL.url +'|' + service.getHeadersEncoded()

        playbackPlayer = settings.integratedPlayer

        #download and play
        if settings.download and settings.play:
            service.downloadMediaFile(int(sys.argv[1]), mediaURL, package)
            playbackMedia = False
        ###
        #right-menu context or STRM
        ##
        elif contextType == '':

            #download
            if settings.download and not settings.play:
                service.downloadMediaFile('',mediaURL, package, force=True)
                playbackMedia = False

            # for STRM (force resolve) -- resolve-only
            elif settings.username != '':
                playbackPlayer = False

            else:
                playbackPlayer = True


        # from within pictures mode, music won't be playable, force
        #direct playback from within plugin
        elif contextType == 'image' and settings.cache:
                item = xbmcgui.ListItem(path=str(playbackPath))
                # local, not remote. "Music" is ok
                item.setInfo( type="Music", infoLabels={ "Title": title } )
                player = gPlayer.gPlayer()
                player.play(mediaURL.url, item)
                playbackMedia = False

        # from within pictures mode, music won't be playable, force
        #direct playback from within plugin
        elif contextType == 'image':
            item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail, path=mediaURL.url)
            # for unknown reasons, for remote music, if Music is tagged as Music, it errors-out when playing back from "Music", doesn't happen when labeled "Video"
            item.setInfo( type="Video", infoLabels={ "Title": title } )
            player = gPlayer.gPlayer()
            player.play(mediaURL.url, item)
            playbackMedia = False

        if playbackMedia:
                if playbackPlayer:

                    item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail)#, path=playbackPath+'|' + service.getHeadersEncoded(service.useWRITELY))
                    # for unknown reasons, for remote music, if Music is tagged as Music, it errors-out when playing back from "Music", doesn't happen when labeled "Video"
                    item.setInfo( type="Video", infoLabels={ "Title": package.file.title , "Plot" : package.file.title } )
                    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

                    player = gPlayer.gPlayer()
                    #player.play(playbackPath, item)
                    player.PlayStream(mediaURL.url, item, 0)

                else:

                    item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail, path=mediaURL.url)
                    # for unknown reasons, for remote music, if Music is tagged as Music, it errors-out when playing back from "Music", doesn't happen when labeled "Video"
                    item.setInfo( type="Video", infoLabels={ "Title": package.file.title , "Plot" : package.file.title } )
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


###
# for video files - playback of video
# force stream - play a video given its url
###
#
# legacy (depreicated) - memorycachevideo [given title]
# legacy (depreicated) - play [given title]
# legacy (depreicated) - playvideo [given title]
# legacy (depreicated) - streamvideo [given title]
elif mode == 'video' or mode == 'search' or mode == 'play' or mode == 'memorycachevideo' or mode == 'playvideo' or mode == 'streamvideo':

    title = getParameter('title') #file title
    filename = getParameter('filename') #file ID
    folderID = getParameter('folder') #folder ID

    settings.setVideoParameters()

    seek = 0
    if settings.seek:
        dialog = xbmcgui.Dialog()
        seek = dialog.numeric(2, 'Time to seek to', '00:00')
        for r in re.finditer('(\d+)\:(\d+)' ,seek, re.DOTALL):
            seekHours, seekMins = r.groups()
            seek = int(seekMins) + (int(seekHours)*60)

    try:
        service
    except NameError:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30051), addon.getLocalizedString(30052))
        log(addon.getLocalizedString(30050)+ 'gdrive-login', True)
        xbmcplugin.endOfDirectory(plugin_handle)

    if settings.cache:
            settings.download = False
            settings.play = False


    playbackMedia = True

    # file ID provided
    if (filename != ''):
        mediaFile = file.file(filename, title, '', 0, '','')
        mediaFolder = folder.folder(folderID,'')
        (mediaURLs,package) = service.getPlaybackCall(package=package.package(mediaFile,mediaFolder))
    # search
    elif mode == 'search':

            if title == '':

                try:
                    dialog = xbmcgui.Dialog()
                    title = dialog.input(addon.getLocalizedString(30110), type=xbmcgui.INPUT_ALPHANUM)
                except:
                    xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30100))
                    title = 'test'
            mediaItems = service.getMediaList(title=title, contentType=contentType)
            playbackMedia = False

            options = []
            urls = []

            if mediaItems:
                for item in mediaItems:
                    if item.file is None:
                        service.addDirectory( item.folder, contextType=contextType)
                    else:
                        options.append(item.file.title)
                        urls.append(service.addMediaFile(item, contextType=contextType))

            if contextType == '':

                ret = xbmcgui.Dialog().select(addon.getLocalizedString(30112), options)
                playbackPath = urls[ret]

                item = xbmcgui.ListItem(path=playbackPath+'|' + service.getHeadersEncoded())
                item.setInfo( type="Video", infoLabels={ "Title": options[ret] , "Plot" : options[ret] } )
                if settings.integratedPlayer:
                    player = gPlayer.gPlayer()
                    player.play(playbackPath+'|' + service.getHeadersEncoded(), item)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                else:
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    # folder only
    elif folderID != '' and title == '':
        mediaItems = service.getMediaList(folderName=folderID, contentType=contentType)
        if mediaItems:
            if contextType == '':
                player = gPlayer.gPlayer()
                player.setMedia(mediaItems)
                player.playLgist(service)
                playbackMedia = False
    # title provided
    else:
            (mediaURLs,package) = service.getPlaybackCall(None,title=title)


    originalURL = ''
    if playbackMedia:
        cache = cache.cache(package)
        service.cache = cache
        package.file.thumbnail = cache.setThumbnail(service)

        if settings.srt and service.protocol == 2:
            cache.setSRT(service)


        mediaURL = service.getMediaSelection(mediaURLs, folderID, filename)
        playbackPlayer = settings.integratedPlayer
        #mediaURL.url = mediaURL.url +'|' + service.getHeadersEncoded(service.useWRITELY)

        #download and play
        if settings.download and settings.play:
#            service.downloadMediaFile(int(sys.argv[1]), playbackPath, str(title)+'.'+ str(playbackQuality), folderID, filename, fileSize)
            service.downloadMediaFile(int(sys.argv[1]), mediaURL, package)
            playbackMedia = False

        ###
        #right-menu context OR STRM
        ##
        elif contextType == '':

            # right-click force download only
            if settings.download and not settings.play:
#                service.downloadMediaFile('',playbackPath, str(title)+'.'+ str(playbackQuality), folderID, filename, fileSize, force=True)
                service.downloadMediaFile('',mediaURL, package, force=True)
                playbackMedia = False

            # for STRM (force resolve) -- resolve-only
            elif settings.username != '':
                playbackPlayer = False

            # right-click force cache playback
#            elif settings.cache:
#                playbackPlayer = True
#                playbackMedia = False
#                dirs, files = xbmcvfs.listdir(settings.cachePath + '/'+ str(package.file.id) + '/')
#                for file in files:
#                    if os.path.splitext(file)[1] == '.stream':
#                        playbackPath = settings.cachePath + '/'+ str(package.file.id) + '/' + file
#                        playbackMedia = True


            # right-click play original, srt, caption, seek
            elif settings.playOriginal or settings.srt or settings.cc or settings.seek:
                playbackPlayer = True

            # TESTING
            elif settings.resume:
                playbackPlayer = False

                spreadshetModule = getSetting('library', False)
                spreadshetName = getSetting('library_filename', 'TVShows')

                media = {}
                if spreadshetModule:
                    try:
                        gSpreadsheet = gSpreadsheets.gSpreadsheets(service,addon, user_agent)
                        service.gSpreadsheet = gSpreadsheet
                        spreadsheets = gSpreadsheet.getSpreadsheetList()
                    except:
                        spreadshetModule = False

                    if spreadshetModule:
                      for title in spreadsheets.iterkeys():
                        if title == spreadshetName:
                            worksheets = gSpreadsheet.getSpreadsheetWorksheets(spreadsheets[title])

                            for worksheet in worksheets.iterkeys():
                                if worksheet == 'db':
                                    media = gSpreadsheet.getMedia(worksheets[worksheet], fileID=package.file.id)
                                    item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                                            thumbnailImage=package.file.thumbnail)

                                    item.setInfo( type="Video", infoLabels={ "Title": package.file.title , "Plot" : package.file.title } )
                                    player = gPlayer.gPlayer()
                                    player.setService(service)
                                    player.setWorksheet(worksheets['db'])
                                    if len(media) == 0:
                                        player.PlayStream(mediaURL.url, item, 0, package)
                                    else:
                                        player.PlayStream(mediaURL.url, item,media[0][7],package)
                                    while not player.isExit:
                                        player.saveTime()
                                        xbmc.sleep(5000)
                playbackMedia = False



#                if seek!='' and seek > 0:
#                    player = gPlayer.gPlayer()
#                    player.PlayStream(playbackPath+'|' + service.getHeadersEncoded(service.useWRITELY), item, seek)


        # direct-click (resolve or use setting-default)
#        elif settings.cache:

        #direct-click (resolve or use setting-default)
#        else:


        if playbackMedia:

                if playbackPlayer:

                    item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail)#, path=playbackPath+'|' + service.getHeadersEncoded(service.useWRITELY))

                    item.setInfo( type="Video", infoLabels={ "Title": package.file.title , "Plot" : package.file.title } )
                    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

                    player = gPlayer.gPlayer()
                    #player.play(playbackPath, item)
                    if seek > 0:
                        player.PlayStream(mediaURL.url, item, seek)
                    else:
                        player.PlayStream(mediaURL.url, item, 0)

                    #load any cc or srt
                    if settings.srt and service.protocol == 2:
                        while not (player.isPlaying()):
                            xbmc.sleep(1000)

                        files = cache.getSRT(service)
                        for file in files:
                            player.setSubtitles(file.encode("utf-8"))

                else:

                    item = xbmcgui.ListItem(package.file.displayTitle(), iconImage=package.file.thumbnail,
                                thumbnailImage=package.file.thumbnail, path=mediaURL.url)

                    item.setInfo( type="Video", infoLabels={ "Title": package.file.title , "Plot" : package.file.title } )
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

                    #need a player?
                    if seek > 0 or settings.srt or settings.cc:

                        player = gPlayer.gPlayer()

                        # need to seek?
                        if seek > 0:
                            player.seekTo(seek)

                        # load captions
                        if  settings.srt and service.protocol == 2:
                            while not (player.isPlaying()):
                                xbmc.sleep(1000)

                            files = cache.getSRT(service)
                            for file in files:
                                player.setSubtitles(file.encode("utf-8"))

#                player = gPlayer.gPlayer()
#                player.play(playbackURL+'|' + service.getHeadersEncoded(service.useWRITELY), item)
#                while not (player.isPlaying()):
#                    xbmc.sleep(1)

#                player.seekTime(1000)
#                w = tvWindow.tvWindow("tvWindow.xml",addon.getAddonInfo('path'),"Default")
#                w.setPlayer(player)
#                w.doModal()

#                player.seekTime(1000)
#                w = tvWindow.tvWindow("tvWindow.xml",addon.getAddonInfo('path'),"Default")
#                w.setPlayer(player)
#                w.doModal()

#                xbmc.executebuiltin("XBMC.PlayMedia("+str(playbackPath)+'|' + service.getHeadersEncoded(service.useWRITELY)+")")




###
# for video files
# force stream - play a video given its url
###
elif mode == 'streamurl':

    url = getParameter('url',0)
    title = getParameter('title')


    promptQuality = getSetting('prompt_quality', True)

    mediaURLs = service.getPublicStream(url)
    options = []

    if mediaURLs:
        mediaURLs = sorted(mediaURLs)
        for mediaURL in mediaURLs:
            options.append(mediaURL.qualityDesc)

        if promptQuality:
            ret = xbmcgui.Dialog().select(addon.getLocalizedString(30033), options)
        else:
            ret = 0

        playbackURL = mediaURLs[ret].url

        if (playbackURL == ''):
            xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30020),addon.getLocalizedString(30021))
            xbmc.log(addon.getAddonInfo('name') + ': ' + addon.getLocalizedString(20021), xbmc.LOGERROR)
        else:
            # if invoked in .strm or as a direct-video (don't prompt for quality)
            item = xbmcgui.ListItem(path=playbackURL+ '|' + service.getHeadersEncoded())
            item.setInfo( type="Video", infoLabels={ "Title": mediaURLs[ret].title , "Plot" : mediaURLs[ret].title } )
            if settings.integratedPlayer:
                player = gPlayer.gPlayer()
                player.play(playbackURL+'|' + service.getHeadersEncoded(), item)
            else:
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    else:
            xbmcgui.Dialog().ok(addon.getLocalizedString(30000), addon.getLocalizedString(30020),addon.getLocalizedString(30021))
            xbmc.log(addon.getAddonInfo('name') + ': ' + addon.getLocalizedString(20021), xbmc.LOGERROR)




xbmcplugin.endOfDirectory(plugin_handle)

