class Util:
    
    #Obtém a autorização
    def getAuth(self):
        import Constants;
        import urllib3;
        import json;
        import Util;
        util = Util.Util();
        objJson = {};
        mac = self.getMac();
        url = Constants.SERVER_API_AUTH + mac + "&version=" + str(Constants.VERSION);
        print("Obtendo autorização: "+url);
        http = urllib3.PoolManager(retries=False);
        try:
            response = http.request('GET', url);
            objJson = json.loads(response.data.decode('utf-8'));
            objJson['online'] = True
        except Exception as e:
            print("Falha na conexão");
            print(str(e));
            #Tenta obter o id local
            playerId = util.getPreferences("id_player");
            objJson['id'] = playerId;
            objJson['auth'] = 'allow';
            objJson['online'] = False

        #Verifica o segundo servidor
        if Constants.SERVER != Constants.SERVER2:
            if objJson['auth'] == 'deny':
                self.changeServer();
                objJson = self.getAuth()

        return objJson;
    
    #Obtém o macaddress
    def getMac(self):
        import netifaces;
        interfaces = netifaces.interfaces();
        deviceInfo = netifaces.ifaddresses(interfaces[1]);
        return deviceInfo[netifaces.AF_LINK][0]['addr'];
    
    #Registra valores na máquina
    def setPreferences(self, key, value):
        import Constants;
        import json;
        from pathlib import Path;
        filePreferences = Constants.PATH_CONTENT + "preferences.json";
        fileContent = "";
        file = Path(filePreferences);
            
        #Carrega um arquivo
        if file.exists():
            objFile = open(filePreferences, 'r');
            fileContent = objFile.read();
            objFile.close();
            
        if fileContent == '':
            fileContent = "{}";

        #Sobrescreve o atributo
        fileContent = fileContent.replace("'", '"')
        objJson = json.loads(fileContent);
        objFile = open(filePreferences, 'w');
        objJson[key] = value;
        objFile.write(str(objJson));
        objFile.close();
        
    #Recupera valores na máquina
    def getPreferences(self, key):
        import Constants;
        import json;
        from pathlib import Path;
        filePreferences = Constants.PATH_CONTENT + "preferences.json";
        fileContent = "";
        file = Path(filePreferences);
            
        #Carrega um arquivo
        if file.exists():
            objFile = open(filePreferences, 'r');
            fileContent = objFile.read();
            objFile.close();
            if fileContent != '':
                objJson = json.loads(fileContent.replace("'", '"'));
                if key in objJson:
                    return objJson[key];

        return "";

    #Carrega o player
    def startPlayer(self):
        import os
        import Constants

        # Fecha o browser caso ja esteja aberto
        self.closeApp()

        # Inicia o browser
        print("Iniciando o browser")
        os.system(Constants.COMMAND_START_PLAYER)

    # Reinicia o player
    def reboot(self):
        import os
        os.system("reboot")

    #Move o cursor para o canto da tela
    def hideCursor(self):
        import time
        import pyautogui

        pyautogui.FAILSAFE = False

        for x in range(1350, 1360):
            pyautogui.moveTo(x, x)

    #Envia o ping para o servidor
    def pingServer(self, playerId):
        import time
        import Util
        import urllib3
        import Constants
        util = Util.Util()

        while True:
            url = Constants.SERVER_API_PING + str(playerId)
            print("Mantendo a comunicação com o servidor (status = on): " + url)
            http = urllib3.PoolManager(retries=False)
            try:
                response = http.request('GET', url);
            except:
                print("Falha no envio do ping");

            time.sleep(60)

    #Tira prints da tela
    def sendScreenshot(self, playerId):
        import time
        import os
        import Constants
        import requests

        while True:
            time.sleep(600)
            try:
                #Captura a tela
                image = Constants.PATH_CONTENT + "screenshot.jpg"
                os.system("scrot " + image)

                #Envia ao servidor
                url = Constants.SERVER_API_UPLOAD_SCREENSHOT + playerId
                files = {'media': open(image, 'rb')}
                requests.post(url, files=files)
            except Exception as e:
                print("Falha no envio de screenshot");
                print(str(e));
            
    #Encerra o player
    def closeApp(self):
        import psutil

        try:
            #Encerra o aplicativo
            for proc in psutil.process_iter():
                if "chromium" in proc.name():
                    proc.kill()
        except Exception as e:
            print("Falha ao encerrar o player");

    #Verifica se é um Raspberry
    def isOsRaspbian(self):
        file = open("/etc/os-release", "r")
        contentFile = file.read()
        if "Raspbian" in contentFile or "bionic" in contentFile:
            return True
        else:
            return False

    #Desliga o monitor
    def screenOff(self):
        import os
        if self.isOsRaspbian():
            os.system("vcgencmd display_power 0")

    #Liga o monitor
    def screenOn(self):
        import os
        if self.isOsRaspbian():
            os.system("vcgencmd display_power 1")

    #Reinicia a máquina
    def reboot(self):
        import os
        os.system("reboot")

    #Registra a versão na máquina
    def registerVersion(self):
        import Constants
        file = open(Constants.PATH_VERSION, "w+")
        file.write(str(Constants.VERSION))
        file.close()

    #Troca o servidor
    def changeServer(self):
        import Constants
        Constants.SERVER = Constants.SERVER2
        Constants.SERVER_URL = Constants.SERVER + "downloads/gnpyplayer/version.txt"
        Constants.SERVER_API_AUTH = Constants.SERVER + "api/get-authorization?linux=true&mac=";
        Constants.SERVER_API_DATA = Constants.SERVER + "api/get-player-content/?id_player="
        Constants.SERVER_API_PING = Constants.SERVER + "api/ping/?id_player="
        Constants.SERVER_API_UPLOAD_SCREENSHOT = Constants.SERVER + "api/send-screenshot/id_player/"
        Constants.FTP_JS_HOST = 'plux.gnsignage.com.br';
        Constants.FTP_CONTENT_HOST = Constants.FTP_JS_HOST;

    #Sincroniza um arquivo via HTTP
    def syncFileHttp(self, src, dst, fileSize, fileUpdate):
        import Constants
        import os
        import urllib.request
        from urllib.parse import urlparse
        download = True
        
        try:
        
            #Verifica se o arquivo já existe
            if os.path.isfile(dst):
                info = os.stat(dst);
                #Compara o tamanho
                if int(fileSize) == int(info.st_size):
                    #Compara a data de modificação
                    if int(fileUpdate) < info.st_mtime:
                        download = False
                        
            #Trata a url
            params = src.split("/")
            src = "";
            count = 0
            for param in params:
                if count > 1:
                    src = src + urllib.parse.quote(param) + "/"
                else:
                    src = src + param + "/"
                count = count + 1
            src = src[:-1]
                        
            #Download
            if download:
                print("Realizando o download via HTTP: " + src)
                #Remove o arquivo antigo
                if os.path.isfile(dst):
                    os.remove(dst)
                #Cria o diretório
                idx = dst.rfind('/')+1
                if os.path.isdir(dst[:idx]) != True:
                    os.makedirs(dst[:idx])
                #Download HTTP
                urllib.request.urlretrieve(src, dst)
                
        except:
                print("Falha no download (HTTP) do arquivo: "+src);
