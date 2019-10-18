class Sync:
    
    #Sincroniza o JsPlayer
    def syncJsPlayer(self):
        import Constants;
        self.sync(Constants.FTP_JS_HOST,
                  Constants.FTP_JS_USER, Constants.FTP_JS_PASS,
                  "/", Constants.PATH_JSPLAYER);

        #Sincroniza as libs
        self.syncLibs();

    # Sincroniza as libs Html5
    def syncLibs(self):
        import Constants;
        import os;

        print("Sincronizando as libs");
        os.makedirs(Constants.PATH_CONTENT+"content/lib", mode=0o777, exist_ok=True);
        self.sync(Constants.FTP_CONTENT_HOST,
                  Constants.FTP_CONTENT_USER, Constants.FTP_CONTENT_PASS,
                  "/lib/", Constants.PATH_CONTENT+"content/lib");
        
    #Sincroniza o conteúdo
    def syncContent(self, playerId):
        import Constants;
        import os;
        import urllib3;
        import json;
        import ast;
        import shutil;
        import time;
        import threading
        from pathlib import Path;
        syncFoldersPairsStarted = False
        
        #Cria os diretórios
        os.makedirs(Constants.PATH_CONTENT, mode=0o777, exist_ok=True);
        os.makedirs(Constants.PATH_CONTENT+"content", mode=0o777, exist_ok=True);
        print("Diretórios de conteúdo criados");

        while True:
            print("Iniciando sincronia de midias")
            arrAccountsRunning = []

            #Atualiza o arquivo de dados json
            url = Constants.SERVER_API_DATA + playerId;
            http = urllib3.PoolManager();
            fileData = Constants.PATH_CONTENT+"data.json";
            print("Obtendo o arquivo de dados (data.json)");
            try:
                response = http.request('GET', url);
            except:
                print("Erro ao baixar o arquivo de dados");
            if response and response.data != "":
                #Grava o arquivo local
                objFile = open(fileData, 'w');
                respData = str(response.data);
                jsonContent = respData[2:-1];
                jsonContent = jsonContent.replace("\\\\", "\\");
                objFile.write(jsonContent);
                objFile.close();
                print("Arquivo de dados atualizado");

            #Realiza a leitura do arquivo json
            file = Path(fileData);
            files = [];
            medias = [];
            if file.exists():
                objFile = open(fileData, 'r');
                dataStr = objFile.read();
                objFile.close();
                if dataStr != "":
                    dataJson = json.loads(dataStr);

                    #Campanhas
                    if "campanhas" in dataJson:
                        for campanha in dataJson['campanhas']:
                            if "midias" in campanha:
                                for midia in campanha['midias']:
                                    if "arquivo" in midia:
                                        arquivo = midia['arquivo'].replace("./upload/midia/", "");
                                        if not arquivo in files:
                                            files.append(arquivo);
                                            medias.append(midia)

                    #Horário de funcionamento
                    if "player" in dataJson:
                        if "display" in dataJson['player']:
                            display = dataJson['player']['display']
                            if display['funcionamento_inicio'] != '00:00:00' or display['funcionamento_fim'] != '00:00:00':
                                if display['funcionamento_inicio'] != '' or display['funcionamento_fim'] != '':
                                    Constants.TIME_PLAYER_ON = display['funcionamento_inicio']
                                    Constants.TIME_PLAYER_OFF = display['funcionamento_fim']

                    #Sincroniza os diretórios e arquivos
                    for rmtMedia in medias:
                        self.syncMedia(rmtMedia)

                    #Remove as mídias que não são mais utilizadas
                    countFiles = len(files)
                    if countFiles > 0:
                        for dir in os.listdir(Constants.PATH_CONTENT+"content") :
                            if dir != "lib":
                                for subdir in os.listdir(Constants.PATH_CONTENT+"content/"+dir):
                                    realPath = Constants.PATH_CONTENT+"content/"+dir+"/"+subdir;
                                    midiaPath = dir+"/"+subdir;
                                    isDir = False;
                                    if os.path.isdir(realPath):
                                        isDir = True;
                                        midiaPath = midiaPath + "/";
                                    if not midiaPath in files:
                                        print("Removendo mídia: "+realPath);
                                        if not isDir:
                                            os.remove(realPath);
                                        else:
                                            shutil.rmtree(realPath);

                    #Sincroniza todos os pares de pastas
                    if "contas" in dataJson:
                        if syncFoldersPairsStarted == False:
                            syncFoldersPairsStarted = True
                            contas = dataJson['contas']
                            thrSync = threading.Thread(target=self.syncAllFoldersPairs, args=(contas,))
                            thrSync.start();

            #Aguarda por 15min
            time.sleep(900);
    
    #Sincroniza mídia
    def syncMedia(self, media):
        import Constants
        import Util
        import os
        util = Util.Util()
        
        #Extrai os caminhos da mídia
        mediaSrc = Constants.SERVER + media['arquivo'][2:]
        mediaDst = Constants.PATH_CONTENT + "content" + media['arquivo'][14:]
        
        #Arquivos
        if media['arquivo'][-1:] != "/":
            
            #Executa o download
            util.syncFileHttp(mediaSrc, mediaDst, int(media["tamanho"]), media["dt_modificacao"])
            
        #Pastas
        else:
            if "sub_arquivos" in media:
                for subFile in media['sub_arquivos']:
                    fileDst = Constants.PATH_CONTENT + "content" + subFile['src'][1:]
                    fileSrc = Constants.SERVER + "upload/midia" + subFile['src'][1:]
                    #Executa o download
                    util.syncFileHttp(fileSrc, fileDst, int(subFile["tamanho"]), subFile["dt_modificacao"])
    
    #Executa a sincronia
    def sync(self, host, user, password, src, dst):
        import os;

        if src[-1:] == "/":
            print("Sincronizando diretório: " + dst)
            command = 'sh ./sync.sh ';
            command += host + ' ' + user + ' ' + password + ' ';
            command += '"'+src+'" "'+dst+'"';
            os.system(command);
        else:
            self.syncFile(host, user, password, src, dst)

    # Sincroniza todos os pares de pastas
    def syncAllFoldersPairs(self, contas):
        import time
        try:
            for conta in contas:
                print("# Sincronizando conta FTP: "+conta["nome"])
                self.syncFolderPair(conta)
        except Exception as e:
            print(str(e))
            
        time.sleep(900)
        self.syncAllFoldersPairs(contas)

    # Sincroniza um par de pastas
    def syncFolderPair(self, conta):
        import os
        import Constants
        import time

        intervalo = int(conta["intervalo"])
        intervalo = intervalo * 60
        nome = conta["nome"]
        host = conta["host"]
        usuario = conta["usuario"]
        senha = conta["senha"]
        origem = conta["origem"]
        destino = conta["destino"]
        destino = destino.replace("C:\\3MIDIA\\", Constants.PATH_CLIENT_CONTENT)
        destino = destino.replace("\\", "/")

        #Ignora em caso de não preenchimento
        if (origem == "") or (destino == ""):
            return;

        #Cria os diretorios
        os.makedirs(destino, mode=0o777, exist_ok=True);
        
        #Executa
        self.sync(host, usuario, senha, origem, destino)

            #Aguarda até a próxima sincronia
            #time.sleep(300);

    # Executa a sincronia de um arquivo
    def syncFile(self, host, user, password, src, dst):
        from ftplib import FTP
        import os.path

        idx = src.rfind("/")+1
        fileName = src[idx:]
        idx = idx - 1
        remoteFolder = src[:idx]
        idx = dst.rfind("/");
        localFolder = dst[:idx];

        # Cria o diretório se não existir
        os.makedirs(localFolder, mode=0o777, exist_ok=True);

        # Estabelece a conexão
        session = FTP(host, user, password)

        # Seleciona o diretório
        if remoteFolder in session.nlst():
            session.cwd(remoteFolder)

            # Verifica se o arquivo existe no diretório
            if fileName in session.nlst():

                # Checa o arquivo
                download = True
                if os.path.isfile(dst):
                    localFileSize = os.path.getsize(dst)
                    session.sendcmd("TYPE i")
                    remoteFileSize = session.size(fileName)
                    if localFileSize == remoteFileSize:
                        download = False

                # Executa o download
                if download:
                    print("Realizando o download do arquivo: " + dst)
                    # session.cwd(remoteFolder)
                    session.retrbinary("RETR " + fileName, open(dst, 'wb').write)
                else:
                    print("Arquivo checado: " + dst)

            else:
                print("Arquivo não encontrado: " + remoteFolder + "/" + fileName)
                if os.path.isfile(dst):
                    print("Removendo arquivo local: " + dst)
                    os.remove(dst)
     
    # Sincroniza os logs com o servidor 
    def syncLogsView(self, playerId):
        import time
        import Constants
        import os
       
        while True:
            
            cmd = 'lftp -f "\n\
                set ftp:ssl-allow false\n\
                set ftp:use-feat false\n\
                set net:timeout 60\n\
                open '+Constants.FTP_LOGS_HOST+'\n\
                user '+Constants.FTP_LOGS_USER+' '+Constants.FTP_LOGS_PASS+'\n\
                lcd /var/www/html/GnPyPlayer\n\
                mirror -R --continue --verbose /var/www/html/gncontent/logs/log_view /log_view\n\
                bye\n\
                "'
            os.system(cmd)
            
            # Sincroniza os logs a cada 1 hora
            time.sleep(3600)
