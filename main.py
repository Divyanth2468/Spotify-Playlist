from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = YOUR CLIENT ID
CLIENT_SECRET = YOUR CLIENT SECRET
REDIRECT_URL = "http://example.com"
USER_ID = YOUR SPOTIFY USER ID
PLAY_LIST_POST_ADDRESS = f'https://api.spotify.com/v1/users/{USER_ID}/playlists'
songs_list = []
date = input("Which year do you want to travel to? Type the date in this format  YYY-MM-DD ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=billboard_url)
soup = BeautifulSoup(response.text, 'html.parser')

ordered_list = soup.find_all('span', class_='chart-element__information__song text--truncate color--primary')
for text in ordered_list:
    song_name = text.getText()
    songs_list.append(song_name)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
