import os
import time
import psutil
import Util

class Watch:
    def start(self):
        util = Util.Util()
        print("Monitoramento iniciado (GnWatch)")

        while True:

            #Verifica se o player está em execução
            opened = False
            for pid in psutil.pids():
                p = psutil.Process(pid)
                print(p.name())
                #if p.name() == "chrome":
                if "chromium-browser" in p.name():
                    opened = True
                    break

            if not opened:
                util.startPlayer()

            time.sleep(60)
