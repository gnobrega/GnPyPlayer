import socketio
import eventlet
import eventlet.wsgi
import Util
from flask import Flask, render_template
util = Util.Util();

def start():

    sio = socketio.Server()
    app = Flask(__name__)

    @sio.on('connect')
    def connect(sid, environ):
        print("connect ", sid)

    @sio.on('keep-opened')
    def keepOpened(sid, data):
        #socket.emit("chat message", {a:123})
        #sio.emit('reply', room=sid)
        #sio.emit('message', data='abc')

        print("Socket, received command: keep-opened");
        util.setPreferences("keep-opened", str(data['status']))


    @sio.on('disconnect')
    def disconnect(sid):
        print('disconnect ', sid)

    #START
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)