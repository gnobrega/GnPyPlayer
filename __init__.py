import sys
import threading
import Watch
import Constants
import Util
import os
import Sync
import Socket

constants = Constants.Constants()
watch = Watch.Watch()
util = Util.Util()
playerId = 0


#Inicia o socket
threading.Thread(target=Socket.start).start()

#Oculta o cursor
util.hideCursor()

#Cria os diretórios
os.makedirs(constants.PATH_CONTENT, exist_ok=True)
os.makedirs(constants.PATH_JSPLAYER, exist_ok=True)

#Obtém a autorização
objAuth = util.getAuth();
if "auth" in objAuth:
    if objAuth['auth'] == 'allow':
        playerId = objAuth['id']

if int(playerId) > 0:

    #Registra o id do player
    util.setPreferences('id_player', playerId)

    #Envia os pings para o servidor
    threading.Thread(target=util.pingServer, args=(playerId,)).start()

    #Sincroniza o JsPlayer
    sync = Sync.Sync();
    sync.syncJsPlayer();
    
    #Sincroniza o conteúdo
    thrSync = threading.Thread(target=sync.syncContent, args=(playerId,))
    thrSync.start();

    #Abre e monitora a execução do player
    threading.Thread(target=watch.start).start()

    # Realiza a captura de tela e o envio ao servidor
    threading.Thread(target=util.sendScreenshot, args=(playerId,)).start()
