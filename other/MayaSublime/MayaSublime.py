# ST2/ST3 compat
from __future__ import print_function
import threading
import os
import re
import sys
import time
import textwrap
import sublime
import sublime_plugin
from telnetlib import Telnet
if sublime.version() < '3000':
    # we are on ST2 and Python 2.X
    _ST3 = False
else:
    _ST3 = True

# Our default plugin settings
_settings = {
    'host': '127.0.0.1',
    'mel_port': 7001,
    'py_port': 7002
}




'''
view.run_command('gtimer')
view.run_command('gtimerpause')
'''
"""
class gtimerCommand(sublime_plugin.TextCommand):    
    def run(self, edit):
        global message
        message = .1
        start_spinner(message)

class gtimerpauseCommand(sublime_plugin.TextCommand):    
    def run(self, edit):         
        stop_all_spinners()
class Spinner(threading.Thread):
    def __init__(self, message):
        threading.Thread.__init__(self)
        self.message = message
        self.spin = True
    
    def stop(self):
        self.spin = False
    
    def run(self):
        while self.spin:
            sublime.set_timeout(write_time,1)
            time.sleep(message)

spinner_lock = threading.Lock()
active_spinners = []

def start_spinner(message):
    global active_spinners, spinner_lock
    spinner_lock.acquire()
    
    spinner = Spinner(message)
    spinner.start()
    active_spinners.append(spinner)
    
    spinner_lock.release()
    return spinner

def stop_spinner(spinner):
    global active_spinners, spinner_lock
    spinner_lock.acquire()
    
    spinner.stop()
    if spinner in active_spinners:
        active_spinners.remove(spinner)
    
    spinner_lock.release()

def stop_all_spinners():
    global active_spinners, spinner_lock
    spinner_lock.acquire()
    
    for spinner in active_spinners:
        spinner.stop()
    active_spinners = []
    
    spinner_lock.release()

size=0
def write_time():
    global size
    file_object = open(r'C:/myScriptEditorLog.txt')
    try:
        
        text = file_object.read()
        if size != len(text):
            print (text)
        size = len(text)
    finally:
        file_object.close()

"""

class send_to_mayaCommand(sublime_plugin.TextCommand):
    PY_CMD_TEMPLATE = textwrap.dedent('''
        import traceback
        import __main__

        namespace = __main__.__dict__.get('_sublime_SendToMaya_plugin')
        if not namespace:
            namespace = __main__.__dict__.copy()
            __main__.__dict__['_sublime_SendToMaya_plugin'] = namespace

        namespace['__file__'] = {2!r}

        try:
            {0}({1!r}, namespace, namespace)
        except:
            traceback.print_exc() 
    ''')
    RX_COMMENT = re.compile(r'^\s*(//|#)')

    def run(self, edit):
        syntax = self.view.settings().get('syntax')
        if re.search(r'python', syntax, re.I):
            lang = 'python'
            sep = '\n'
        elif re.search(r'mel', syntax, re.I):
            lang = 'mel'
            sep = '\r'
        else:
            print('No Maya-Recognized Language Found')
            return
        isPython = (lang == 'python')
        if _ST3 and _settings['host'] == None:
            sync_settings()
        host = _settings['host']
        port = _settings[
            'py_port'] if lang == 'python' else _settings['mel_port']
        selections = self.view.sel()  # Returns type sublime.RegionSet
        selSize = 0
        for sel in selections:
            if not sel.empty():
                selSize += 1
        snips = []
        if selSize == 0:
            execType = 'execfile'
            print("Nothing Selected, Attempting to exec entire file")
            if self.view.is_dirty():
                sublime.error_message("Save Changes Before Maya Source/Import")
                return
            file_path = self.view.file_name()
            if file_path is None:
                sublime.error_message(
                    "File must be saved before sending to Maya")
                return
            plat = sublime_plugin.sys.platform
            if plat == 'win32':
                file_path = file_path.replace('\\', '\\\\')
                print("FILE PATH:", file_path)

            if lang == 'python':
                snips.append(file_path)
            else:
                snips.append('rehash; source "{0}";'.format(file_path))
        else:
            execType = 'exec'
            file_path = ''
            substr = self.view.substr
            match = self.RX_COMMENT.match
            for sel in selections:
                snips.extend(
                    line for line in substr(sel).splitlines() if not match(line))
        mCmd = str(sep.join(snips))
        if not mCmd:
            return
        print('Sending {0}:\n{1!r}\n...'.format(lang, mCmd[:200]))
        if lang == 'python':
            mCmd = self.PY_CMD_TEMPLATE.format(execType, mCmd, file_path)
        c = None
        try:
            c = Telnet(host, int(port), timeout=3)
            if _ST3:
                c.write(mCmd.encode(encoding='UTF-8'))
            else:
                c.write(mCmd)
        except Exception:
            e = sys.exc_info()[1]
            err = str(e)
            sublime.error_message(
                "Failed to communicate with Maya (%(host)s:%(port)s)):\n%(err)s" % locals(
                )
            )
            raise
        else:
            time.sleep(.1)

        finally:
            if c is not None:
                c.close()


def settings_obj():
    return sublime.load_settings("MayaSublime.sublime-settings")


def sync_settings():
    global _settings
    so = settings_obj()
    _settings['host'] = so.get('maya_hostname')
    _settings['py_port'] = so.get('python_command_port')
    _settings['mel_port'] = so.get('mel_command_port')
settings_obj().clear_on_change("MayaSublime.settings")
settings_obj().add_on_change("MayaSublime.settings", sync_settings)
sync_settings()


'''
scriptEditorInfo -e -wh 1 -chf -hfn "";
scriptEditorInfo -wh 1 -historyFilename "C:/myScriptEditorLog.txt";
'''
