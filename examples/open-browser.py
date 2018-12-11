import subprocess

#command = "chromium-browser"
command = "google-chrome"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()
print(process.returncode)

print("OK")