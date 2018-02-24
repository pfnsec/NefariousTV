import os
import queue
import random
import time
from pprint  import pprint
from os.path import splitext
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def listFiles():
    flist = []

    for root, dirs, files, in os.walk('./video/'):
        path = root.split(os.sep)

        for file in files:
            if(splitext(file)[1] == '.mpd'):
                show = path[2:-1]
                if(len(show) > 0):
                    showdir = '/'.join(show) + '/'
                else:
                    showdir = ''

                flist.append({
                        'name':file,
                        'show':showdir,
                        'path':showdir + splitext(file)[0] + '/' + file
                    })


    return flist


playlistPosition = 0
currentTrack = None
currentTime  = 42
timeStarted  = 0

playlist = queue.Queue()

def getTrack():
    global currentTrack
    global currentTime
    global timeStarted
    flist = listFiles()
    #if(len(playlist == 0)):
        
    print(currentTrack)
    print(timeStarted)
        
    if(currentTrack == None):
        currentTrack = random.choice(flist)['path']

    if(timeStarted == 0):
        timeStarted = time.time()
        
    #currentTrack = flist[playlistPosition]['path']
    return {
            'currentTrack':currentTrack,
            'timeStarted' :timeStarted
        }

def playTrack(name):
    global currentTrack
    global currentTime
    global timeStarted
    flist = listFiles()
    paths = [f['path'] for f in flist]
    res = process.extractOne(name, paths)
    print(res)
    currentTrack = res[0]
    timeStarted = 0
