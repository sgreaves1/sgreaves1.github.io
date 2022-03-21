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

DATA = [{
            'name': 'Movies',
            'thumb': '',
            'icon': '',
            'fanart': '',
            'videos': [{
                            'name': "The Adam Project",
                            'thumb': "http://image.tmdb.org/t/p/original/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg",
                            'video': "http://samgreaves.com:3020/videos/tt2463208.mp4",
                            'genre': "Action, Adventure, Comedy"
                       }]
          },
          {
             'name': 'TV Shows',
             'thumb': '',
             'icon': '',
             'fanart': '',
             'shows': [{
                            'name': "Game Of Thrones",
                            'thumb': "http://image.tmdb.org/t/p/original/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg",
                            'genre': "Action, Fantasy",
                            'episodes': [{
                                            'name': '1 - First episode name',
                                            'thumb': "http://image.tmdb.org/t/p/original/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg",
                                            'video': "http://samgreaves.com:3020/videos/tt2463208.mp4",
                                            'genre': "Action, Fantasy"
                            },{
                                            'name': '2 - Second episode name',
                                            'thumb': "http://image.tmdb.org/t/p/original/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg",
                                            'video': "http://samgreaves.com:3020/videos/tt2463208.mp4",
                                            'genre': "Action, Fantasy"
                            }]
                        }]
          }
       ]

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or API.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    for x in DATA:
        if x['name'] == category:
            return x['videos']

    return none

def list_shows():
    xbmcplugin.setPluginCategory(_handle, 'TV Shows')
    xbmcplugin.setContent(_handle, 'videos')

    shows = []
    for x in DATA:
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
         url = get_url(action='listing', category=show['name'])
         is_folder = True
         xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_episodes(showName):
    xbmcplugin.setPluginCategory(_handle, showName)
    xbmcplugin.setContent(_handle, 'videos')

    episodes = []
    for category in DATA:
        if category['name'] == 'TV Shows':
            for show in category['shows']:
                if show['name'] == showName:
                    episodes = show['episodes']


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
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'My Video Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Iterate through categories
    for category in DATA:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['name'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': category['thumb'],
                          'icon': category['thumb'],
                          'fanart': category['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category['name'],
                                    'genre': category['name'],
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category['name'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, category)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
#     xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
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
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'listing' and params['category'] == 'TV Shows':
            list_shows()
        elif params['action'] == 'listing':
            list_episodes(params['category'])
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
