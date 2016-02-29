'''
    onedrive XBMC Plugin
    Copyright (C) 2013-2015 ddurdle

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
import os
import re
import urllib, urllib2
import cookielib
import unicodedata
import sys

# cloudservice - standard modules
from resources.lib import authorization
from cloudservice import cloudservice
from resources.lib import folder
from resources.lib import file
from resources.lib import package
from resources.lib import mediaurl
from resources.lib import crashreport
from resources.lib import cache


# cloudservice - standard XBMC modules
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs



#
#
#
class onedrive(cloudservice):


    AUDIO = 1
    VIDEO = 2
    PICTURE = 3

    MEDIA_TYPE_MUSIC = 1
    MEDIA_TYPE_VIDEO = 2
    MEDIA_TYPE_PICTURE = 3

    MEDIA_TYPE_FOLDER = 0

    PROTOCOL = 'https://'

    API_URL = PROTOCOL+'api.onedrive.com/v1.0/drive/'

    ##
    # initialize (save addon, instance name, user agent)
    ##
    def __init__(self, PLUGIN_URL, addon, instanceName, user_agent, settings, authenticate=True, gSpreadsheet=None):
        self.PLUGIN_URL = PLUGIN_URL
        self.addon = addon
        self.instanceName = instanceName
        self.integratedPlayer = False
        self.gSpreadsheet = gSpreadsheet
        self.settings = settings
        self.protocol = 2
        self.cache = cache.cache()

        if authenticate == True:
            self.type = int(addon.getSetting(instanceName+'_type'))

        self.crashreport = crashreport.crashreport(self.addon)

        try:
            username = self.addon.getSetting(self.instanceName+'_username')
        except:
            username = ''
        self.authorization = authorization.authorization(username)


        self.cookiejar = cookielib.CookieJar()

        self.user_agent = user_agent


        # load the OAUTH2 tokens or force fetch if not set
        if (authenticate == True and (not self.authorization.loadToken(self.instanceName,addon, 'auth_access_token') or not self.authorization.loadToken(self.instanceName,addon, 'auth_refresh_token'))):
            if self.type ==4 or self.addon.getSetting(self.instanceName+'_code'):
                self.getToken(self.addon.getSetting(self.instanceName+'_code'))
            else:
                xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30018))
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
        #***


    ##
    # get OAUTH2 access and refresh token for provided code
    #   parameters: OAUTH2 code
    #   returns: none
    ##
    def getToken(self,code):

            header = { 'User-Agent' : self.user_agent }

            if (self.type == 2):
                url = addon.getSetting(self.instanceName+'_url')
                values = {
                      'code' : code
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)

            elif (self.type == 3):
                url = 'https://login.live.com/oauth20_token.srf'
                clientID =self.addon.getSetting(self.instanceName+'_client_id')
                clientSecret = self.addon.getSetting(self.instanceName+'_client_secret')
                header = { 'User-Agent' : self.user_agent , 'Content-Type': 'application/x-www-form-urlencoded'}

                req = urllib2.Request(url, 'code='+str(code)+'&client_id='+str(clientID)+'&client_secret='+str(clientSecret)+'&redirect_uri=https://login.live.com/oauth20_desktop.srf&grant_type=authorization_code', header)

            elif (self.type ==1):
                url = 'http://dmdsoftware.net/api/onedrive.php'
                values = {
                      'code' : code
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)

            else:
                url = 'https://script.google.com/macros/s/AKfycbw8fdhaq-WRVJXfOSMK5TZdVnzHvY4u41O1BfW9C8uAghMzNhM/exec'
                values = {
                      'username' : self.authorization.username,
                      'passcode' : self.addon.getSetting(self.instanceName+'_passcode')
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)
                xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30140), self.addon.getLocalizedString(30141))

                # try login
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    if e.code == 403:
                        #login issue
                        xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                        xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    else:
                        xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                        xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return

                response_data = response.read()
                response.close()

                # retrieve code
                code = ''
                for r in re.finditer('code found =\"([^\"]+)\"',
                             response_data, re.DOTALL):
                    code = r.group(1)
                if code != '':
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30143))
                else:
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30144))
                    return

                url = 'https://script.google.com/macros/s/AKfycbwZeRGIvW8lNMinPzbRW7DaUnPVgIpxxqvmzeiIs4cHA4tOs-A/exec'
                values = {
                      'code' : code
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)

            # try login
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403:
                    #login issue
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                else:
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return


            response_data = response.read()
            response.close()

            # retrieve authorization token
            for r in re.finditer('\"access_token\"\s?\:\s?\"([^\"]+)\".+?' +
                             '\"refresh_token\"\s?\:\s?\"([^\"]+)\".+?' ,
                             response_data, re.DOTALL):
                accessToken,refreshToken = r.groups()
                self.authorization.setToken('auth_access_token',accessToken)
                self.authorization.setToken('auth_refresh_token',refreshToken)
                self.updateAuthorization(self.addon)
                xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30142))

            for r in re.finditer('\"error_description\"\s?\:\s?\"([^\"]+)\"',
                             response_data, re.DOTALL):
                errorMessage = r.group(1)
                xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30119), errorMessage)
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(errorMessage), xbmc.LOGERROR)

            return

    def login(self):
        self.refreshToken()

    ##
    # refresh OAUTH2 access given refresh token
    #   parameters: none
    #   returns: none
    ##
    def refreshToken(self):

            header = { 'User-Agent' : self.user_agent }

            if (self.type ==2):
                url = self.addon.getSetting(self.instanceName+'_url')
                values = {
                      'refresh_token' : self.authorization.getToken('auth_refresh_token')
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)

            elif (self.type ==3):
                url = 'https://login.live.com/oauth20_token.srf'
                clientID = self.addon.getSetting(self.instanceName+'_client_id')
                clientSecret = self.addon.getSetting(self.instanceName+'_client_secret')
                header = { 'User-Agent' : self.user_agent , 'Content-Type': 'application/x-www-form-urlencoded'}

                req = urllib2.Request(url, 'client_id='+clientID+'&client_secret='+clientSecret+'&refresh_token='+self.authorization.getToken('auth_refresh_token')+'&redirect_uri=https://login.live.com/oauth20_desktop.srf&grant_type=refresh_token', header)

            elif (self.type ==1):
                url = 'http://dmdsoftware.net/api/onedrive.php'
                values = {
                      'refresh_token' : self.authorization.getToken('auth_refresh_token')
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)

            else:
                url = 'https://script.google.com/macros/s/AKfycbwZeRGIvW8lNMinPzbRW7DaUnPVgIpxxqvmzeiIs4cHA4tOs-A/exec'
                values = {
                      'refresh_token' : self.authorization.getToken('auth_refresh_token')
                      }
                req = urllib2.Request(url, urllib.urlencode(values), header)


            # try login
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403:
                    #login issue
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                else:
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30017), self.addon.getLocalizedString(30222))
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return

            response_data = response.read()
            response.close()

            # retrieve authorization token
            for r in re.finditer('\"access_token\"\s?\:\s?\"([^\"]+)\".+?' ,
                             response_data, re.DOTALL):
                accessToken = r.group(1)
                self.authorization.setToken('auth_access_token',accessToken)
                self.updateAuthorization(self.addon)

            for r in re.finditer('\"error_description\"\s?\:\s?\"([^\"]+)\"',
                             response_data, re.DOTALL):
                errorMessage = r.group(1)
                xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30119), errorMessage)
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(errorMessage), xbmc.LOGERROR)

            return




    ##
    # return the appropriate "headers" for onedrive requests that include 1) user agent, 2) authorization cookie
    #   returns: list containing the header
    ##
    def getHeadersList(self, forceWritely=True, isPOST=False):
        if self.authorization.isToken(self.instanceName,self.addon, 'auth_access_token') and not isPOST:
#            return { 'User-Agent' : self.user_agent, 'Authorization' : 'Bearer ' + self.authorization.getToken('auth_access_token') }
            return { 'Authorization' : 'Bearer ' + self.authorization.getToken('auth_access_token'), 'X-Target-URI': 'https://api.onedrive.com' }
        elif self.authorization.isToken(self.instanceName,self.addon, 'auth_access_token'):
#            return { 'User-Agent' : self.user_agent, 'Authorization' : 'Bearer ' + self.authorization.getToken('auth_access_token') }
            return { "If-Match" : '*', 'Content-Type': 'application/atom+xml', 'Authorization' : 'Bearer ' + self.authorization.getToken('auth_access_token') }
        else:
            return { 'User-Agent' : self.user_agent}



    ##
    # return the appropriate "headers" for onedrive requests that include 1) user agent, 2) authorization cookie
    #   returns: URL-encoded header string
    ##
    def getHeadersEncoded(self, forceWritely=True):
        return urllib.urlencode(self.getHeadersList(forceWritely))

    ##
    # retrieve a list of videos, using playback type stream
    #   parameters: prompt for video quality (optional), cache type (optional)
    #   returns: list of videos
    ##
#    def getMediaList(self, folderName='', title=False, cacheType=CACHE_TYPE_MEMORY):
    def getMediaList(self, folderName='', title=False, contentType=7):


        limiter = '?select=name,webUrl,size,file,folder'
        # show all videos
        if folderName=='VIDEO':
            url = url + "?q=mimeType+contains+'video'"
        # show all music
#        elif folderName=='MUSIC':
#            url = url + "?q=mimeType+contains+'audio'"
        # show all music and video
        elif folderName=='VIDEOMUSIC':
            url = url + "?q=mimeType+contains+'audio'+or+mimeType+contains+'video'"
        # show all photos and music
        elif folderName=='PHOTOMUSIC':
            url = url + "?q=mimeType+contains+'image'+or+mimeType+contains+'music'"
        # show all photos
#        elif folderName=='PHOTO':
#            url = url + "?q=mimeType+contains+'image'"
        # show all music, photos and video
        elif folderName=='ALL':
            url = url + "?q=mimeType+contains+'audio'+or+mimeType+contains+'video'+or+mimeType+contains+'image'"

        #*** onedrive
        # special folder - music
        elif folderName == 'MUSIC':
            url = self.API_URL + 'special/music/children'+limiter
        elif folderName == 'PHOTOS':
            url = self.API_URL + 'special/photos/children'+limiter
        elif folderName == 'DOCUMENTS':
            url = self.API_URL + 'special/documents/children'+limiter
        # special folder - camera roll
        elif folderName == 'CAMERA_ROLL':
            url = self.API_URL + 'special/cameraroll/children'+limiter
        ##**

        # search for title
        elif title != False or folderName == 'SAVED SEARCH':
            encodedTitle = re.sub(' ', '+', title)
            url = self.API_URL + 'root/view.search?'+limiter+'&q=' + str(encodedTitle)



        # show all starred items
        elif folderName == 'STARRED-FILES' or folderName == 'STARRED-FILESFOLDERS' or folderName == 'STARRED-FOLDERS':
            url = url + "?q=starred%3dtrue"
        # show all shared items
        elif folderName == 'SHARED':
            url = url + "?q=sharedWithMe%3dtrue"

        # default / show root folder
        elif folderName == '' or folderName == False or folderName == 'root':
            url = self.API_URL +'root:/:/children'+limiter

        # retrieve folder items
        else:
            url = self.API_URL +'items/'+str(folderName) + '/children'+limiter



        mediaFiles = []
        while True:
            req = urllib2.Request(url, None, self.getHeadersList())

            # if action fails, validate login
            try:
              response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.login()
                req = urllib2.Request(url, None, self.getHeadersList())
                try:
                  response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    if e.code == 403 or e.code == 401:
                        xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), self.addon.getLocalizedString(30223), self.addon.getLocalizedString(30224))
                        xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                        self.crashreport.sendError('getMediaList',str(e))
                        return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                self.crashreport.sendError('getMediaList',str(e))
                return

            response_data = response.read()
            response.close()

            self.crashreport.sendError('mediadata',response_data[:29000], isDebug=True)

            # files
            for r1 in re.finditer('[^\:]+\,?\[?\{([^\}]+\"file\"[^\/]+[^\}]+)\}\}' ,response_data, re.DOTALL):
                entry = r1.group(1)

                media = self.getMediaPackage(entry, folderName=folderName, contentType=contentType)
                if media is not None:
                    mediaFiles.append(media)


            # folders
            for r1 in re.finditer('[^\:]+\,?\[?\{([^\}]+\"folder\"[^\}]+)\}\}' ,response_data, re.DOTALL):
                entry = r1.group(1)

                media = self.getFolderPackage(entry, folderName=folderName)
                if media is not None:
                    mediaFiles.append(media)

            # look for more pages of videos
            nextURL = ''
            for r in re.finditer('\"@odata.nextLink\"\:\s*\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
                nextURL = r.group(1)


            # are there more pages to process?
            if nextURL == '':
                break
            else:
                url = nextURL

        return mediaFiles



    ##
    # retrieve a media package
    #   parameters: given an entry
    #   returns: package (folder,file)
    ##
    def getMediaPackage(self, entry, folderName='',contentType=2):

                resourceID = 0
                resourceType = ''
                title = ''
                fileSize = 0
                url = ''
                for r in re.finditer('\"mimeType\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  resourceType = r.group(1)
                  break
                for r in re.finditer('\"name\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  title = r.group(1)
                  try:
                            title = title.decode('unicode-escape')
                            title = title.encode('utf-8')
                  except:
                            pass
                  break
                for r in re.finditer('\"size\"\:\s*(\d+)' ,
                             entry, re.DOTALL):
                  fileSize = r.group(1)
                  break
                for r in re.finditer('\"@content.downloadUrl\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  url = r.group(1)
                  break
                for r in re.finditer('resid\=([^\"]+)\"' ,
                             entry, re.DOTALL):
                  resourceID = r.group(1)
                  break

                # entry is a video
                if ('video' in resourceType and contentType in (0,1,2,4,7)):
                    thumbnail = 'https://api.onedrive.com/v1.0/drive/items/'+str(resourceID)+'/thumbnails/0/small/content'
#                    thumbnail = self.cache.getThumbnail(self, thumbnail,resourceID)
                    mediaFile = file.file(resourceID, title, title, self.MEDIA_TYPE_VIDEO, '', thumbnail, size=fileSize)

                    media = package.package(mediaFile,folder.folder(folderName,''))
                    media.setMediaURL(mediaurl.mediaurl(url, 'original', 0, 9999))
                    return media

                # entry is a music file
                elif ('audio' in resourceType and contentType in (1,2,3,4,6,7)):
                    thumbnail = 'https://api.onedrive.com/v1.0/drive/items/'+str(resourceID)+'/thumbnails/0/small/content'
#                    thumbnail = self.cache.getThumbnail(self, thumbnail,resourceID)

                    mediaFile = file.file(resourceID, title, title, self.MEDIA_TYPE_MUSIC, '', thumbnail, size=fileSize)
                    media = package.package(mediaFile,folder.folder(folderName,''))
                    media.setMediaURL(mediaurl.mediaurl(url, 'original', 0, 9999))
                    return media

                # entry is a photo
                elif ('image' in resourceType and contentType in (2,4,5,6,7)):
                    thumbnail = 'https://api.onedrive.com/v1.0/drive/items/'+str(resourceID)+'/thumbnails/0/small/content'
#                    thumbnail = self.cache.getThumbnail(self, thumbnail,resourceID)
                    mediaFile = file.file(resourceID, title, title, self.MEDIA_TYPE_PICTURE, '', thumbnail, size=fileSize)

                    media = package.package(mediaFile,folder.folder(folderName,''))
                    media.setMediaURL(mediaurl.mediaurl(url, '','',''))
                    return media

                # entry is unknown
                elif ('application' in resourceType):
                    mediaFile = file.file(resourceID, title, title, self.MEDIA_TYPE_VIDEO, '', '', size=fileSize)

                    media = package.package(mediaFile,folder.folder(folderName,''))
                    media.setMediaURL(mediaurl.mediaurl(url, 'original', 0, 9999))
                    return media

                # all files (for saving to encfs)
                elif (contentType == 8):
                    mediaFile = file.file(resourceID, title, title, self.MEDIA_TYPE_VIDEO, '', '', size=fileSize)

                    media = package.package(mediaFile,folder.folder(folderName,''))
                    media.setMediaURL(mediaurl.mediaurl(url, '','',''))
                    return media

    ##
    # retrieve a media package
    #   parameters: given an entry
    #   returns: package (folder,file)
    ##
    def getFolderPackage(self, entry, folderName=''):

                resourceID = 0
                title = ''
                for r in re.finditer('\"name\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  title = r.group(1)
                  try:
                            title = title.decode('unicode-escape')
                            title = title.encode('utf-8')
                  except:
                            pass
                  break
                for r in re.finditer('resid\=([^\"]+)\"' ,
                             entry, re.DOTALL):
                  resourceID = r.group(1)
                  break

                media = package.package(None,folder.folder(resourceID,title))
                return media



    ##
    # retrieve a playback url
    #   returns: url
    ##
    def getPlaybackCall(self, package):

        url = self.API_URL +'items/'+str(package.file.id)

        req = urllib2.Request(url, None, self.getHeadersList())

        # if action fails, validate login
        try:
              response = urllib2.urlopen(req)
        except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.login()
                req = urllib2.Request(url, None, self.getHeadersList())
                try:
                  response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                  xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                  self.crashreport.sendError('getPlaybackCall',str(e))
                  return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                self.crashreport.sendError('getPlaybackCall',str(e))
                return

        response_data = response.read()
        response.close()

        media = self.getMediaPackage(response_data)
        mediaURLs = []
        mediaURLs.append(mediaurl.mediaurl(media.getMediaURL(), '9999 - original', 0, 9999))

        return (mediaURLs, media)


    ##
    # retrieve a media url
    #   returns: url
    ##
    def getMediaSelection(self, mediaURLs, folderID, filename):
        return mediaURLs[0]



    ##
    # retrieve the download URL for given docid
    #   parameters: resource ID
    #   returns: download URL
    ##
    def getDownloadURL(self, docid):

            url = self.API_URL +'items/'+str(docid)

            req = urllib2.Request(url, None, self.getHeadersList())


            # if action fails, validate login
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403 or e.code == 401:
                    self.login()
                    req = urllib2.Request(url, None, self.getHeadersList())
                    try:
                        response = urllib2.urlopen(req)
                    except urllib2.URLError, e:
                        xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                        self.crashreport.sendError('getDownloadURL',str(e))
                        return
                else:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    self.crashreport.sendError('getDownloadURL',str(e))
                    return

            response_data = response.read()
            response.close()

            media = self.getMediaPackage(response_data)
            return media.getMediaURL()

    ##
    # download remote picture
    # parameters: url of picture, file location with path on disk
    ##
    def downloadPicture(self, url, file):

        req = urllib2.Request(url, None, self.getHeadersList())

        f = xbmcvfs.File(file, 'w')

        # if action fails, validate login
        try:
            f.write(urllib2.urlopen(req).read())
            f.close()

        except urllib2.URLError, e:
              self.login()
              req = urllib2.Request(url, None, self.getHeadersList())
              try:
                f.write(urllib2.urlopen(req).read())
                f.close()
              except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                self.crashreport.sendError('downloadPicture',str(e))
                return


    ##
    # retrieve a srt file for playback
    #   parameters: title of the video file
    #   returns: download url for srt
    ##
    def getSRT(self, title):

        url = ''
        # search for title
        if title != False:
            title = os.path.splitext(title)[0]
            encodedTitle = re.sub(' ', '+', title)
            url = self.API_URL + 'root/view.search?q=' + str(encodedTitle)


        srt = []
        while True:
            req = urllib2.Request(url, None, self.getHeadersList())

            # if action fails, validate login
            try:
              response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.login()
                req = urllib2.Request(url, None, self.getHeadersList())
                try:
                  response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                  xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                  self.crashreport.sendError('getSRT',str(e))
                  return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                self.crashreport.sendError('getSRT',str(e))
                return

            response_data = response.read()
            response.close()


            # files
            for r1 in re.finditer('\{("\@content.*?\"mimeType\":\"[^\"]+\")\}[^\}]*\}' ,response_data, re.DOTALL):
                entry = r1.group(1)

                title = ''
                url = ''
                for r in re.finditer('\"name\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  title = r.group(1)
                  break
                for r in re.finditer('\"@content.downloadUrl\"\:\"([^\"]+)\"' ,
                             entry, re.DOTALL):
                  url = r.group(1)
                  if 'srt' in title:
                      srt.append([title,url])
                  break

            # look for more pages of videos
            nextURL = ''
            for r in re.finditer('\"@odata.nextLink\"\:\s*\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
                nextURL = r.group(1)


            # are there more pages to process?
            if nextURL == '':
                break
            else:
                url = nextURL

        return srt


