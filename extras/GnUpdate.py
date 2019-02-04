#Realiza a atualização do GnPyPlayer
import os
import urllib.request

URL_SERVER = "http://gnsignage.com.br/"
URL_VERSION = URL_SERVER + "downloads/gnpyplayer/version.txt"
PATH_FILE_VERSION = "/var/www/html/gncontent/version.txt"
TO_UPDATE = True

#Verifica a versão do servidor
REMOTE_VERSION = 0.0
contents = ""
try:
    print("Verificando se há atualizações")
    contents = urllib.request.urlopen(URL_VERSION).read()
    if contents != "":
        contents = str(contents).replace("'", "").replace("b", "")
        REMOTE_VERSION = float(contents)

    #Verifica a versão local
    if REMOTE_VERSION > 0.0:
        if os.path.exists(PATH_FILE_VERSION):
            localContent = open(PATH_FILE_VERSION, "r")
            strLocalContent = str(localContent.read()).replace("\n", "")
            LOCAL_VERSION = float(strLocalContent)
            if LOCAL_VERSION >= REMOTE_VERSION:
                TO_UPDATE = False

    #Executa a sincronia
    if TO_UPDATE:
        command = 'lftp -f "\n'
        command += 'open gnsignage.com.br\n'
        command += 'user gnpyplayer gnpyplayer1515\n'
        command += 'lcd /var/www/html/GnPyPlayer\n'
        command += 'mirror --continue --delete --verbose / /var/www/html/GnPyPlayer\n'
        command += 'bye\n'
        command += '"'
        os.system(command)    
   
except:
    print("Não foi possível atualizar o GnPyPlayer. Sem conexão")

#Executa o player
os.system("gnome-terminal -e 'bash -c \"cd /var/www/html/GnPyPlayer && python3 __init__.py\"'")
