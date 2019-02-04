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
            print("Enviando ping: " + url)
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

            #Captura a tela
            image = Constants.PATH_CONTENT + "screenshot.jpg"
            os.system("scrot " + image)

            #Envia ao servidor
            url = Constants.SERVER_API_UPLOAD_SCREENSHOT + playerId
            files = {'media': open(image, 'rb')}
            requests.post(url, files=files)

            time.sleep(600)

    #Encerra o player
    def closeApp(self):
        import psutil

        #Encerra o aplicativo
        for proc in psutil.process_iter():
            if "chromium" in proc.name():
                proc.kill()

    #Verifica se é um Raspberry
    def isOsRaspbian(self):
        file = open("/etc/os-release", "r")
        contentFile = file.read()
        if "Raspbian" in contentFile:
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
