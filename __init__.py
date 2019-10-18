import sys
import threading
import Watch
import Constants
import Util
import os
import Sync
import Socket

watch = Watch.Watch()
util = Util.Util()
playerId = 0
isOnline = False

#Inicia o socket
threading.Thread(target=Socket.start).start()

#Oculta o cursor
util.hideCursor()

#Cria os diretórios
os.makedirs(Constants.PATH_CONTENT, exist_ok=True)
os.makedirs(Constants.PATH_JSPLAYER, exist_ok=True)

#Registra a versão na máquina
util.registerVersion()

#Obtém a autorização
objAuth = util.getAuth();
if "auth" in objAuth:
    if objAuth['auth'] == 'allow':
        playerId = objAuth['id']

#Verifica a conexão  
if objAuth['online'] == True:
    isOnline = True

if int(playerId) > 0:

    #Registra o id do player
    util.setPreferences('id_player', playerId)
    
    #Envia o status ONLINE para o servidor
    threading.Thread(target=util.pingServer, args=(playerId,)).start()

    #Sincroniza o JsPlayer
    sync = Sync.Sync();
    if isOnline == True:

        #Verifica se o JsPlayer já foi baixado, se sim, atualiza em background
        if os.path.exists(Constants.PATH_JSPLAYER+"index.html"):
            print("Sincronizando o JsPlayer em background");
            threading.Thread(target=sync.syncJsPlayer).start()
        else:
            print("Sincronizando o JsPlayer em primeiro plano");
            sync.syncJsPlayer();
        
    #Sincroniza o conteúdo
    thrSync = threading.Thread(target=sync.syncContent, args=(playerId,))
    thrSync.start();

    #Inicia e monitora a execução do player
    threading.Thread(target=watch.start).start()

    # Realiza a captura de tela e o envio ao servidor
    threading.Thread(target=util.sendScreenshot, args=(playerId,)).start()
    
    #Envia os logs para o servidor
    threading.Thread(target=sync.syncLogsView, args=(playerId,)).start()

else:
    print("ERRO! Player não cadastrado. Mac: "+util.getMac())
