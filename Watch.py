import os
import time
import psutil
import Util

class Watch:
    firstAccess = True

    def start(self):
        import Constants
        import datetime
        import threading

        util = Util.Util()
        print("Monitoramento iniciado (GnWatch)")
        time.sleep(10)
        SCREEN_ON = True

        while True:
           
            #Verifica se está dentro do horário de funcionamento            
            now = datetime.datetime.now()
            if now.hour < 10:
                hourNow = "0"+str(now.hour)
            else:
                hourNow = str(now.hour)
            if now.minute < 10:
                hourMin = "0"+str(now.minute)
            else:
                hourMin = str(now.minute)
            currentHour = hourNow+hourMin+"00"
            currentHour = int(currentHour)
            onTime = True

            #Verifica se foi especificado horários de início e fim
            if Constants.TIME_PLAYER_ON != "" and Constants.TIME_PLAYER_OFF != "":

                timeOn = int(Constants.TIME_PLAYER_ON.replace(":", ""))
                timeOff = int(Constants.TIME_PLAYER_OFF.replace(":", ""))
                
                #Início antes do fim
                if timeOff > timeOn:
                    if timeOn > currentHour or timeOff < currentHour:
                        onTime = False
                        
                else: #Fim antes do início
                    if currentHour > timeOff and currentHour < timeOn:
                        onTime = False
                        
                if onTime == False:
                    print("Fora do horário de funcionamento: "+Constants.TIME_PLAYER_ON+" - "+Constants.TIME_PLAYER_OFF)
                    onTime = False
                    util.closeApp()
                    SCREEN_ON = False
                    #Desliga o monitor
                    util.screenOff()

            #Verifica se está dentro do período de exibição do player
            if onTime:
                if SCREEN_ON == False:
                    util.reboot()

                #Liga a tela
                util.screenOn()

                #Verifica se o modo de persistência está ativo
                keepOpened = util.getPreferences("keep-opened")
                if keepOpened != "False" or Watch.firstAccess == True:

                    #Verifica se o player está em execução
                    import Socket
                    print("Tempo de ociosidade: " + str(Socket.lastPing) + "s")
                    if Socket.lastPing > 240 or Watch.firstAccess == True:
                        threading.Thread(target=util.startPlayer).start()

                    Watch.firstAccess = False

            time.sleep(30)
