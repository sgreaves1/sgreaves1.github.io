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
            'name': 'Comedy Central East (720p) [Not 24/7]',
            'thumb': 'https://cdn.tvpassport.com/image/station/240x135/comedycentral.png',
            'video': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5d4947590ba40f75dc29c26b/master.m3u8?advertisingId=&appName=web&appStoreUrl=&appVersion=DNT&app_name=&architecture=&buildVersion=&deviceDNT=0&deviceId=5d4947590ba40f75dc29c26b&deviceLat=51.2993&deviceLon=9.4910&deviceMake=web&deviceModel=web&deviceType=web&deviceVersion=DNT&includeExtendedEvents=false&marketingRegion=DE&serverSideAds=false&sid=400&terminate=false&userId=',
            'genre': 'comedy'
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
