import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from utilities import determineMood, printResults
#from json.decoder import JSONDecoderError

#Get username from terminal
username = "blank"
client_id = "blank"
client_secret = "blank"
redirect_uri = "https://www.google.com/"
scope = 'playlist-read-private user-library-read'

#Erase cache and prompt for user permission
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
# try:
#     token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
# except:
#     os.remove(f".cache-{username}")
#     token = util.prompt_for_user_token(username)

#Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

displayName = user['display_name']

while True:
    print()
    print(">>> Welcome to Spotipy " + displayName + "!")
    print()
    print("0 - Enter Playlist, Album, or Song")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    #search for playlist
    if choice == "0":
        print()
        cat = input("P for Playlist, A for Album, S for Song: ")
        searchQuery = input("Name: ")
        print()

        #Get search results
        if cat == "P" or cat == "p":
            searchResults = spotifyObject.search(searchQuery, 1, 0, "playlist")
            playlist = searchResults['playlists']['items'][0]
            playlistID = playlist['id']
            trackIDsJSON = spotifyObject.playlist_tracks(playlistID, offset=0, fields='items.track.id,total', additional_types=['track'])
        elif cat == "A" or cat == "a":
            artist = input("Artist Name: ")
            searchResults = spotifyObject.search(q="artist:" + artist + " album:" + searchQuery, type="album")
            albumID = searchResults['albums']['items'][0]['id']
            trackIDsJSON = spotifyObject.album_tracks(albumID)   
        elif cat == "S" or cat == "s":
            trackIDs = []
            artist = input("Artist Name: ")
            album = input("Album Name: ")
            searchResults = spotifyObject.search(q="artist:" + artist + " album:" + album + " track:" + searchQuery, limit=1, type="track")
            print(json.dumps(searchResults, sort_keys=True, indent=4))
            track = searchResults['tracks']['items'][0]
            trackID = track['id']
            print(trackID)
            trackIDs.append(trackID)

        #Storing track ids from json in list for albums and playlists
        if cat == "p" or cat == "P":
            trackIDs = []
            for items in trackIDsJSON['items']:
                trackIDs.append(items['track']['id'])
        elif cat == "A" or cat == "a":
            trackIDs = []
            for items in trackIDsJSON['items']:
                trackIDs.append(items['id'])

        print(trackIDs)

        #Finding valence and energy of each track and the playlist total
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

        mood = determineMood(energyAve, valenceAve)
        
        printResults(searchQuery, energyAve, valenceAve, mood)
        

    #end program    
    if choice == "1":
        break

#print(json.dumps(trackIDsJSON, sort_keys=True, indent=4))