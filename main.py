from flask import Flask, redirect, url_for, render_template, request

import sys
import spotipy
import spotipy.util as util

from functions import createObj, playlistIDs, albumIDs, songID, findNums, determineMood

client_id = "blank"
client_secret = "blank"
redirect_uri = "https://www.google.com/"
scope = 'playlist-read-private user-library-read'

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope):
    if request.method == "POST":
        user = request.form["username"]

        searchType = request.form["searchType"]

        return redirect(url_for("search", searchT=searchType, user=user))
    else:
        return render_template("home.html")
    
    #return redirect(url_for("search", searchT=searchType, spotifyObj=obj))


@app.route("/<searchT>/<user>", methods=["POST", "GET"])
def search(searchT, user):

    token = util.prompt_for_user_token(user, scope, client_id, client_secret, redirect_uri)
    spotifyObj = createObj(token)

    if searchT == "playlist":
        if request.method == "POST":
            searchName = request.form["playlist"]
            tracks = playlistIDs(searchName, spotifyObj)
            energy, valence = findNums(tracks, spotifyObj)
            mood = determineMood(energy, valence)

            return redirect(url_for("results", searchT=searchT, searchName=searchName, energy=energy, valence=valence, mood=mood))
        else:
            return render_template("playlistsearch.html")
    elif searchT == "album":
        if request.method == "POST":
            searchName = request.form["album"]
            artist = request.form["artist"]
            tracks = albumIDs(searchName, artist, spotifyObj)
        else:
            return render_template("albumsearch.html")
    elif searchT == "song":
        if request.method == "POST":
            searchName = request.form["song"]
            album = request.form["album"]
            artist = request.form["artist"]
            tracks = songID(searchName, album, artist, spotifyObj)
        else:
            return render_template("songsearch.html")

    # energy, valence = findNums(tracks, spotifyObj)
    # mood = determineMood(energy, valence)

    # return redirect(url_for("results", searchT=searchT, searchName=searchName, energy=energy, valence=valence, mood=mood))
 
@app.route("/<searchT>/<searchName>/<energy>/<valence>/<mood>")
def results(searchT, searchName, energy, valence, mood):
    return render_template("results.html", type=searchT, name=searchName, energy=energy, valence=valence, mood=mood)



if __name__ == "__main__":
    app.run()
