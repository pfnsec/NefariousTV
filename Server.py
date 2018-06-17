#!/usr/bin/python3
import flask
from flask import Flask, request, session, redirect
from flask_cors import CORS, cross_origin
#from flask_socketio import SocketIO


import configparser
import logging
import time
from pprint import pprint

import Torrent
import Playlist
import Auth
import Youtube
#import eventlet
#import eventlet.wsgi
#eventlet.monkey_patch()

config = configparser.ConfigParser()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#socketio = SocketIO(app)

#socketio.init_app(app, async_mode='gevent_uwsgi')
#socketio.init_app(app, async_mode='eventlet')
#socketio.init_app(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

users = {}


@app.before_request
def make_session_permanent():
    session.permanent = True

def requestSync():
	pass
	#socketio.emit('track', { 'hello': 'world' });


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
    search = request.args.get('search')
    return flask.jsonify(Playlist.listFiles(search)), 200

@app.route('/list_playlists')
def list_playlists():
    search = request.args.get('search')
    return flask.jsonify(Playlist.listPlaylists(search)), 200


@app.route('/list_users')
def list_users():
    #search = request.args.get('search')
    return flask.jsonify(users), 200


@app.route('/track')
@cross_origin()
def get_track():
    tnow = time.time()
    users[session['name']] = {
            "time": tnow,
            "state": ""
        }

    track = Playlist.getTrack()

    active_users = []
    for name, state in users.items():
        if (tnow - state['time']) < 30:
            active_users.append({name: state})

    res = {
            "track":track,
            "users":active_users,
    }

    return flask.jsonify(res), 200

@app.route('/play_track')
def queue_track():
    name = request.args.get('name')
    res = Playlist.playTrack(name)
    return flask.jsonify(res), 200


@app.route('/play_playlist')
def queue_list():
    name = request.args.get('name')
    res = Playlist.playPlaylist(name)
    return flask.jsonify(res), 200

@app.route('/skip')
def skip_track():
    res = Playlist.skipTrack()
    return flask.jsonify(res), 200

@app.route('/yt_add')
def yt_add():
    url = request.args.get('url')
    res = Youtube.add(url)
    return flask.jsonify(res), 200

#The bot GETs this with a signed message 
#to get the server to mint a new token.
@app.route('/create_token')
def create_token():
    name = request.args.get('name')
    sig  = request.args.get('sig')

    res = Auth.createToken(name, sig)

    if res is None:
        flask.abort(401)

    #We return the token id used to collect the token.
    #This is randomly generated and used as the lookup key in our local
    #access token database!
    return flask.jsonify(res), 200

#The bot links the user to this URL. 
#The token expires after it's collected 
#and added to the user's session.
#'token_id' is 
@app.route('/collect_token')
def collect_token():
    token_id = request.args.get('token_id')

    res = Auth.collectToken(token_id)

    if res is None:
        flask.abort(401)

    if(res['token_id'] != token_id):
        print('blurgh!')
        print(res['token_id'])
        print(token_id)

    session['ntv_token'] = res['token_id']
    session['name'] = res['name']

    #return flask.jsonify(res), 200
    return flask.redirect("/")

    

@app.route('/auth')
def auth():
    try:
        res = Auth.lookupToken(session['ntv_token'])
        name = res['name']
    except:
        flask.abort(401)

    return name, 200



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
    
#@socketio.on('track')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    return None

app.secret_key = "weebtv"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)


