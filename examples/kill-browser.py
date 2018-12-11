import subprocess
import signal
import os

#processName = "chromium"
processName = "chrome"
proc = subprocess.Popen(["pgrep", processName], stdout=subprocess.PIPE)
for pid in proc.stdout:
    os.kill(int(pid), signal.SIGTERM)
    try: 
        os.kill(int(pid), 0)
    except OSError as ex:
        continue

print("OK")