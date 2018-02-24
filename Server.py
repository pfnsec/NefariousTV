#!/usr/bin/python3
import flask
from flask import Flask,request
from flask_cors import CORS, cross_origin

import Torrent
import Playlist

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/torrent')
def add_torrent():
    print('torrent')
    url = request.args.get('url')
    Torrent.queueTorrent(url, 0)
    return 'Dope', 200

@app.route('/list_torrents')
def list_torrents():
#    name = request.args.get('name')
    return flask.jsonify(Torrent.listTorrents()), 200


@app.route('/list_files')
def list_files():
#    name = request.args.get('name')
    return flask.jsonify(Playlist.listFiles()), 200


@app.route('/track')
@cross_origin()
def get_track():
    return flask.jsonify(Playlist.getTrack()), 200

@app.route('/queue')
def queue_track():
    name = request.args.get('name')
    Playlist.playTrack(name)
    return "Dope", 200

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    

if __name__ == '__main__':
        app.run(host='0.0.0.0')
