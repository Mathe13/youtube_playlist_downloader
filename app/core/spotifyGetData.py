# !/usr/bin/env python
import requests
import sys


class spotifyData():
    def __init__(self, token):
        self.tok = token
        #  track dictionary
        self.mytracks = []

    def getTrackData(self, url):
        print('\nget_track_data')

        #  Spotify track API
        self.api_url_track = "https://api.spotify.com/v1/tracks/"
        newURL = self.api_url_track + str(url) + "?market=ES"
        print('\tAcessing ' + newURL)

        try:
            response = requests.get(
                newURL,
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.tok
                })
        except Exception as e:
            print(
                "\n\tError connecting to spotify API looking details for uri %s"
                % url)
            return False

        try:
            data = response.json()
        except Exception as e:
            print("\n\tError handling json object looking details for uri %s" %
                  url)
            return False

        try:
            self.mytracks.append({
                'album': str(data['album']['name']),
                'artist': str(data['artists'][0]['name']),
                'track': str(data['name'])
            })
            sys.stdout.write("\tThe data is save")
            sys.stdout.flush()
        except Exception as e:
            print("\n\tError getting details for uri %s" % url)
            print(data)
            return False

    def setTrackDataWithIdTrackOnFile(self, input_file):
        print('setTrackDataWithIdTrackOnFile')
        #  Open input file
        try:
            fd = open(input_file, "r")
        except Exception as e:
            print("Error opening %s" % input_file)
            print(e)
            sys.exit(0)

        sys.stdout.write("\tIterating through tracks in " + input_file)
        sys.stdout.flush()
        for track in fd:
            self.getTrackData(url=(track.split(":")[2]).split('\n')[0])


#  close input file
        fd.close()

    def getDataTracks(self, ordination='artist'):
        #  it can be ordered by 'artist', 'album' or 'track'
        return sorted(self.mytracks, key=lambda k: k[ordination])

    def getDataPlaylistTracks(self, user, playlistID):
        print('\ngetDataPlaylistTracks')

        #  Spotify playlist tracks API
        self.api_url_playlist_track = "https://api.spotify.com/v1/users/" + \
            user + "/playlists/" + playlistID + "/tracks?market=ES"
        print('\tAcessing ' + self.api_url_playlist_track)

        try:
            response = requests.get(
                self.api_url_playlist_track,
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.tok
                })
        except Exception as e:
            print(
                "\n\tError connecting to spotify API looking details for uri %s"
                % self.api_url_playlist_track)
            return False

        try:
            data = response.json()
        except Exception as e:
            print("\n\tError handling json object looking details for uri %s" %
                  self.api_url_playlist_track)
            return False

        try:
            for d in data['items']:
                # print(str(d['track']['album']['name']) + "\n")
                self.mytracks.append({
                    'album':
                    str(d['track']['album']['name']),
                    'artist':
                    str(d['track']['artists'][0]['name']),
                    'track':
                    str(d['track']['name'])
                })

            sys.stdout.write("\tThe data is save")
            sys.stdout.flush()
        except Exception as e:
            print("\n\tError getting details for uri %s" %
                  self.api_url_playlist_track)
            print(data)
            return False


'''
token = '' # token gerado pelo spotify para acessar a api
teste = spotifyData(token = token)
spotifyURI_Playlist = 'spotify:user:<NOME DO USUARIO>:playlist:<ID DA PLAYLIST>' # URI de uma playlist do spotfy
teste.getDataPlaylistTracks(user = spotifyURI_Playlist.split(":")[2], playlistID =spotifyURI_Playlist.split(":")[4])
print(str(teste.getDataTracks()))
'''
