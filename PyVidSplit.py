from __future__ import unicode_literals

import getopt
import os
import re
import sys
import wave
from pathlib import Path
from time import time

import ffmpeg
import pyperclip
import youtube_dl


def arg_parser():

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "u:o:t:", ["URL=", "output=", "type="]
            )
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    output_path = str(Path.home()) + "\\Music"
    url = pyperclip.paste()
    ftype = 'opus'

    for o, a in opts:
        if o in ('-u', '--URL'):
            url = a
        elif o in ('-o', '--output'):
            output_path = a
        elif o in ('-t', '--type'):
            ftype = a
        else:
            assert False, "Unhandled Option"

    try:
        regex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        matches = re.findall(regex, url)
        if len(matches) == 0:
            raise Exception(
                'URL not recognized. Please provide a valid youtube URL'
                )

        if ftype not in ('wav', 'opus', 'mp3'):
            raise Exception(
                'FileType not supported. Please choose from: \
                    wav, opus or mp3 file types')

    except Exception as inst:
        x = inst.args[0]
        print(x)
        sys.exit(1)

    return (url, output_path, ftype)


def parse_description(description):

    regex = r'.*[0-9]{1,2}:[0-9]{2}.*'
    song_list = re.findall(regex, description)

    # Parse the video description for the song list
    # if not found, the user has to provide it
    # to give correct results the song list has to exist in
    # {song_start} - Title or Title - {song_start} format
    if len(song_list) == 0:
        try:
            f1 = open('song_list.txt', 'r')
            for line in f1:
                song_list.append(line)
        except FileNotFoundError as error:
            print(error)
            print("Song list was not in the video description. \
            You need to create the song_list.txt \
            \nusing the format specified at: \
            https://github.com/Panagiotis-Zachos/youtube-downloader-autosplit")
            sys.exit()

    print("\n\nSong List:\n")
    for song in song_list:
        print(song.strip())
    print("\n")
    return song_list


def song_parser(song_list):
    regex = r"[0-9]*:?[0-9]{1,2}:[0-9]{2}"
    name_list = []
    dur_list = []
    for line in song_list:
        start_time = re.findall(regex, line)[0]
        dur_list.append(convert_to_sec(start_time))
        name_list.append(line.replace(start_time, '').strip())

    num_of_tracks = len(name_list)
    return (name_list, dur_list, num_of_tracks)


def convert_to_sec(start_time):
    hms = start_time.split(':')
    if len(hms) == 3:
        [hour, min, sec] = hms
        start = int(hour)*60*60 + int(min)*60 + int(sec)
    else:
        [min, sec] = hms
        start = int(min)*60 + int(sec)
    return start


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def main():

    url, output_path, ftype = arg_parser()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': r'{}'.format(output_path) + r'/%(title)s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',
        }],
        'simulate': 'True',
        'keepvideo': 'True',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url)
        print('Done Converting. Splitting into tracks...')
        title = info['title']

        description = info['description']
        tot_duration = info['duration']
        title = title.replace("/", "_")
        song_list = parse_description(description)
        name_list, dur_list, num_of_tracks = song_parser(song_list)
        dur_list.append(tot_duration)

        src = '{0}/{1}/{1}.wav'.format(output_path, title)
        fp = wave.open(src)

        for i in range(num_of_tracks):

            name_list[i] = name_list[i] \
                .replace(':', '') \
                .replace('-', '') \
                .replace('"', '') \
                .replace("'", '') \
                .strip()
            start = dur_list[i]
            end = dur_list[i+1]
            sec = end-start
            output = wave.open(
                '{}/{}/{}.wav'.format(
                    output_path, title, name_list[i]), 'wb'
                )
            output.setparams(fp.getparams())
            frames_to_read = fp.getframerate() * sec

            frames = fp.readframes(frames_to_read)
            if not frames:
                break

            output.writeframes(frames)
            if ftype != 'wav':
                (
                    ffmpeg
                    .input('{}/{}/{}.wav'.format(
                        output_path, title, name_list[i])
                        )
                    .output(
                        '{}/{}/{}.{}'.format(
                            output_path, title, name_list[i], ftype),
                        **{'loglevel': 'panic', 'ab': '192k'})
                    .overwrite_output()
                    .global_args('-hide_banner', '-stats')
                    .run()
                )
                output.close()
                print("Done with song: {}".format(name_list[i]))
                os.remove('{}/{}/{}.wav'.format(
                    output_path, title, name_list[i])
                    )
        fp.close()
        os.remove('{0}/{1}/{1}.wav'.format(output_path, title))


if __name__ == '__main__':

    t0 = time()
    main()
    print(time() - t0)
