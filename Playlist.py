import os
import re
import queue
import random
import time
from pprint  import pprint
from os.path import splitext,isfile
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import Server


def strip_tags(name):
    """Strips tags in brackets like [1080p] from names"""
    pattern = r'[\s]*\[[^\]]*\][\s]*'
    name = re.sub(pattern, '', name)
    pattern = r'[\s]*\([^\)]*\)[\s]*'
    name = re.sub(pattern, '', name)
    return name


def listFiles(search, videopath='./video/'):
    flist = []
    if search is not None:
        search = search.split('/')

    for root, dirs, files, in os.walk(videopath):
        path = root.split(os.sep)

        for file in files:
			
            if(splitext(file)[1] == '.mpd'):
                #print(file)
                show = path[2:-1]
                if(len(show) > 0):
                    showdir = '/'.join(show) + '/'
                else:
                    showdir = ''

                trackdir = splitext(file)[0]

                if(isfile(f'./video/{showdir}/{trackdir}/.{trackdir}.complete')):
                    flist.append({
                            'name':file,
                            'track':trackdir,
                            'show':showdir,
                            'path':showdir + trackdir + '/' + file
                        })

    

    items = []

    for f in flist:
        #show = f['show']
        
        track = strip_tags(f['track'])
        track = re.sub(r'\W+', '', track)
        track = track.lower();

        items.append((fuzz.partial_ratio(track, search), f))
        paths = sorted(items, key=lambda p: p[0]) 
        score = paths[-1][0] 

       #show = strip_tags(f['show'])
       #show = re.sub(r'\W+', '', show)
       #show = show.lower();

       #items.append((fuzz.partial_ratio(show, search), f))
       #paths = sorted(items, key=lambda p: p[0]) 
       #score = paths[-1][0] 

        res = []

        for p in paths:
            if p[0] == score:
                res.append(p[1]['path'])

    print(res)


    return res

#function getPlaylists:
#return a list of directories that have a .playlist file
def listPlaylists(search, videopath='./video/'):
    plist = []
    if search is not None:
        search = search.split('/')

    for root, dirs, files, in os.walk(videopath):
        path = root.split(os.sep)

        for file in files:
            if(splitext(file)[1] == '.playlist'):
                name = splitext(file)[0]

                plist.append({
                    'name':name,
                    'dir':root})

    return plist

#function nextPlaylist:
#Set the currentPlaylist and playlistPosition/shuffle


playlistPosition = 0
currentTrack = None
currentTime  = 42
timeStarted  = 0

currentPlaylist = None

playlist = queue.Queue()

def playPlaylist(search):
    global currentTrack
    global currentPlaylist
    global currentTime
    global timeStarted
    plist = listPlaylists(None)
    paths = []
    for p in plist:
        #show = strip_tags(f['show'])
        #name = strip_tags(f['name'])
        #paths.append(strip_tags(f'{show}{name}'))
        paths.append(p['name'])
    #res = process.extract(search, paths, scorer=fuzz.token_sort_ratio, limit=10)
    res = process.extract(search, paths, limit=10)

    #Set the matching playlist entry 
    currentPlaylist = [p for p in plist if p['name'] == res[0][0]][0]
    currentTrack = None
    timeStarted = 0
    Server.requestSync();
    return [res[0][0]]

shuffle = False
trackIndex = 0

def getTrack():
    global currentTrack
    global currentPlaylist
    global currentTime
    global timeStarted
        
    if(currentTrack == None):
        if(currentPlaylist == None):

            flist = listFiles(None)

            if(shuffle):
                currentTrack = random.choice(flist)
            else:
                trackIndex = 0
                currentTrack = flist[trackIndex % len(flist)]

        else:
            flist = listFiles(currentPlaylist['dir'])
            print(flist)

            if(shuffle):
                currentTrack = random.choice(flist)
            else:
                trackIndex += 1
                currentTrack = flist[trackIndex % len(flist)]


    if(timeStarted == 0):
        timeStarted = time.time() + 1
        
    #currentTrack = flist[playlistPosition]['path']
    return {
            'currentTrack':currentTrack,
            'timeStarted' :timeStarted
        }

def skipTrack():
    global currentTrack
    global currentPlaylist
    global timeStarted

    if(currentPlaylist == None):
        flist = listFiles(None)
        currentTrack = random.choice(flist)
    else:
        flist = listFiles(None, videopath = currentPlaylist['dir'])
        currentTrack = random.choice(flist)

    timeStarted = 0

    return currentTrack

def playTrack(search):
    global currentTrack
    global currentTime
    global timeStarted
    flist = listFiles(search)

    #currentTrack = random.choice(flist)
    currentTrack = flist[0]
    timeStarted = 0
    Server.requestSync();
    return [currentTrack]
