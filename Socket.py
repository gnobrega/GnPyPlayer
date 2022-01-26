from websocket_server import WebsocketServer
import json
import Util

util = Util.Util();
lastPing = 0
clientConnected = False
clientOfflineTime = 0
startCountTimeOffline = False

def start():
    
    # Called for every client connecting (after handshake)
    def new_client(client, server):
        import Socket
        print("[SOCKET] Cliente conectado id %d" % client['id'])
        #server.send_message_to_all("Hey all, a new client has joined us")
        Socket.clientConnected = True
        Socket.startCountTimeOffline = True


    # Called for every client disconnecting
    def client_left(client, server):
        import Socket
        Socket.clientConnected = False
        print("Client(%d) disconnected" % client['id'])


    # Called when a client sends a message
    def message_received(client, server, message):
        #print("Client(%d) said: %s" % (client['id'], message))
        
        objJson = json.loads(message);
        if 'command' in objJson:
            
            #Ping
            if objJson['command'] == 'send-ping':
                import Socket
                Socket.lastPing = 0
                #print('[SOCKET] Ping received')
                
            #LogView
            if objJson['command'] == 'log-view':
            	if "data" in objJson:
            		util.logView(objJson['data'])

    # Incrementa o registro de ociosidade
    import threading
    threading.Thread(target=increaseLastPing).start()	

    # Ini socket server
    PORT=8000
    server = WebsocketServer(PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()

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
                        print("[SOCKET] O clinte perdeu a comunicação com o Socket")
                        Socket.startCountTimeOffline = False
                        Socket.clientOfflineTime = 0
                        util.closeApp();
                        time.sleep(3)
                        threading.Thread(target=util.startPlayer).start()
                        
        except Exception as e:
            print("(X) Exception no monitoramento do Socket");
