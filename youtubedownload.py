import yt_dlp
import os

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4/bestaudio/best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename
