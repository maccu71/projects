import os
import json
import time
import requests
from math import floor
import vlc

def download():
    print('We need to download data from the web...one moment')
    URL = "http://91.132.145.114/json/stations"
    response = requests.get(URL)
    if response.status_code == '200':
        open("stations", "wb").write(response.content)
    else:
        print('strona z bazą stacji radiowych jest nieaktywna..')
        exit

# check if the file exists and is not too old, alternatively download
filename = 'stations'
days = 30

if os.path.exists(filename):
    file_time = os.path.getmtime(filename)
    current_time = time.time()
    time_diff = current_time - file_time
    days_diff = floor(time_diff / (24 * 3600))
    if days_diff > days:
        download()
    else:
        print(f'loading data from a file... it\'s only {days_diff} days old')
else:
    download()


with open('stations', 'r') as st:
    stacje = json.load(st)

po_wyb = []
while len(po_wyb) == 0:
    name_station = input('Enter the name of the station: ').lower()
    for stacja in stacje:
        if name_station in stacja.get('name').lower():
            # print(stacja)
            c = stacja.get('name'), stacja.get('url'), stacja.get('votes'), stacja.get('bitrate')
            po_wyb.append(c)

print('\nnr   vote      bitrate      name')
for i, y in enumerate(po_wyb):
    print(str(i+1).ljust(5, ' ') + (str(y[2]).ljust(10, ' ') + str(y[3]).ljust(13, ' ') + str(y[0])))

ktora = int(input('\nWhich one you want? (enter the nr): '))
urls = po_wyb[ktora-1][1]

print(f'stacja: {urls}\n')

# zapisac = input('Write your stream to a file? y/n ').lower()

# if zapisac == 'y':
#     extension = int(time.monotonic())
#     chosen = (po_wyb[ktora-1][0]).replace(' ', '_')#.replace('\'','')
#     filling = (f'/home/maco/Pulpit/{chosen}_{extension} -i {urls} &')  or use $PWD
#     filling = (f'/home/maco/Pulpit/{chosen} -i {urls} &') # or use $PWD
#     print(chosen)
#     os.system('ffmpeg -f ogg '+ filling)

def getData(url):
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    prev = ""
    while True:
        time.sleep(1)
        m = Media.get_meta(12) # vlc.Meta 12: 'NowPlaying',
        if m != prev:
            print(m)
            prev = m
#             with open(f'/home/maco/Pulpit/{chosen}.txt','a') as file:
#                 file.write(f'{m}\n')
    return player.audio_get_track_description()

print(getData(urls))
