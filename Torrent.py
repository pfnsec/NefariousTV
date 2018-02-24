#!/usr/bin/python3
import libtorrent as lt
import time
import threading
import queue
import uuid

from tinydb import TinyDB, Query
from pprint import pprint 

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

db   = TinyDB('torrents.json')
User = Query()

#Queue of encoder jobs
from Encoder import EncoderQueue

#Queue of torrent jobs
TorrentQueue = queue.Queue()

session = lt.session()
session.listen_on(6881, 6891)
handles = []

folder = 'video'

alert_mask = (
    lt.alert.category_t.error_notification        |
 #   lt.alert.category_t.port_mapping_notification |
     lt.alert.category_t.storage_notification      |
 #   lt.alert.category_t.tracker_notification      |
     lt.alert.category_t.status_notification       |
 #   lt.alert.category_t.ip_block_notification     |
 #   lt.alert.category_t.performance_warning       |
    lt.alert.category_t.progress_notification
)

settings = {
    'alert_mask':alert_mask
}

session.apply_settings(settings)

alert_event = threading.Event()
torrent_event = threading.Event()


def dispatcher():
    while(True):
        session.wait_for_alert(3000)
        alerts = session.pop_alerts()

        alerts = [a for a in alerts if type(a) is not lt.piece_finished_alert]
        alerts = [a for a in alerts if type(a) is not lt.block_downloading_alert]
        alerts = [a for a in alerts if type(a) is not lt.block_finished_alert]

        if len(alerts) > 0:
            pprint(alerts)

        for a in alerts:
            if type(a) is lt.file_completed_alert:
                files = ''.join(a.handle.torrent_file().files().file_path(a.index))
                #print(files)
                EncoderQueue.put(files)
            elif type(a) is lt.add_torrent_alert:
                print("Added new torrent")
                handles.append(a.handle)
                pprint(a.handle.torrent_file())

            elif type(a) is lt.state_changed_alert:
                #pprint(a.handle.torrent_file())
                #pprint(dir(a.handle.torrent_file()))
                if(a.state == lt.torrent_status.seeding):
                    torrent_event.wait()
                    session.remove_torrent(a.handle)
                    handles.remove(a.handle)


def consume_torrents():
    while True:
        item = TorrentQueue.get()
        if item is None:
            continue
        startTorrent(item)
        torrent_event.wait()
        TorrentQueue.task_done()


def startTorrent(url):
    global session

    params = { 
        'save_path': folder,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'url':url
    }

    handle = session.add_torrent(params)
    print('Started torrent')


def queueTorrent(url, uuid):
    entry = {
        'url':url,
        'uuid':uuid,
        'complete':False
        }

    TorrentQueue.put(url)
    print('Queued torrent')



def listTorrents():
    state_str = ['queued', 'checking', 'downloading metadata', \
                 'downloading', 'finished', 'seeding', 'allocating']

    tlist = []
    #pprint(handles)

    for h in handles:
        s = h.status()

        info = {
                'name':    s.name,
                'progress':s.progress,
                'state':   state_str[s.state]
            }

        print(s.name)
        tlist.append(info)

        #print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
        #      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
        #       s.num_peers, state_str[s.state]))

    return tlist
    

threading.Thread(target=consume_torrents).start()
threading.Thread(target=dispatcher).start()


#Search the DB for torrents to resume...
resume_list = db.search(User.url.exists())
for t in resume_list:
    if not t['completed']:
        queueTorrent(t['url'], t['uuid'])

