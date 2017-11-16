
from synapse.platforms import *
from synapse.hexSupport import *
from synapse.CAT24C128 import * # Example Serial EEPROM chip
from synapse.switchboard import *


redLEDPin = GPIO_2
greenLEDPin=GPIO_1

def init():
    # Go ahead and redirect STDOUT to Portal now
    ucastSerial("\x00\x00\x01") # put your correct Portal address here!
    
    #crossConnect(DS_STDIO,DS_TRANSPARENT)
    crossConnect( DS_STDIO, DS_UART1)
    initUart(1, 9600)
    stdinMode(1, False)      # Line Mode, Echo On

    
@setHook(HOOK_STARTUP)
def startupEvent():
    setPinDir(greenLEDPin, True)
    setPinDir(redLEDPin, True)
    pulsePin(redLEDPin, 1000, True)
    init() 
    
@setHook(HOOK_STDOUT)
def getOutput(data):
    pulsePin(redLEDPin, 1000, True)
    pass 
    
@setHook(HOOK_1S)
def timer100msEvent(currentMs):
    pulsePin(greenLEDPin, 500, True)

def writePacket(s):
    print s,

           