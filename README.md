# youtube-downloader-autosplit
Simple app I created (Python 3.7.3) to easily download full albums from youtube

Libraries needed: pyperclip, youtube_dl and pydub
ffmpeg is also necessary.

Download the python script and use as follows.

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

