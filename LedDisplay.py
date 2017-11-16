# -*- coding: utf8 -*-

import serial
import random
import sys
from struct import pack, unpack

class display:

    def __init__(self):
        self.ledInit()
        self.panelAddress = ['Z00',]
        self.SOH='\x01'
        self.STX='\x02'
        self.currentFileLabel='\x41'
        self.EOT='\x04'
        self.SYNC='\x00'*10


    def ledInit(self):
        global ledSerialPort
        ledSerialPort = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

    def prepareMessage(self, message):
        packet = ''
        #Clearing the display
        packet += self._getMessageBlankDisplay()

        #Adding sync bytes
        packet += self.SYNC
        #Add packet prefix
        packet += self._getPrefix(message)
        #Encode strings and add them to acket
        strArray=message[::-1]      #Invert list of strings
        for string in strArray:
            packet += self._getEncodedString(string)
        #Add packet suffix
        packet += self._getSuffix(message)
        #self._prnstr(packet)#####################################
        return packet

    def _getMessageBlankDisplay(self):
        outString=''
        outString += self.SYNC
        outString += self.SOH

        for address in self.panelAddress:
            outString += address

        outString += self.STX

        outString += spetialFunction.WRITE_TEXT_FILE

        outString += self.currentFileLabel
        #self.labelNextFile +=1

        outString += '\x1B'

        outString += spetialFunction.DISPLAY_POSITION_FILL

        outString += '\x20'*10

        outString += self.EOT
        return outString


    def _getPrefix(self, message):
        outString =''
        outString += self.SOH

        for address in self.panelAddress:
            outString += address

        outString += self.STX

        outString += spetialFunction.WRITE_SPEC_FUNC
        outString += spetialFunction.CLEAR_MEMORY
        q=len(message)
        for i in range (0, len(message)):
            outString += self.currentFileLabel
            newLabel=ord(self.currentFileLabel)+1
            self.currentFileLabel=(hex(newLabel)[2:]).decode('hex')

            outString += '\x41'    #type 'text file'

            outString += spetialFunction.IR_ACCESIBLE

            outString += '\x30\x33\x45\x38'
            outString += '\x46\x46\x46\x46'

        outString += self.EOT
        return outString

    def _getEncodedString(self, sourseString):
        outString = ''
        outString += self.SOH

        for address in self.panelAddress:
            outString += address

        outString += self.STX

        outString += spetialFunction.WRITE_TEXT_FILE

        outString += self.currentFileLabel

        newLabel = ord(self.currentFileLabel) - 1
        self.currentFileLabel = (hex(newLabel)[2:]).decode('hex')

        outString += '\x1B'

        outString += spetialFunction.DISPLAY_POSITION_FILL

        outString += sourseString[1]

        outString += spetialFunction.SET_COLOR

        outString += sourseString[2]

        outString += sourseString[0]

        outString += self.EOT

        return outString

    def _getSuffix(self, message):
        outString = ''
        outString += self.SOH
        for address in self.panelAddress:
            outString += address
        outString += spetialFunction.WRITE_SPEC_FUNC
        outString += '\x2E\x53'
        outString += spetialFunction.IR_ACCESIBLE
        for label in message:
            outString += self.currentFileLabel
            newLabel=ord(self.currentFileLabel)+1
            self.currentFileLabel=(hex(newLabel)[2:]).decode('hex')
        outString += self.EOT

        return outString

    def _prnstr(self, outstr):
        for st in outstr:
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
            elif p=='41':
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


    def signal_handler(self, signal, frame):
        print('received HUP signal')
        self.prepareMessage(LedDisplayMode.HOLD, '')
        sys.exit(0)

class LedDisplayMode:
    ROTATE = "a"  # Message travels right to left.
    HOLD = "b"  # Message remains stationary.
    FLASH = "c"  # Message remains stationary and flashes.
    ROLL_UP = "e"  # Previous message is pushed up by new message.
    ROLL_DOWN = "f"  # Previous message is pushed down by new message.
    ROLL_LEFT = "g"  # Previous message is pushed left by new message.
    ROLL_RIGHT = "h"  # Previous message is pushed right by new message.
    WIPE_UP = "i"  # New message is wiped over the previous message from bottom to top.
    WIPE_DOWN = "j"  # New message is wiped over the previous message from top to bottom.
    WIPE_LEFT = "k"  # New message is wiped over the previous message from right to left.
    WIPE_RIGHT = "l"  # New message is wiped over the previous message from left to right.
    SCROLL = "m"  # New message line pushes the bottom line to the top line if two line unit.
    AUTOMODE = "o"  # Various modes are called upon to display the message automatically.
    ROLL_IN = "p"  # Previous message is pushed toward the center of the display by the new message.
    ROLL_OUT = "q"  # Previous message is pushed outward from the center of the display by the new message.
    WIPE_IN = "r"  # New message is wiped over the previous message in an inward motion.
    WIPE_OUT = "s"  # New message is wiped over the previous message in an outward motion.
    COMPRESSED_ROTATE = "t"  # Message travels right to left.  Characters are approximately one half their normal width.  Available only on certain models. (See your Owner's Manual.)
    TWINKLE = "n0"  # The message will twinkle on the display.
    SPARKLE = "n1"  # The new message will sparkle on the display over the current message.
    SNOW = "n2"  # The message will "snow" onto the display.
    INTERLOCK = "n3"  # The new message will interlock over the current message in alternating rows of dots from each end.
    SWITCH = "n4"  # Alternating characters "switch" off the display up and down. New message "switches" on in a similar manner.
    SLIDE = "n5"  # The new message slides onto the display one character at a time from right to left.
    SPRAY = "n6"  # The new message sprays across and onto the display from right to left.
    STARBURST = "n7"  # "Starbursts" explode your message onto the display.
    SCRIPT_WELCOME = "n8"  # The word "Welcome" is written in script across the display.
    SLOT_MACHINE = "n9"  # Slot machine symbols randomly appear across the display.

    @staticmethod
    def random():
        return 'o'

class LedColor:
    RED = '\x1c1'
    GREEN = '\x1c2'
    AMBER = '\x1c3'
    DIMRED = '\x1c4'
    DIMGREEN = '\x1c5'
    BROWN = '\x1c6'
    ORANGE = '\x1c7'
    YELLOW = '\x1c8'
    RAINBOW1 = '\x1c9'
    RAINBOW2 = '\x1cA'
    MIXED = '\x1cB'
    AUTO = '\x1cC'

    @staticmethod
    def random():
        return '\x1c' + ('%1X' % random.randrange(1, 13))

class spetialFunction:
    CLEAR_MEMORY='\x24'
    WRITE_TEXT_FILE='\x41'
    WRITE_SPEC_FUNC='\x45'
    IR_ACCESIBLE='\x55'
    DISPLAY_POSITION_FILL='\x30'
    SET_COLOR='\x1C'





