
# -*- coding:utf-8 -*-
'''
     _   _____   __   _   __   _  
    | | /  _  \ |  \ | | |  \ | |     
    | | | | | | |   \| | |   \| |     
 _  | | | | | | | |\   | | |\   |     
| |_| | | |_| | | | \  | | | \  |     
\_____/ \_____/ |_|  \_| |_|  \_|     
'''
import sublime
import sublime_plugin
import os
import socket
import time
import sys
import threading
CALLBACK = None
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
Path = os.path.join(BASE_PATH, 'code').replace('\\', '/')

class connectionmayaCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global CALLBACK
        if CALLBACK is None:
            print "connect"
            CALLBACK = starting()
            CALLBACK.start()
            mayaSocket()
            CALLBACK = True
        else:
            # CALLBACK.stop()
            # CALLBACK=None
            mayaSocket()
            print "done"
class reconnectionmayaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        mayaSocketA()
class starting(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.spin = True
        port = 6000
        host = 'localhost'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((host, port))
        except:
            print "Tried to open port %s, but failed:  It's probably already open\n" % port
            return
        self.s.listen(5)

    def stop(self):
        try:
            self.spin = False
        except:
            pass

    def run(self):
        while self.spin:
            self.client, address = self.s.accept()
            data = self.client.recv(4096)
            if data:
                print (data.decode("utf8"))
            sublime.set_timeout(notify, 1)
            time.sleep(.1)
            self.client.close()


def notify():
    pass


def mayaSocket():
    host = 'localhost'
    port = 7001
    date = 'python("import sys;sys.path.append(\'%s\');import execmaya;execmaya.createCallback()")' % Path
    try:
        maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = maya.connect((host, port))
        if conn == None:
            # maya.send('python("execfile(\'%s\');createCallback()")'%Path)
            maya.send(date)
        #data = maya.recv(4096)
        # if data:
        #     print (data.decode("utf8"))
    except:
        raise Exception, 'Connection Failed To : %s:%s' % (host, port)
    finally:
        maya.close()

def mayaSocketA():
    host = 'localhost'
    port = 7001
    date = 'python("import sys;sys.path.append(\'%s\');import execmaya;reload(execmaya);execmaya.createCallback()")' % Path
    try:
        maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = maya.connect((host, port))
        if conn == None:
            # maya.send('python("execfile(\'%s\');createCallback()")'%Path)
            maya.send(date)
        #data = maya.recv(4096)
        # if data:
        #     print (data.decode("utf8"))
    except:
        raise Exception, 'Connection Failed To : %s:%s' % (host, port)
    finally:
        maya.close()
# view.run_command('connectionmaya')
