# -*- coding:utf-8 -*-
from PyQt4 import QtCore
import usb.core
import usb.util
import time
from enum import __repr__

class Printer():
    def __init__(self):
        self.dev = None  # Сыллка на устройство печати
        self.printDevOut = None  # ссылка на канал вывода данных
        self.printDevIn = None  # ссылка на канал получения ответа от устройства
        self.reattach = False  # Флаг отключения системного драйвера порта
        self.command = None  # команда принтеру
        self.SEQ = 0x20  # Порядковый номер команды
        self._initial()  # инициализация устройства


    def sendCommand(self, command):
        print 'c ', command
        for b in command:
            print b
            self.printDevOut.write(b, 10)
            #time.sleep(0.1)
        #self.disconnectDev()

    def sync(self):
        packet = []
        packet.append('\x00')
        for i in range(1, 10):
            self.sendCommand(packet)
        #time.sleep(2)


    def _getAnswer(self):
        answer = self.printDevIn.read_all()
        print answer

    def ppp(self):
        for i in range(1, 10):
            self.printDevOut.write('\x00', 10)
        time.sleep(0.2)

        s= '\x01\x5A\x30\x30\x02\x41\x41\x1B\x30\x20\x20\x20\x20'
        s=s+'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x04'
        print '! ' ,s
        self.printDevOut.write(s, 10)
        '''
        time.sleep(0.2)
        for i in range(1, 10):
            self.printDevOut.write('\x00', 10)
        time.sleep(0.2)
        '''
        self.disconnectDev()



    def _initial(self):
        self._getPrintDevice()
        self.printDevOut, self.printDevIn = self._connectDev()
        if self.printDevOut == None or self.printDevIn == None:
            raise PrinterHardwareException(u'Printer endpoint setup error')

    def _getPrintDevice(self):  # получаем ссылку на устройство печати
        # ищем устройство по коду производителя и коду устройства
        self.dev = usb.core.find(idVendor=0x067b, idProduct=0x2303)
        # если устройство не найдено -
        if self.dev is None:
            raise PrinterHardwareException(u'Device not found')

            # Если устройство найдено, оключаем системный драйвер
        if self.dev.is_kernel_driver_active(0):
            self.reattach = True
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()

    def _connectDev(self):  # получаем ссылку на каналы вывода и получения данных
        # get an endpoint instance
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0, 0)]
        # получаем ссылку на канал вывода данных на печать
        epOut = usb.util.find_descriptor(
            intf,
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)

        # получаем ссылку на канал получения ответа от устройства печати
        epIn = usb.util.find_descriptor(
            intf,
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN)

        return epOut, epIn

    def disconnectDev(self):
        usb.util.dispose_resources(self.dev)  # освобождаем ресурсы устройства

        if self.reattach:  # подключаем системный драйвер обратно
            self.dev.attach_kernel_driver(0)

    # Exceptions


class PrinterHardwareException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return __repr__(self.value)