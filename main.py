from flask import Flask, redirect, url_for, render_template, request
from functions import createObj, playlistIDs, albumIDs, songID, findNums, determineMood

global client_id = "blank"
global client_secret = "blank"
global redirect_uri = "https://www.google.com/"
global scope = 'playlist-read-private user-library-read'

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user = request.form["username"]
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        obj = createObj(token)
        searchType = request.form["searchType"]
        return redirect(url_for("search", searchT=searchType, spotifyObj=obj))
    else:
        return render_template("home.html")

searchT = ""
@app.route("/<searchT>", methods=["POST", "GET"])
def search(searchT,spotifyObj):
    if searchT == "playlist":
        if request.method == "POST":
            searchName = request.form["playlist"]
        else:
            return render_template("playlistsearch.html")
    elif searchT == "album":
        if request.method == "POST":
            searchName = request.form["album"]
            artist = request.form["artist"]
        else:
            return render_template("albumsearch.html")
    elif searchT == "song":
        if request.method == "POST":
            searchName = request.form["song"]
            album = request.form["album"]
            artist = request.form["artist"]
        else:
            return render_template("songsearch.html")

    

if __name__ == "__main__":
    app.run()
