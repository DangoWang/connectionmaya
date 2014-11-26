connectionmaya
==============


实时显示maya输出


    # -*- coding:utf-8 -*-
    import maya.cmds as cmds
    def commandport():
	    try:
	        cmds.commandPort(name=":7001", close=True)
	    except:
	        cmds.warning(
	            'Could not close port 7001 (maybe it is not opened yet...)')
	    try:
	        cmds.commandPort(name=":7002", close=True)
	    except:
	        cmds.warning(
	            'Could not close port 7002 (maybe it is not opened yet...)')

    # Open new ports
    cmds.commandPort(name=":7001", sourceType="mel")
    cmds.commandPort(name=":7002", sourceType="python")
    cmds.evalDeferred('commandport()')


================================================

上面 加到 userSetup.py里

快捷键是 Ctrl + F5 or Tools 菜单下 jonn_connectionToMaya

如果重起了sublime  Ctrl + F6 or Tools 菜单下 jonn_ReconnectionToMaya

jonn_ReconnectionToMaya 不可执行多次 

ctrl+` 显示sublime面板

================================================ 

[http://jonn.cnblogs.com/](http://jonn.cnblogs.com/)