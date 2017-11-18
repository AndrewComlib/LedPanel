# -*- coding: utf8 -*-

import sys
from time import sleep
from snapconnect import snap

SERIAL_TYPE = snap.SERIAL_TYPE_RS232

class BridgeVersionClient(object):

    def __init__(self, path, nodeAddress, message):
        print 'init conn2'
        self.path=path
        self.nodeAddress=nodeAddress
        self.message=message
        #Создаем экземпляр SnapConnect
        self.comm = snap.Snap(funcs = {'reportLightState': self.start})

        self.comm.set_hook(snap.hooks.HOOK_SNAPCOM_OPENED, self.hook_open)
        self.comm.set_hook(snap.hooks.HOOK_SNAPCOM_CLOSED, self.hook_closed)
        #self.comm.set_hook(snap.hooks.HOOK_10MS, self.make_poll)

        self.comm.loop()

    def start(self, m):
        print 'm'
        self.comm.poll()

    def make_poll(self):
        self.comm.poll()

    def hook_open(*args):
        print "SNAPCOM OPENED: %r" % (args,)
        print 'open'

    def hook_closed(*args):
        print "SNAPCOM CLOSED: %r" % (args,)
        print  'closed'


    def sendMessage(self, packet):
        # Открываем последовательный порт по заданному пути
        self.comm.open_serial(SERIAL_TYPE, self.path)
        #Отправляем сообщение на ноду через RPC

        for message in packet:
            self._prnstr(message)
            a=self.comm.rpc(self.nodeAddress, 'writePacket', message)
            print 'snap ', a
            self.comm.poll()
            sleep(1)
        #self.comm.poll()
        self.comm.loop()

    #self.comm.set_hook(snap.hooks.HOOK_RPC_SENT)
    #snap.Snap.set_hook(snap.hooks.HOOK_RPC_SENT)
    #def a(self, p1, p2):
        #print 'hook ', p1, p2

        #self.comm.loop()
        #for b in message:
        #    self.comm.rpc(self.nodeAddress, 'sendPacket', b, 200)

        #    self.comm.poll()
        #    sleep(0.3)
        #self.comm.loop()
        #self.stop()


    def clearScreen(self):
        # Открываем последовательный порт по заданному пути
        self.comm.open_serial(SERIAL_TYPE, self.path)
        #Отправляем сообщение на ноду через RPC
        print 'sending clear'
        self.comm.rpc(self.nodeAddress, 'clear1')
        #self.comm.poll()
        self.comm.loop()
        #sleep(2)

        #self.stop()

    def stop(self):
        """Stop the SNAPconnect instance."""
        print 'closing'
        self.comm.close_all_serial()  # Close all serial connections opened with SNAPconnect
        print 'closed'
        sys.exit(0)  # Exit the program


    def _prnstr(self, outstr):
        print outstr
        for i in range (0, len(outstr)):#st in outstr:
            st=outstr[i]
            newLabel = ord(st)
            h=hex(newLabel)
            hh=(h[2:])
            if len(hh)<2:
                hh='0'+hh
            p=hh.decode('hex')
            s='n'
            if p=='\x00':
                s='0'
            elif p=='\x01':
               s='SOH'
            elif p=='\x02':
                s='STX'
            elif p=='\x41':
                s='WTF'
            elif p=='\x1B':
                s='1B'
            elif p=='\x30':
                s='DisP:0'
            elif p=='\x20':
                s='20'
            elif p=='\x45':
                s='WrSpecFunk'
            elif p=='\x24':
                s='ClearMem'
            elif p=='\x55':
                s='IR'
            elif p=='\x04':
                s='EOT'
            elif p=='\x1C':
                s='setColor'

            s=s+' | '
            print s,