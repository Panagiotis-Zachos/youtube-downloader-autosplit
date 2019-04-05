from __future__ import unicode_literals
from pydub import AudioSegment
from time import time
from pathlib import Path
import pyperclip 
import youtube_dl
import os
import re
import sys

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def convert_to_ms(start_time):
    hms = start_time.split(':')
    if len(hms) == 3:
        [hour, min, sec] = hms
        start = int(hour)*60*60000 + int(min)*60000 + int(sec)*1000
    else:
        [min, sec] = hms
        start = int(min)*60000 + int(sec)*1000
    return start

def parse_description(description):

    regex = r'.*[0-9]{1,2}:[0-9]{2}.*'
    song_list = re.findall(regex, description)

    #Parse the video description for the song list
    #if not found, the user has to provide it
    #to give correct results the song list has to exist in 
    #{song_start} - Title or Title - {song_start} format
    if len(song_list) == 0:
        try:
            f1 = open('song_list.txt', 'r')
            for line in f1:
                song_list.append(line)
        except FileNotFoundError as error:
            print(error)
            print("Song list was not in the video description. You need to create the song_list.txt \
            \nusing the format specified at: https://github.com/Panagiotis-Zachos/youtube-downloader-autosplit")
            sys.exit()

    print("Song List:")
    for song in song_list:
        print(song.strip())
    return song_list

def arg_parser():
    if len(sys.argv) == 1: # No arguments passed, read url from clipboard and set outpath as current dir
        output_path = str(Path.home()) + "\\Music"
        url = pyperclip.paste()
        regex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        matches = re.findall(regex, url)
        if len(matches) == 0:
            print("Not enough arguments given, and wrong clipboard content.")
            print("Give video URL as argument or copy it to clipboard before running.")
            sys.exit()
    elif len(sys.argv) == 2: # 1 arg passed, the url
        output_path = str(Path.home()) + "\\Music"
        url = sys.argv[1]
    elif len(sys.argv) == 3: # both arguments passed
        url = sys.argv[1]
        output_path = sys.argv[2]
    else:
        print("Error: Too Many arguments.")
        print("Call like: video_download [URL] [output_directory]")
        sys.exit()
    return (url, output_path)

def song_parser(song_list):
    regex = r"[0-9]*:?[0-9]{1,2}:[0-9]{2}"
    name_list = []
    dur_list = []        
    for line in song_list:
        start_time = re.findall(regex, line)[0]
        dur_list.append(convert_to_ms(start_time))
        name_list.append(line.replace(start_time,'').strip())

    num_of_tracks = len(name_list)
    return (name_list,dur_list,num_of_tracks)

def main():
    
    url, output_path = arg_parser()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + r'/%(title)s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        # 'simulate': 'True',
        'progress_hooks': [my_hook],
        
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url)
        print('Done Converting. Splitting into tracks...')

        title = info['title']
        description = info['description']
        output_path += '/' + title + '/' #Into folder
        title = title.replace("/","_")
        mp3_audio = AudioSegment.from_file(output_path + title + ".mp3", format="mp3")

        song_list = parse_description(description)
        name_list,dur_list,num_of_tracks = song_parser(song_list)
        tot_duration = len(mp3_audio)
        dur_list.append(tot_duration)

        for i in range(num_of_tracks):
            start = dur_list[i]
            end = dur_list[i+1]
            cut = mp3_audio[start:end]
            track = open("{}{}.mp3".format(output_path,name_list[i]),'wb')
            cut.export(track, format='mp3')
            print("{} Tracks Remaining".format(num_of_tracks - (i+1)))
    print("Deleting downloaded file...")
    os.remove(output_path + title + ".mp3")


if __name__ == "__main__":
    t0 = time()
    main()
    print("Time elapsed: {:.2f}s".format(time()-t0))

