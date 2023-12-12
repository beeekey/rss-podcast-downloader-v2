import csv
import pickle
from typing import List

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials


def fetch_albums(artist: str) -> List[str]:
    """
    Fetch all albums from a given artist and return a list of album names.
    """
    albums = []

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="b4f4e012388443c5ac05c7bee1518ca9",
        client_secret="e4ce7b749a17464ca1a93db292aa884c",
    ))

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Globi'

    playlists = {}
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        # print(artist['name'], artist['images'][0]['url'])

        artist_uri = f'spotify:artist:{artist["id"]}'

        results = spotify.artist_albums(artist_uri, album_type='album')
        albums = results['items']

        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])


        for album in albums:
            # print(album['name'], album['external_urls']['spotify'])
            pl = get_playlist(album['id'], spotify)
            playlists.update(pl)

        album_list = " ".join([album['external_urls']['spotify'] for album in albums])
        # print(album_list)


    file = open('playlists.pickle', 'wb')
    pickle.dump(playlists, file)
    file.close()

    print(playlists)

    myFile = open('playlists.csv', 'w')
    writer = csv.writer(myFile)
    for k, v in playlists.items():
        writer.writerow(f"{k},{v}")
    # # writer = csv.DictWriter(myFile, fieldnames=['name', 'track_number',])
    # # writer.writeheader()
    # # writer.writerows(playlists)
    myFile.close()


    return albums


def get_playlist(album_id: str, spotify):
    pl_info = {}
    pl = spotify.album_tracks(f'spotify:album:{album_id}')

    for v in pl["items"]:
        # print(v)
        pl_info[v["name"]] = v["track_number"]


    # print(pl_info)
    return pl_info

if __name__ == '__main__':
    fetch_albums("Globi")