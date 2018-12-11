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

Socket.start()
sys.exit()


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

    #Sincroniza o JsPlayer
    sync = Sync.Sync();
    sync.syncJsPlayer();
    
    #Sincroniza o conteúdo
    thrSync = threading.Thread(target=sync.syncContent, args=(playerId))
    thrSync.start();

    #Abre e monitora a execução do player
    threading.Thread(target=watch.start).start()