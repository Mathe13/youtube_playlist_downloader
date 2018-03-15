"""Controlar de rotas."""
from app import app
from flask import render_template, request, send_from_directory
from app.core import Yt_Downloader


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.j2')


@app.route('/YoutubeDownloader/baixar', methods=['POST'])
def baixar_video():
    if request.method == 'POST':
        core = Yt_Downloader.Yt_Downloader(request.form['vid_name'])
        file_name = core.Download(path=app.config['MEDIA_FOLDER'])

        if file_name:
            print('entrou na parte de baixar')
            if not request.form.get('mp3'):
                return (send_from_directory(
                    app.config['MEDIA_FOLDER'],
                    file_name + '.mp4',
                    as_attachment=True,
                    mimetype='video/mp4'))
            else:
                Yt_Downloader.Yt_Downloader.video_to_mp3(
                    video_path=app.config['MEDIA_FOLDER'] + file_name + '.mp4',
                    mp3_path=app.config['MEDIA_FOLDER'],
                    file_name=file_name)
                print('cheguei aqui:', file_name)
                return (send_from_directory(
                    app.config['MEDIA_FOLDER'],
                    file_name + '.mp3',
                    as_attachment=True,
                    mimetype='audio/*'))

        else:
            return ('erro')
    else:
        return ('not okay')


# @app.route('/teste')
# def teste():
#     return send_from_directory(
#         app.config['MEDIA_FOLDER'], 'teste.txt', mimetype='text/txt')


@app.route('/YoutubeDownloader')
def Youtube():
    return render_template('youtube.html.j2')


@app.route('/SpotifyDownloader', defaults={'token': None})
@app.route('/SpotifyDownloader/', defaults={'token': None})
@app.route('/SpotifyDownloader/<string:token>')
def Spotify(token):
    print(token)
    return render_template('/spotify.html.j2', token=token)


# @app.route("/teste", defaults={'name': None})
# @app.route("/teste/<string:name>")
# def teste(name):
#     """Só um teste."""
#     if name:
#         return ("Olá " + name)
#     else:
#         return ("Olá estranho")
