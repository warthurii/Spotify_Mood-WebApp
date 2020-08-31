import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
#from json.decoder import JSONDecoderError

#Get username from terminal
username = "safari.will"
client_id = "156004f3993643e9994292b6c8cd86ff"
client_secret = "f4962a3328c849a48cf8cb8f9ede7113"
redirect_uri = "https://www.google.com/"
scope = 'playlist-read-private user-library-read'

#Create our spotifyObject
def createObj(token):
    spotifyObject = spotipy.Spotify(auth=token)

def playlistIDs(searchQuery, spotifyObject):
    searchResults = spotifyObject.search(searchQuery, 1, 0, "playlist")
    playlist = searchResults['playlists']['items'][0]
    playlistID = playlist['id']
    trackIDsJSON = spotifyObject.playlist_tracks(playlistID, offset=0, fields='items.track.id,total', additional_types=['track'])
    trackIDs = []
    for items in trackIDsJSON['items']:
        trackIDs.append(items['track']['id'])
    return trackIDs
def albumIDs(searchQuery, artist, spotifyObject):
    artist = input("Artist Name: ")
    searchResults = spotifyObject.search(q="artist:" + artist + " album:" + searchQuery, type="album")
    albumID = searchResults['albums']['items'][0]['id']
    trackIDsJSON = spotifyObject.album_tracks(albumID)
    trackIDs = []
    for items in trackIDsJSON['items']:
        trackIDs.append(items['id'])  
    return trackIDs 
def songID(searchQuery, album, artist, spotifyObject):
    trackIDs = []
    artist = input("Artist Name: ")
    album = input("Album Name: ")
    searchResults = spotifyObject.search(q="artist:" + artist + " album:" + album + " track:" + searchQuery, limit=1, type="track")
    print(json.dumps(searchResults, sort_keys=True, indent=4))
    track = searchResults['tracks']['items'][0]
    trackID = track['id']
    print(trackID)
    trackIDs.append(trackID)
    return trackIDs

#Finding valence and energy of each track and the playlist total
def findNums(tracks):
    valenceTotal = 0
    energyTotal = 0
    tracksAudio = []
    for track in trackIDs:
        audio = spotifyObject.audio_features(track)
        tracksAudio.append(audio)
        energy = audio[0]['energy']
        valence = audio[0]['valence']
            
        energyTotal += energy
        valenceTotal += valence
        
    #Getting averages
    energyAve = energyTotal / len(trackIDs)
    valenceAve = valenceTotal / len(trackIDs)

    return energyAve, valenceAve

def determineMood(energy, valence):
    if valence < .5 and energy >= .5:
        return "angry"
    elif valence >= .5 and energy >= .5:
        return "happy"
    elif valence >= .5 and energy < .5:
        return "chill"
    elif valence < .5 and energy < .5:
        return "sad"