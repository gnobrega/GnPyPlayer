import socketio
import eventlet
import eventlet.wsgi
import Util
from flask import Flask, render_template
util = Util.Util();
lastPing = 0
clientConnected = False
clientOfflineTime = 0
startCountTimeOffline = False

def start():

    sio = socketio.Server()
    app = Flask(__name__)

    @sio.on('connect')
    def connect(sid, environ):
        import Socket
        Socket.clientConnected = True
        Socket.startCountTimeOffline = True
        print("SocketIo: Connect ", sid)
        
    @sio.on('disconnect')
    def disconnect(sid):
        import Socket
        Socket.clientConnected = False
        print("SocketIo: Disconnect ", sid)

    @sio.on('keep-opened')
    def keepOpened(sid, data):
        #socket.emit("chat message", {a:123})
        #sio.emit('reply', room=sid)
        #sio.emit('message', data='abc')

        print("SocketIo: received command, keep-opened");
        util.setPreferences("keep-opened", str(data['status']))

    @sio.on('send-ping')
    def sendPing(sid, data):
        import Socket
        Socket.lastPing = 0
        
    #Recebe comando do JavaScript
    @sio.on('call-app')
    def callApp(sid, data):
        if "action" in data:
            if data['action'] == "log-view":
                if "data" in data:
                    util.logView(data['data'])

    @sio.on('get-info')
    def getInfo(sid, data):
        sio.emit('get-info-response', {'keep-opened':util.getPreferences("keep-opened")})

    #Incrementa o registro de ociosidade
    import threading
    threading.Thread(target=increaseLastPing).start()

    #START
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

#Incrementa o valor do ping
def increaseLastPing():
    import threading
    import Socket
    import time
    import Util
    util = Util.Util()

    while True:
        Socket.lastPing += 5
        time.sleep(5)
        
        try:
        
            #Inicia a verificação de conectividade com o Socket
            if Socket.startCountTimeOffline == True:
                if Socket.clientConnected == False:
                    Socket.clientOfflineTime += 5
                    if Socket.clientOfflineTime > 5:
                        print("Socket: O clinte perdeu a comunicação com o SocketIO")
                        Socket.startCountTimeOffline = False
                        Socket.clientOfflineTime = 0
                        util.closeApp();
                        time.sleep(3)
                        threading.Thread(target=util.startPlayer).start()
                        
        except Exception as e:
            print("Exception no monitoramento do Socket");
