import os
import time
import psutil
import Util

class Watch:
    firstAccess = True

    def start(self):
        util = Util.Util()
        print("Monitoramento iniciado (GnWatch)")
        time.sleep(10)

        while True:

            #Verifica se está dentro do horário de funcionamento
            import Constants
            import datetime
            import threading
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
            if Constants.TIME_PLAYER_ON != "" and Constants.TIME_PLAYER_OFF != "":

                timeOn = int(Constants.TIME_PLAYER_ON.replace(":", ""))
                timeOff = int(Constants.TIME_PLAYER_OFF.replace(":", ""))
                if timeOn > currentHour or timeOff < currentHour:
                    print("Fora do horário de funcionamento: "+Constants.TIME_PLAYER_ON+" - "+Constants.TIME_PLAYER_OFF)
                    onTime = False
                    util.closeApp()
                    #Desliga o monitor
                    util.screenOff()

            #Verifica se está dentro do período de exibição do player
            if onTime:
                util.screenOn()

                #Verifica se o modo de persistência está ativo
                keepOpened = util.getPreferences("keep-opened")
                if keepOpened != "False" or Watch.firstAccess == True:

                    #Verifica se o player está em execução
                    import Socket
                    if Socket.lastPing > 200 or Watch.firstAccess == True:
                        threading.Thread(target=util.startPlayer).start()

                    Watch.firstAccess = False

            time.sleep(60)
