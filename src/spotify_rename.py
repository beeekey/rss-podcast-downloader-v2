import os
import pickle

file = open('playlists.pickle', 'rb')
playlists = pickle.load(file)
file.close()

base_path = '/home/ben/dev/kaudio/back/spotify_fetcher'


# iter over all folders in base_path
albums = [os.path.join(base_path, x) for x in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, x))]

for album in albums:
    tracks = [ x for x in os.listdir(album) if os.path.isfile(os.path.join(album, x)) and x.endswith('.mp3')]

    for track in tracks:
        try:
            track_name = track.replace(".mp3", "")
            if "-" in track:
                track_number = playlists[track_name.split('-')[1].strip()]
            else:
                track_number = playlists[track_name]
            os.rename(os.path.join(album, track), os.path.join(album, f"{track_number:02d} - {track}"))
        except KeyError:
            print(track)
            pass