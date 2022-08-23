from pytube import Playlist, YouTube
import validators
from pathlib import Path
import os
import concurrent.futures
import subprocess


def check_option(p:str, options:list):
    while True:
        if p not in options:
            print("Incorrecct option,try again\n")
            p = input('\n') 
        else:
            return p


def vid_or_aud(vid, audio:bool, output_path):

    if audio:
        vid.streams.filter(only_audio=audio, abr='160kbps').first().download(output_path=output_path)
    else:
        vid.streams.filter(progressive=True).get_highest_resolution().download(output_path=output_path)    

def convert_to_mp3(vid, output_path):

    mp3File = ''.join(output_path).replace("webm", "mp3")
    command = f"ffmpeg -i \"{output_path}\" -vn -ab 128k -ar 44100 -y \"{mp3File}\""
    subprocess.call(command, shell=True)    
    os.remove(output_path)

p = input("Enter p for playlist,enter v for video\n")
p = check_option(p, ['p', 'v']) 

url = input("Enter url\n")

while True:
    if not validators.url(url):
        print("Not valid url,try again\n")
        url = input('\n')
    else:
        break    

f_format = input("Enter 3 for mp3(audio), enter 4  for mp4(video)\n")
f_format = check_option(f_format, ['3','4'])

adonl = False
if f_format == '3':
    adonl = True

default_path = str(Path.home() / "Downloads")
output_path = input(f"Enter path to save, folder 'yt_downloads' will be automatically created, enter 0 to save in {default_path}\n")

if output_path == '0':
    output_path = default_path

if p == 'p':

    p = Playlist(url)  
    output_path = '/'.join((output_path, 'yt_downloads'))    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for vid in p.videos:
            print(f"Downloading {vid.title}")
            executor.submit(vid_or_aud, vid, adonl, output_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for file in os.listdir(output_path):
            file_path = '/'.join((output_path, file))
            executor.submit(convert_to_mp3, file, file_path)        
else:
    p = YouTube(url)
    print(f"Downloading {p.title}")
    vid_or_aud(p, adonl, output_path)
    if adonl:
        for file in os.listdir(output_path):
            file_path = '/'.join((output_path, file))
            convert_to_mp3(file, file_path) 