import time
import pyautogui

pyautogui.FAILSAFE = False

for x in range(1350, 1360):
    pyautogui.moveTo(x, x)