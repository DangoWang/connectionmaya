# -*- coding:utf-8 -*-
'''
     _   _____   __   _   __   _  
    | | /  _  \ |  \ | | |  \ | |     
    | | | | | | |   \| | |   \| |     
 _  | | | | | | | |\   | | |\   |     
| |_| | | |_| | | | \  | | | \  |     
\_____/ \_____/ |_|  \_| |_|  \_|     
'''
'''
CALLBACK_ID = MCommandMessage.addCommandOutputFilterCallback(writeToTerminal)
def writeToTerminal(msg, msgType, filterOutput, clientData):
    MScriptUtil.setBool(filterOutput, True)
'''

import sys
import socket
import maya.OpenMaya as OpenMaya
CALLBACK_ID = None
ID = ''


def createCallback():
    #import sys
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    global CALLBACK_ID
    global ID
    if CALLBACK_ID is None:
        ID = OpenMaya.MCommandMessage.addCommandOutputCallback(cmdCallback, '')
        sys.stdout.write('>> starting...\n')
        CALLBACK_ID = True
    else:
        sys.stdout.write('>> fucking...\n')

def cmdCallback(msg, msgType, data):
    global ID
    line = str(msg)
    if msgType == OpenMaya.MCommandMessage.kWarning:
        line = '# Warning: %s #\n' % line
    elif msgType == OpenMaya.MCommandMessage.kError:
        line = '// Error: %s //\n' % line
    elif msgType == OpenMaya.MCommandMessage.kResult:
        line = '# Result: %s #\n' % line
    host = 'localhost'
    port = 6000
    message = line
    try:
        maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        maya.connect((host, port))
        maya.send(message.encode('utf-8'))
    except:
        OpenMaya.MMessage.removeCallback(ID)
        #raise Exception, 'Connection Failed To : %s:%s' % (host, port)
    finally:
        maya.close()
