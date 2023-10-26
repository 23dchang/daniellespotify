import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request
import pandas as pd


client_id = "6a6c425d0b424157b0003b7ccfc4fab4"
client_secret = "9fe61604885d4cfdb89e4fc4488b1f59"
redirect_uri = "http://127.0.0.1:9090/callback"
scope = "user-top-read"

sp_oauth = SpotifyOAuth(redirect_uri=redirect_uri, client_id=client_id,
                        client_secret=client_secret, scope=scope)
auth_url = sp_oauth.get_authorize_url()
app = Flask(__name__)
@app.route("/")
def hello_world():
    return f'<a href="{auth_url}">login to spotify!</a>'


@app.route('/callback')
def callback():
    tracklist = []
    authorization_code = request.args.get('code')
    if authorization_code:
        # You have obtained the authorization code.
        print("Authorization Code:", authorization_code)
        access_token = sp_oauth.get_access_token(authorization_code)
        print("Access Token:", access_token)
        sp = spotipy.Spotify()
        sp.set_auth(access_token['access_token'])

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                     client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=redirect_uri,
                     scope=scope))

top_tracks_list = sp.current_user_top_tracks(
    limit=10,
    offset=0,
    time_range="medium_term")
top_artists_list = sp.current_user_top_artists(
    limit=10,
    offset=0,
    time_range="short_term"
)

def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids
track_ids = get_track_ids(top_tracks_list)


def get_track_features(id):
    meta = sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    result = sp.search(name)
    track = result['tracks']['items'][0]
    artists = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    track_info = [name, album, artist, artists['genres'][0], ]
    print(track_info)

tracks_list = []
for i in range(len(track_ids)):
    track = get_track_features(track_ids[i])
    tracks_list.append(track)
# '''
# def get_track_aspects(time_frame):
#     track_features = []
#     for song in time_frame['items']:
#         track_features.append(song['id']) #id
#     return track_features
# track_features = get_track_aspects( )
# '''

def get_track_analysis(id):
    meta = sp.audio_features(id)
    song_acousticness = meta['acousticness']
    song_danceability = m\['danceability']
    list_analysis = [song_acousticness, song_danceability]
    print(list_analysis)
#     '''song_energy = 0
#     song_instrumentalness = 0
#     song_liveness = 0
#     song_loudness = 0
#     song_speechiness = 0
#     song_valence = 0
#     song_tempo = 0
#     '''
# ''''(sp.audio_features(get_track_ids(top_tracks_list)))
# print(analysis)'''''

user_analysis = []
for i in range(len(track_ids)):
    track = get_track_analysis(track_ids[i])
    user_analysis.append(track)