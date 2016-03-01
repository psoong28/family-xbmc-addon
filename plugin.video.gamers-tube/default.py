# -*- coding: utf-8 -*-
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#


import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.gamers-tube'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCOpNcN46UbXVtpKMrmU4Abg"
YOUTUBE_CHANNEL_ID_2 = "UCQvWX73GQygcwXOTSf_VDVg"
YOUTUBE_CHANNEL_ID_3 = "UCOyNcdlDkEIQB2HilY7aAoQ"
YOUTUBE_CHANNEL_ID_4 = "UC28ZciCEOs5ruffKqyvrcYA"
YOUTUBE_CHANNEL_ID_5 = "UCOquqcRMJmURiGfEnaitptg"


# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Gamers Channels[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://lh3.googleusercontent.com/-y6LtkCX6VYU/U5Wr4bNPbsI/AAAAAAAAADg/2__GBWuEU2o/w800-h800/gamer+tube.JPG",
        folder=True )
		

    plugintools.add_item( 
        #action="", 
        title="MineCraft",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://pmcdeadline2.files.wordpress.com/2014/02/minecraft__140227211000.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="FIFA 16",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://thisgengaming.com/wp-content/uploads/2015/09/FIFA-16.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Call of Duty Black Ops",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://cdn2-www.playstationlifestyle.net/assets/uploads/gallery/call-of-duty-series/black-ops.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Grand Theft Auto V",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://www.godisageek.com/wp-content/uploads/GTAV-Review.jpg",
        folder=True )
run()
