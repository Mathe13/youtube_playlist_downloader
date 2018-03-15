"""Gerencia arquivos de video e audio"""
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
from app.core import Searcher


class Yt_Downloader():
    def __init__(self, video_tag):
        print('entrou')
        if Yt_Downloader.is_link(video_tag):
            # print('é link')
            self.link = Yt_Downloader.validate_link(video_tag)
        else:
            # print('não é link')
            self.link = Searcher.YouTube_Searcher.search(video_tag, 's')

    def Download(self, path='/tmp'):
        print('baixar')
        if Yt_Downloader.check_path(path):
            yt = YouTube(self.link)
            print(self.link)
            video_links = yt.streams.filter(file_extension='mp4').all()
            if video_links:
                print('Baixando video' + yt.title)
                file_name = yt.title
                file_name = Yt_Downloader.normalize_name(file_name)
                if not os.path.exists(path + file_name + '.mp4'):
                    print(path + file_name)
                    video_links[0].download(
                        output_path=path, filename=file_name)
                return file_name
        return False

    @staticmethod
    def normalize_name(name):
        falhas = []
        for i in range(len(name)):
            if not (name[i].isalnum()):
                falhas.append(name[i])
        for falha in falhas:
            name = name.replace(falha, ' ')
        name = name.encode('ascii', 'ignore')
        name = name.decode('utf-8')
        name = name.replace(' ', '')
        return name

    @staticmethod
    def is_link(link):
        # print('verifica')
        if link.find('www.youtube.com/watch?v=') >= 0:
            return True
        return False

    @staticmethod
    def validate_link(link):
        # print('valida')
        if not link.find('https://') >= 0:
            link = 'https://' + link
        return link

    @staticmethod
    def check_path(path_to_check, creat='s'):
        print('checando' + path_to_check)
        if not (os.path.exists(path_to_check)):
            print('a pasta vai ser criada')
            if creat == 's':
                try:
                    os.makedirs(path_to_check)
                except Exception as e:
                    print("erro ao criar arquvio", e)
                    return False
            else:
                print('a pasta não existe')
                return False
        print('a pasta existe')
        return True

    @staticmethod
    def video_to_mp3(video_path, mp3_path, file_name, manter='n'):
        print('teste' + video_path)
        if not Yt_Downloader.check_path(video_path, 's'):
            print('erro na pasta do video')
            return False
        if not Yt_Downloader.check_path(mp3_path):
            print('erro ao criar pastas para mp3')
            return False
        try:
            print('tentando converter')
            print(file_name + '.mp3')
            videoclip = VideoFileClip(video_path)
            audioclip = videoclip.audio
            audioclip.write_audiofile(
                filename=(mp3_path + file_name + '.mp3'),
                nbytes=2,
                codec='mp3',
                write_logfile=False)
            return True
        except Exception as e:
            print('erro na conversão', e)
            return False
        if manter == 'n':
            os.remove(video_path)
        print('terminado')
