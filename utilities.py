import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util

def determineMood(energy, valence):
    if valence < .5 and energy >= .5:
        return "angry"
    elif valence >= .5 and energy >= .5:
        return "happy"
    elif valence >= .5 and energy < .5:
        return "chill"
    elif valence < .5 and energy < .5:
        return "sad"

def printResults(query, energy, valence, mood):
    print("<<< " + query + "'s results >>>")
    print("Valence: " + str(valence))
    print("Energy: " + str(energy))
    print("Mood: " + mood)
    print()