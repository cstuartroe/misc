import os
import signal
import time
from subprocess import Popen

running = True

while running:
    p = Popen(r'~/Desktop/pianoteq_linux_trial_v673/Pianoteq\ 6/amd64/Pianoteq\ 6', shell=True, preexec_fn=os.setsid)
    try:
        time.sleep(1200)
    except KeyboardInterrupt:
        running = False
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
