# Youtube-Downloader-Autosplit v2
Simple command prompt app I created (Python 3.7.3) to easily download and split full albums into separate tracks from youtube

This has only been tested on Windows 10!
This supports videos of arbitrary length, the only bottleneck is your internet speed.

Installation
-------

There are two ways to install. 

1. Automatically using setup.exe under: https://github.com/Panagiotis-Zachos/youtube-downloader-autosplit/releases

2. Μanually by following the steps under requirements (recommended).

Requirements
-------
Python 3.7 added to PATH

If you don't know what this means, check out this tutorial: https://geek-university.com/python/add-python-to-the-windows-path/

Libraries: pyperclip, youtube_dl
ffmpeg

1. To install the libraries, download the requirements.txt
2. Hit Win+R and type "cmd"
3. From there type "cd Downloads"
4. Then type "pip install -r requirements.txt"

To download ffmpeg go to: https://ffmpeg.zeranoe.com/builds/
Unzip, and add the /bin folder to PATH

Tutorial Here: https://windowsloop.com/install-ffmpeg-windows-10/

Common Usage
=========
In cmd type:

python PyVidSplit -u(--URL) [VIDEO_URL] -o(--output) [Output Directory] -t(--type) [Output File Type]

If no [Output Directory] is given the Music directory will be used

If no [VIDEO_URL] is given the programm will try to read from the clipboard. So you can
copy the URL and just run "python video_download"

If no [Output File Type] is given the default is .opus

If you use the installer replace "python PyVidSplit" with "PyVidSplit.exe" without the "

The programm will first try to parse the video description to find a tracklist, along with the start
time of each track. If that fails it will try to read from 'song_list.txt' that you need to create
yourself using the following format:

{Title1} {StartTime1}

{Title2} {StartTime2}

.

.

.

You can check song_list.txt in this repo for an example
