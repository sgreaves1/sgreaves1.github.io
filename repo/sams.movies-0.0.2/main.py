# Module: main
# Author: Sam Greaves
# Created on: 15.03.2022
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Video addon that is compatible with Kodi 19.x "Matrix" and above
"""
import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import requests

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

r =requests.get('http://samgreaves.com:3020/videos/kodi')
VIDEOS = r.json()
VIDEOS.append({
    'name': 'Live TV',
    'thumb': '',
    'icon': 'fanart',
    'channels': [
        {
            'name': 'BBC One North East (540p)',
            'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/BBC_One_logo_%28box_variant%29.svg/2560px-BBC_One_logo_%28box_variant%29.svg.png',
            'video': 'https://vs-hls-pushb-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_one_north_east/mobile_wifi_main_sd_abr_v2_akamai_hls_live_http.m3u8',
            'genre': 'Entertainment'
        },
        {
            'name': '1HD Music Television (1080p) [Not 24/7]',
            'thumb': 'data:image/jpeg;base64,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',
            'video': 'http://1hdru-hls-otcnet.cdnvideo.ru/onehdmusic/tracks-v1a1/index.m3u8',
            'genre': 'Music'
        },
        {
            'name': 'AMC Presents (1080p)',
            'thumb': 'https://i.imgur.com/yngqRL8.png',
            'video': 'https://amc-amcpresents-1.imdbtv.wurl.com/manifest/playlist.m3u8',
            'genre': 'Entertainment'
        }
    ]
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

    movies = []
    for x in VIDEOS:
        if x['name'] == 'Movies':
            movies = x['videos']

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

    channels = []
    for x in VIDEOS:
        if x['name'] == 'Live TV':
            channels = x['channels']

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

    shows = []
    for x in VIDEOS:
        if x['name'] == 'TV Shows':
            shows = x['shows']

    for show in shows:
         list_item = xbmcgui.ListItem(label=show['name'])
         list_item.setArt({'thumb': show['thumb'],
                           'icon': show['thumb'],
                           'fanart': show['thumb']})
         list_item.setInfo('video', {'title': show['name'],
                                     'genre': show['name'],
                                     'mediatype': 'video'})
         url = get_url(action='listing', show=show['name'], category='show')
         is_folder = True
         xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_seasons(showName):
    xbmcplugin.setPluginCategory(_handle, showName)
    xbmcplugin.setContent(_handle, 'videos')
    seasons = []
    for category in VIDEOS:
        if category['name'] == 'TV Shows':
            for show in category['shows']:
                if show['name'] == showName:
                    seasons = show['seasons']

    for season in seasons:
        list_item = xbmcgui.ListItem(label='Season ' + str(season['number']))
        list_item.setArt({'thumb': season['thumb'],
                          'icon': season['thumb'],
                          'fanart': season['thumb']})
        list_item.setInfo('video', {'title': 'Season ' + str(season['number']),
                                    'genre': 'Season ' + str(season['number']),
                                    'mediatype': 'video'})

        url = get_url(action='listing', category='episodes', show=showName, season=season['number'])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_episodes(showName, seasonNumber):
    xbmcplugin.setPluginCategory(_handle, showName + '/ Season ' + str(seasonNumber))
    xbmcplugin.setContent(_handle, 'videos')

    episodes = []
    for category in VIDEOS:
        if category['name'] == 'TV Shows':
            for show in category['shows']:
                if show['name'] == showName:
                    for season in show['seasons']:
                        if str(season['number']) == seasonNumber:
                            episodes = season['episodes']

    for episode in episodes:
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
            list_seasons(params['show'])
        elif params['action'] == 'listing' and params['category'] == 'episodes':
            list_episodes(params['show'], params['season'])
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
