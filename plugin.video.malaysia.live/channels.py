import time
import simplejson
from channel import BaseChannel, ChannelException,ChannelMetaClass, STATUS_BAD, STATUS_GOOD, STATUS_UGLY
from utils import *

class TV1(BaseChannel):
    playable = True
    short_name = 'tv1'
    long_name = 'RTM TV1'
    default_action = 'play_stream' 

    def action_play_stream(self):
        self.plugin.set_stream_url('http://supercharged.stream.my/live/rtm-ch001.stream_360p/chunklist.m3u8 live=true')

class TV2(BaseChannel):
    playable = True
    short_name = 'tv2'
    long_name = 'RTM TV2'
    default_action = 'play_stream' 

    def action_play_stream(self):
        self.plugin.set_stream_url('http://supercharged.stream.my/live/rtm-ch003.stream_360p/chunklist.m3u8 live=true')
        
class TV3(BaseChannel):
    playable=True
    short_name = 'tv3'
    long_name = "Media Prima TV3"
    default_action = 'play_stream'

    def action_play_stream(self):        
        self.plugin.set_stream_url("http://tv3liveios-i.akamaihd.net/hls/live/205900/ios/tv3live/master.m3u8 live=true")
    
class NTV7(BaseChannel):
    playable = True
    short_name = 'ntv7'
    long_name = 'Media Prima TV7'
    default_action = 'play_stream'
    
    def action_play_stream(self):
	self.plugin.set_stream_url("http://ntv7liveios-i.akamaihd.net/hls/live/205902/ios/ntv7live/master.m3u8 live=true")
	
class 8TV(BaseChannel):
    playable = True
    short_name = '8tv'
    long_name = 'Media Prima TV8'
    default_action = 'play_stream'
    
    def action_play_stream(self):
	self.plugin.set_stream_url("http://8tvliveios-i.akamaihd.net/hls/live/205901/ios/8tvlive/master.m3u8")
	
class TV9(BaseChannel):
    playable=True
    short_name = 'tv9'
    long_name = "Media Prima TV9"
    default_action = 'play_stream'

    def action_play_stream(self):        
        self.plugin.set_stream_url("http://tv9liveios-i.akamaihd.net/hls/live/205903/ios/tv9live/master.m3u8 live=true")
        
class ALHIJRAH(BaseChannel):
    playable=True
    short_name = 'alhijrah'
    long_name = "Al Hijrah Media Corporation"
    default_action = 'play_stream'

    def action_play_stream(self):        
        self.plugin.set_stream_url("http://stream2.1malaysiaiptv.com:1935/mylive/alhijrah_600k/media_b508239_w1246988830.m3u8")

class Awani(BaseChannel):
    playable=True
    short_name = 'awani'
    long_name = "Astro Awani"
    default_action = 'play_stream'

    def action_play_stream(self):        
        self.plugin.set_stream_url('rtmp://cp160334.live.edgefcs.net:1935/live app=live?ovpfv=1.1 playpath=AstroAwani24x7_2@74937 swfUrl="http://vdata.astroawani.com/flash/VideoPlayer.swf" pageUrl="http://www.layanmovie.com/2013/05/11/astro-awani-live-streaming/" swfVfy=true live=true')
