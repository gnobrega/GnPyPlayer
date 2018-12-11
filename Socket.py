import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template

def start():

    sio = socketio.Server()
    app = Flask(__name__)

    @sio.on('connect')
    def connect(sid, environ):
        print("BBBBBBBBBBBB")
        print("connect ", sid)

    @sio.on('chat message')
    def message(sid, data):
        #socket.emit("chat message", {a:123})
        print("CCCCCCCCCCC")
        print("message ", data)
        sio.emit('reply', room=sid)

    @sio.on('disconnect')
    def disconnect(sid):
        print('disconnect ', sid)

    #START
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)