# youtube-downloader-autosplit
Simple app I created (Python 3.7.3) to easily download full albums from youtube

This has only been tested on Windows 10
Libraries needed: pyperclip, youtube_dl and pydub
ffmpeg is also necessary.

1. To install the libraries, download the requirements.txt along the video_downloader.py
2. Hit Win+R and type "cmd"
3. From there type "cd Downloads"
4. Then type "pip install -r requirements.txt"

To download ffmpeg go to: https://ffmpeg.zeranoe.com/builds/
Unzip, and add the /bin folder to PATH
Tutorial Here: https://windowsloop.com/install-ffmpeg-windows-10/

Common Usage
=========

python video_download [VIDEO_URL] [OUPUT_LOCATION]

If no [OUPUT_LOCATION] is given the current working directory will be used
If no [VIDEO_URL] is given the programm will try to read from the clipboard. So you can
copy the URL and just run "python video_download"

The programm will first try to parse the video description to find a tracklist, along with the start
time of each track. If that fails it will try to read from 'song_list.txt' that you need to create
yourself using the following format:

{Title1} {StartTime1}

{Title2} {StartTime2}

.

.

.

You can check song_list.txt in this repo for an example
