class Util:
    
    #Obtém a autorização
    def getAuth(self):
        import Constants;
        import urllib3;
        import json;
        import Util;
        constants = Constants.Constants();
        util = Util.Util();
        objJson = {};
        
        mac = self.getMac();
        url = constants.SERVER_API_AUTH + mac;
        print("Obtendo autorização: "+url);
        http = urllib3.PoolManager();
        try:
            response = http.request('GET', url);
            objJson = json.loads(response.data);
        except:
            print("Falha na conexão");
            #Tenta obter o id local
            playerId = util.getPreferences("id_player");
            objJson['id'] = playerId;
            objJson['auth'] = 'allow';
            
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
        constants = Constants.Constants();
        filePreferences = constants.PATH_CONTENT + "preferences.json";
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
        constants = Constants.Constants();
        filePreferences = constants.PATH_CONTENT + "preferences.json";
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

        # Inicia o browser
        print("Iniciando o browser")
        #os.system("chromium-browser --kiosk --no-sandbox --app=\"http://localhost/jsplayer/index-linux.html\"")
        os.system("chromium-browser --kiosk --no-sandbox --load-and-launch-app=/var/www/html/chrome-ext")

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
        constants = Constants.Constants();

        while True:
            url = constants.SERVER_API_PING + str(playerId)
            print("Enviando ping: " + url)
            http = urllib3.PoolManager()
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
        constants = Constants.Constants()

        while True:

            #Captura a tela
            image = constants.PATH_CONTENT + "screenshot.jpg"
            os.system("scrot " + image)

            #Envia ao servidor
            url = constants.SERVER_API_UPLOAD_SCREENSHOT + playerId
            files = {'media': open(image, 'rb')}
            requests.post(url, files=files)

            time.sleep(600)
