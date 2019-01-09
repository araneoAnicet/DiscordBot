import subprocess as sp
from time import sleep
reconnection_time = 20


while True:
    try:
        sp.call('python main.py', shell=True)
    except:
        sleep(reconnection_time)
        continue
