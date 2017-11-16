#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import sys
import traceback
import signal
from com import Printer

import LedDisplay as display
import RFConnector

if __name__ == "__main__":
    conn=None
    targetString="Hello, world!"

    com=Printer()

    try:
        d = display.display()                           #Экземпляр LED-панели
        dm = display.LedDisplayMode()                   #Режим вывода теста
        lc=display.LedColor()
        signal.signal(signal.SIGHUP, d.signal_handler)
    except:
        print 'Display initialization error'
        time.sleep(5)
        sys.exit(1)

    try:
        #Получение строки байт в формате альфа-протокола для отправки на ноду
        messageClear=d.prepareMessageClear(None, None)
        message1=d.prepareMessage(dm.HOLD, lc.RED+targetString)
        message2=d.prepareMessage2(None, None)
    except SystemExit:
        print('exiting')
        raise
    except:
        print("CRASH: " + str(sys.exc_info()[0]))
        tb = traceback.format_exc()
        print(tb)
        time.sleep(5)

    #Отправляем строку байт на ноду
    #conn.sendMessage(message)
    com.ppp()


    print 'Sync '
    #com.sync()

    print 'Out message: ', messageClear
    #com.sendCommand(messageClear)
    #time.sleep(2)

#    com.disconnectDev()
    '''
    print 'Out message: ', message1
    com.sendCommand(message1)
    time.sleep(1)
    
    print 'Out message: ', message2
    com.sendCommand(message2)
    '''



