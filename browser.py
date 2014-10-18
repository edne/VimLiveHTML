from sys import argv, exit
import webkit, gtk
from threading import Thread
from multiprocessing.connection import Listener, Client

class Receiver(Thread):
    def __init__(self, browser):
        self.browser = browser
        Thread.__init__(self)

        self.cbs = {
            'close': self.browser.stop,
            'refresh': self.browser.refresh
        }

        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            address = ('localhost', 6000)
            conn = Client(address)
            msg = conn.recv()
            conn.close()

            [cb() for k,cb in self.cbs.items() if msg==k]


class Browser(object):
    def __init__(self):
        self.web = webkit.WebView()
        self.web.open(argv[-1])

        win = gtk.Window()
        win.connect('destroy', self.stop)
        scroller = gtk.ScrolledWindow()
        win.add(scroller)
        scroller.add(self.web)
        win.show_all()

        self.receiver = Receiver(self)

    def stop(self, stuff=None):
        gtk.main_quit()
        self.receiver.stop()

    def run(self):
        self.receiver.start()
        gtk.main()

    def refresh(self):
        self.web.reload()


def send(msg):
    address = ('localhost', 6000)
    listener = Listener(address)
    conn = listener.accept()
    conn.send(msg)

    conn.close()
    listener.close()

if 'start' in argv:
    Browser().run()

if 'close' in argv:
    send('close')
if 'refresh' in argv:
    send('refresh')
