import os.path
from ftplib import FTP

print('Conecting to FTP server . . . Please wait . . ')

localFile = "1532115391.mp4"
remoteFile = "1532115391.mp4"
remoteFolder = "2018-07"

#Estabelece a conexão
session = FTP('gnsignage.com.br','gnsignage','gnsignage1515')

#Seleciona o diretório
if remoteFolder in session.nlst():
    session.cwd(remoteFolder)

    #Verifica se o arquivo existe no diretório
    if remoteFile in session.nlst():

        # Checa o arquivo
        download = True
        if os.path.isfile(localFile):
            localFileSize = os.path.getsize(localFile)
            session.sendcmd("TYPE i")
            remoteFileSize = session.size(remoteFile)
            if localFileSize == remoteFileSize:
                download = False

        # Executa o download
        if download:
            print("Realizando o download do arquivo: "+localFile)
            #session.cwd(remoteFolder)
            session.retrbinary("RETR "+remoteFile, open(localFile, 'wb').write)
        else:
            print("Arquivo checado: " + localFile)

    else:
        print("Arquivo não encontrado: " + remoteFolder+"/"+remoteFile)
        if os.path.isfile(localFile):
            print("Removendo arquivo local: " +localFile)
            os.remove(localFile)
else:
    print("Diretório não encontrado: " + remoteFolder)

session.quit()