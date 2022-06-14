# Module: main
# Author: Sam Greaves
# Created on: 15.03.2022
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Video addon that is compatible with Kodi 19.x "Matrix" and above
"""
from __future__ import unicode_literals

import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import requests

import os
from base64 import b64encode, b64decode
from binascii import a2b_hex
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Cryptodome.Cipher import DES
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import unpad
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

base_url = "https://rocktalk.net/tv/index.php"  # 31.220.0.210 31.220.0.8
user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
player_user_agent = "mediaPlayerhttp/2.5 (Linux;Android 5.1) ExoPlayerLib/2.6.1"
s = requests.Session()
s.headers.update({"User-Agent": "USER-AGENT-tvtap-APP-V2"})

def payload():
    _pubkey = RSA.importKey(
        a2b_hex(
            "30819f300d06092a864886f70d010101050003818d003081890281"
            "8100bfa5514aa0550688ffde568fd95ac9130fcdd8825bdecc46f1"
            "8f6c6b440c3685cc52ca03111509e262dba482d80e977a938493ae"
            "aa716818efe41b84e71a0d84cc64ad902e46dbea2ec61071958826"
            "4093e20afc589685c08f2d2ae70310b92c04f9b4c27d79c8b5dbb9"
            "bd8f2003ab6a251d25f40df08b1c1588a4380a1ce8030203010001"
        )
    )
    _msg = a2b_hex(
        "7b224d4435223a22695757786f45684237686167747948392b58563052513d3d5c6e222c22534"
        "84131223a2242577761737941713841327678435c2f5450594a74434a4a544a66593d5c6e227d"
    )
    cipher = Cipher_PKCS1_v1_5.new(_pubkey)
    return b64encode(cipher.encrypt(_msg))

def api_request(case, channel_id=None):
    headers = {"app-token": "37a6259cc0c1dae299a7866489dff0bd"}
    data = {"payload": payload(), "username": "603803577"}
    if channel_id:
        data["channel_id"] = channel_id
    params = {"case": case}
    r = s.post(base_url, headers=headers, params=params, data=data, timeout=5, verify = False)
    r.raise_for_status()
    resp = r.json()
    if resp["success"] == 1:
        return resp["msg"]
    else:
        raise ValueError(resp["msg"])

def update_channels():
    _channels = api_request("get_all_channels")["channels"]
    _channels_list = []
#     _categories = []
    for c in _channels:
        if c['country'] == "US" or c['country'] == "UK":
            _channels_list.append({
                'id' : c.get("pk_id"),
                'name': c.get("channel_name"),
                'thumb': "https://rocktalk.net/tv/" + c.get("img"),
                'video': get_channel_links(c.get("pk_id"))[0],
                'genre': c.get("cat_name")
            })
    return _channels_list
#         if c.get("cat_id") not in _category_list:
#             _category_list.append(c.get("cat_id"))
#             _categories.append({"cat_id": c.get("cat_id"), "cat_name": c.get("cat_name")})

def get_channel_links(pk_id):
    _channel = api_request("get_channel_link_with_token_latest", pk_id)["channel"][0]
    links = []
    for stream in _channel.keys():
        if "stream" in stream or "chrome_cast" in stream:
            _crypt_link = _channel[stream]
            if _crypt_link:
                d = DES.new(b"98221122", DES.MODE_ECB)
                link = unpad(d.decrypt(b64decode(_crypt_link)), 8).decode("utf-8")
                if not link == "dummytext" and link not in links:
                    links.append(link)
                    print(link)
    return links

CHANNELS = []

CHANNELS2 = [
    {
        'name': 'BBC One North East (540p)',
        'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/BBC_One_logo_%28box_variant%29.svg/2560px-BBC_One_logo_%28box_variant%29.svg.png',
        'video': 'https://vs-hls-pushb-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_one_north_east/mobile_wifi_main_sd_abr_v2_akamai_hls_live_http.m3u8',
        'genre': 'Entertainment'
    },
    {
        'name': '1HD Music Television (1080p) [Not 24/7]',
        'thumb': 'https://freestreamstv.live/upload/source/1HD%20Music%20Channel.png',
        'video': 'http://1hdru-hls-otcnet.cdnvideo.ru/onehdmusic/tracks-v1a1/index.m3u8',
        'genre': 'Music'
    },
    {
        'name': 'Greatest Hits',
        'thumb': 'https://provider-static.plex.tv/epg/cms/staging/73c31029-967e-496f-a175-4e49112b4da1/stingray-greatest-hits_logo_dark.png',
        'video': 'https://stream.ads.ottera.tv/playlist.m3u8?network_id=1385&livestream=1&live=1&app_bundle=com.plexapp.android&did=62274240-07e7-5d94-8dc8-ef68cf19e175&app_domain=app.plex.tv&app_name=plex&h=&w=&custom4=plex&gdpr=0&device_make=&device_model=&coppa=1&us_privacy=1---&custom_6=eHK8K_69v6Dss5oCUAbz&custom_7=61aa97d4113e1e5137fd5325',
        'genre': 'Music'
    },
    {
        'name': 'AMC Presents (1080p)',
        'thumb': 'https://i.imgur.com/yngqRL8.png',
        'video': 'https://amc-amcpresents-1.imdbtv.wurl.com/manifest/playlist.m3u8',
        'genre': 'Entertainment'
    },
    {
        'name': 'Hunt Channel (1080p)',
        'thumb': 'https://i.imgur.com/DkvWWbE.png',
        'video': 'https://1111296894.rsc.cdn77.org/LS-ATL-56868-1/index.m3u8',
        'genre': 'Sport'
    },
    {
        'name': 'IDG (720p)',
        'thumb': 'https://i.imgur.com/M0omWCW.jpg',
        'video': 'https://a.jsrdn.com/broadcast/529a360c04/+0000/c.m3u8',
        'genre': 'News'
    },
    {
        'name': 'Hard Knocks',
        'thumb': 'https://provider-static.plex.tv/epg/images/ott_channels/logos/hardknocks_logo_dark.png',
        'video': 'https://d3uyzhwvmemdyf.cloudfront.net/v1/master/9d062541f2ff39b5c0f48b743c6411d25f62fc25/HardKnocks-PLEX/121.m3u8?ads.plex_token=eHK8K_69v6Dss5oCUAbz&ads.channel_id=5fd115bdb7ef8d002dcf1820&ads.device_id=62274240-07e7-5d94-8dc8-ef68cf19e175&ads.dnt=0',
        'genre': 'Sport'
    }
]

# r =requests.get('http://samgreaves.com:3020/videos/kodi')
# VIDEOS = r.json()
VIDEOS = []
VIDEOS.append({
    'name': 'Movies',
    'thumb': '',
    'icon': 'fanart',
    'videos': []
})

VIDEOS.append({
    'name': 'TV Shows',
    'thumb': '',
    'icon': 'fanart',
    'shows' : []
})

VIDEOS.append({
    'name': 'Live TV',
    'thumb': '',
    'icon': 'fanart',
    'channels' : []
})

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def list_videos():
    xbmcplugin.setPluginCategory(_handle, 'Movies')
    xbmcplugin.setContent(_handle, 'videos')

    r = requests.get('http://samgreaves.com:3020/videos/kodi/Movies')

    movies = r.json()

    for video in movies:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['name'],
                                    'mediatype': 'video'})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)

def list_channels():
    xbmcplugin.setPluginCategory(_handle, 'Live TV')
    xbmcplugin.setContent(_handle, 'videos')

    channels = update_channels() + CHANNELS2

    for channel in channels:
        list_item = xbmcgui.ListItem(label=channel['name'])
        list_item.setInfo('video', {'title': channel['name'],
                                    'genre': channel['name'],
                                    'mediatype': 'video'})
        list_item.setArt({'thumb': channel['thumb'], 'icon': channel['thumb'], 'fanart': channel['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=channel['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_shows():
    xbmcplugin.setPluginCategory(_handle, 'TV Shows')
    xbmcplugin.setContent(_handle, 'videos')

    r = requests.get('http://samgreaves.com:3020/videos/kodi/TV Shows')
    shows = r.json()

    for show in shows:
         list_item = xbmcgui.ListItem(label=show['name'])
         list_item.setArt({'thumb': show['thumb'],
                           'icon': show['thumb'],
                           'fanart': show['thumb']})
         list_item.setInfo('video', {'title': show['name'],
                                     'genre': show['name'],
                                     'mediatype': 'video'})
         url = get_url(action='listing', show=show['name'], showId=show['id'], category='show')
         is_folder = True
         xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_seasons(showName, showId):
    xbmcplugin.setPluginCategory(_handle, showName)
    xbmcplugin.setContent(_handle, 'videos')

    r = requests.get('http://samgreaves.com:3020/videos/kodi/TV Shows/' + showId)
    seasons = r.json()

    for season in seasons:
        list_item = xbmcgui.ListItem(label='Season ' + str(season['name']))
        list_item.setArt({'thumb': season['thumb'],
                          'icon': season['thumb'],
                          'fanart': season['thumb']})
        list_item.setInfo('video', {'title': 'Season ' + str(season['name']),
                                    'genre': 'Season ' + str(season['name']),
                                    'mediatype': 'video'})

        seasonNumber = ""
        for m in str(season['name']):
            if m.isdigit():
                seasonNumber = seasonNumber + m

        url = get_url(action='listing', category='episodes', showName=showName, showId=showId, seasonNumber=seasonNumber)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_episodes(showName, showId, seasonNumber):
    xbmcplugin.setPluginCategory(_handle, showName + '/ Season ' + str(seasonNumber))
    xbmcplugin.setContent(_handle, 'videos')

    r = requests.get('http://samgreaves.com:3020/videos/kodi/TV Shows/' + showId + '/' + seasonNumber)
    season = r.json()

    for episode in season.episodes:
        list_item = xbmcgui.ListItem(label=episode['name'])
        list_item.setArt({'thumb': episode['thumb'],
                          'icon': episode['thumb'],
                          'fanart': episode['thumb']})
        list_item.setInfo('video', {'title': episode['name'],
                                    'genre': episode['name'],
                                    'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=episode['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'Type')
    xbmcplugin.setContent(_handle, 'videos')

    for category in VIDEOS:
        list_item = xbmcgui.ListItem(label=category['name'])
        list_item.setArt({'thumb': category['thumb'],
                          'icon': category['thumb'],
                          'fanart': category['thumb']})
        list_item.setInfo('video', {'title': category['name'],
                                    'genre': category['name'],
                                    'mediatype': 'video'})
        url = get_url(action='listing', category=category['name'])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        elif params['action'] == 'listing' and params['category'] == 'Movies':
            list_videos()
        elif params['action'] == 'listing' and params['category'] == 'TV Shows':
            list_shows()
        elif params['action'] == 'listing' and params['category'] == 'show':
            list_seasons(params['show'], params['showId'])
        elif params['action'] == 'listing' and params['category'] == 'episodes':
            list_episodes(params['showName'], params['showId'], params['seasonNumber'])
        elif params['action'] == 'listing' and params['category'] == 'Live TV':
            list_channels()
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
