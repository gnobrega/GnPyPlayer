import socketio
import eventlet
import eventlet.wsgi
import Util
from flask import Flask, render_template
util = Util.Util();
lastPing = 0

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

    @sio.on('send-ping')
    def sendPing(sid, data):
        import Socket
        Socket.lastPing = 0

    @sio.on('get-info')
    def getInfo(sid, data):
        sio.emit('get-info-response', {'keep-opened':util.getPreferences("keep-opened")})

    @sio.on('disconnect')
    def disconnect(sid):
        print('disconnect ', sid)

    #Incrementa o registro de ociosidade
    import threading
    threading.Thread(target=increaseLastPing).start()

    #START
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

def increaseLastPing():
    import Socket
    import time

    while True:
        Socket.lastPing += 10
        time.sleep(10)
        #print("LastPing: " + str(Socket.lastPing));
