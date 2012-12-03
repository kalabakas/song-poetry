import web
import urllib
import urllib2
import json
import re

# Returns a list of songs(playlist).
# The titles of the songs in the row form the initial text (without chars like spaces, commas etc)
def getPlaylist(text):
    tokens = re.split(r"[\s\+*.,!\?]+",text)
    playlist = getSonglist(tokens)
    return playlist

# Returns a list of songs.
# Backward chaining, depth-first.
# LongestMatch.
def getSonglist(tokens=[], minSongSize=1, maxSongSize=5):
    length = len(tokens)
    for j in range(min(length,maxSongSize),minSongSize-1,-1):
        songTitle= " ".join(tokens[0:j])
        song = findSongByTilte(songTitle)
        songlist = []
        if (song):
            subplaylist = getSonglist(tokens[j:],minSongSize, maxSongSize)
            if (len(subplaylist)>0 or j==length):
                songlist.insert(0,song)
                songlist += subplaylist
                return songlist
    return []

# TO DO: Search to other pages if nothing found.
# TO DO: The url of spotify Metadata API doesn t belong here.
# Returns song, the title of which matches the query string.
# Uses the Spotify Metadata API to find songs.
def findSongByTilte(query):
    title_s = query.lower().strip()
    q = 'title:'+ title_s
    params = {'q': q, 'page': 1}
    url = 'http://ws.spotify.com/search/1/track.json?'
    url += urllib.urlencode(params)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    tracks = json.load(response)['tracks']
    #trackresults = []
    for track in tracks:
        if (track['name'].lower().strip() == title_s):
            trackresult = {"uri": track['href'], \
                           "trackname": track['name']}
            return trackresult
            #trackresults.append(trackresult)
    return ''

