import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit
import credentials
import spotipy.oauth2 as oauth2
import spotipy

authManager = SpotifyClientCredentials(client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET, )
sp = spotipy.Spotify(auth_manager=authManager)

def getTracks(trackName):
    results = sp.search(q=trackName, type='track')
    trackUri = results['tracks']['items'][0]['uri']
    return trackUri

def getRecommendations(songTracks):
    recommendations = sp.recommendations(limit=3,seed_tracks=songTracks)['tracks']
    return recommendations


streamlit.title("Music Recommendation System")
trackName1 = streamlit.text_input("Enter a song name:")
trackName2 = streamlit.text_input("Enter the second song name:")
trackName3 = streamlit.text_input("Enter the third song name:")
combineTracks = []
if trackName1:
    tracks1 = getTracks(trackName1)
    combineTracks.append(tracks1)

if trackName2:
    tracks2 = getTracks(trackName2)
    combineTracks.append(tracks2)

if trackName3:
    tracks3 = getTracks(trackName3)
    combineTracks.append(tracks3)


if len(combineTracks) == 3:
    recommendation = getRecommendations(combineTracks)
    streamlit.write("Recommended songs")
    for track in recommendation:
        streamlit.write(track['name'])
        streamlit.image(track['album']['images'][0]['url'])
