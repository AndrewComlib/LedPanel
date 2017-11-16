#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import sys
import traceback
import signal

import LedDisplay as display
import RFConnector

if __name__ == "__main__":
    conn=None
    #---------------------------------
    stickAddress='/dev/ttyUSB0'
    targetNodeAddress='\x07\x91\x1B'
    '''
    targetMessage=[['Gentelements!', display.LedDisplayMode.SNOW, display.LedColor.MIXED],
                   ['Now', display.LedDisplayMode.HOLD, display.LedColor.GREEN],
                   ['we can send', display.LedDisplayMode.ROLL_DOWN, display.LedColor.AMBER],
                   ['any messages', display.LedDisplayMode.ROLL_LEFT, display.LedColor.RED],
                   ['to LED-panel', display.LedDisplayMode.ROTATE, display.LedColor.YELLOW],
                   ['from ', display.LedDisplayMode.SPARKLE, display.LedColor.DIMGREEN],
                   ['anywhere', display.LedDisplayMode.SWITCH, display.LedColor.DIMRED],
                   ['by air', display.LedDisplayMode.WIPE_DOWN, display.LedColor.RAINBOW1],
                   ['with the Synapse.', display.LedDisplayMode.STARBURST, display.LedColor.MIXED],
                   ['I''m happy...', display.LedDisplayMode.FLASH, display.LedColor.RAINBOW2]
                  ]
    '''
    targetMessage = [['Gentelements!', display.LedDisplayMode.SNOW, display.LedColor.MIXED]]
    #---------------------------------
    try:
        panel = display.display()                           #Экземпляр LED-панели
        signal.signal(signal.SIGHUP, panel.signal_handler)
    except:
        print 'Display initialization error'
        time.sleep(5)
        sys.exit(1)

    try:
        #Коннектор стика
        conn = RFConnector.BridgeVersionClient(stickAddress, targetNodeAddress)
    except:
        print 'RF module connection error'
        sys.exit(2)

    try:
        #Получение строки байт в формате альфа-протокола для отправки на ноду
        #messageClear=conn.clearScreen()
        message=panel.prepareMessage(targetMessage)
    except SystemExit:
        print('exiting')
        raise
    except:
        print("CRASH: " + str(sys.exc_info()[0]))
        tb = traceback.format_exc()
        print(tb)
        time.sleep(5)
    print 'Out message: ', message
    #Отправляем строку байт на ноду

    #conn.clearScreen()
    conn.sendMessage(message)




#============================================================================

def main():

    global preferences

#-------------------------------------------------------------------------------


    '''
        # TIME OF DAY

        timeOfDay=datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        displayFeedback('TIME',timeOfDay)
        ledDisplay(LedDisplayMode.HOLD, LedColor.RED+timeOfDay)
        time.sleep(5)

        # GARAGE DOOR

        content = ''
        try:
            fname = '/tmp/betabrite.'+str(os.getpid())
            urllib.urlretrieve("http://garagepi/", filename=fname)
            with open(fname) as f:
                content = f.readlines()
        except IOError:
            pass

        doorState = '???'
        if len(content) > 0:
            for line in content:
                line = line.rstrip('\n')
                if (line == 'DOOR=OPEN'):
                    doorState = 'open'
                elif (line == 'DOOR=CLOSED'):
                    doorState = 'closed'

        displayFeedback('DOOR','garage '+doorState)
        ledDisplay(LedDisplayMode.HOLD, LedColor.BROWN+'garage '+doorState)
        time.sleep(5)

        # FLASHBACK

        fname = '/tmp/betabrite.'+str(os.getpid())
        content = ''
        try:
            urllib.urlretrieve("http://pogo/status.txt", filename=fname)
            with open(fname) as f:
                content = f.readlines()
        except IOError:
            pass

        fbTarget = '???'
        fbStatus = ''
        if len(content) > 0:
            kvpairs = dict(line.rstrip('\n').split('=') for line in content)
            fbStatus = re.sub('_', ' ', kvpairs['status'])
            fbTarget = kvpairs['target']
            fbWait = kvpairs['wait']
            if (fbWait != '0'):
                fbStatus += ' ' + fbWait
            fbDisk = kvpairs['disk.free.percent']+'% free'

        displayFeedback('FLASHBACK',fbStatus+' '+fbTarget)
        ledDisplay(LedDisplayMode.ROTATE,
            LedColor.GREEN+'flashback: '+
            LedColor.YELLOW+fbStatus+' '+
            LedColor.ORANGE+fbTarget+' '+
            LedColor.RED+fbDisk)
        time.sleep(10)

        # INTERMISSION

        displayFeedback('SLOT MACHINE','5s')
        ledDisplay(LedDisplayMode.SLOT_MACHINE, '')
        time.sleep(5)

        # LOOK UP TWITTER STUFF

        try:
            twitterInit()
            twitterUserTimeline = twitterGetUserTweets(preferences.twitter_mine_count)
            twitterHomeTimeline = twitterGetHomeTweets(preferences.twitter_peer_count)
        except tweepy.error.TweepError as e:
            # we did not get anything from Twitter, so don't show any messages
            twitterUserTimeline = ()
            twitterHomeTimeline = ()
            # show some info about the error
            response = e.response
            status = 0
            if response == None:
                print "TWITTER !!! unknown Tweepy error"
            else:
                print "TWITTER !!! Tweepy error %d: %s" % (e.response.status, e.response.reason)
                if e.response.status == 429:
                    displayFeedback('PAUSE FOR TWITTER API RESET','60s')
                    ledDisplay(LedDisplayMode.SNOW, 'TWITTER ERROR')
                    time.sleep(60)
            pass

        # MY TWEETS

        for tweet in reversed(twitterUserTimeline):
            timeStamp = utc_to_local_datetime(tweet.created_at).strftime('%a %H:%M')
            tweetText = unicodeHtmlToAscii(tweet.text)
            displayFeedback('MY TWEET', '('+timeStamp+') '+tweetText)
            # RED GREEN AMBER DIMRED DIMGREEN BROWN ORANGE YELLOW RAINBOW1 RAINBOW2 MIXED
            ledDisplay(LedDisplayMode.COMPRESSED_ROTATE,
                LedColor.RED+timeStamp+' '+
                LedColor.YELLOW+tweetText)
            time.sleep(preferences.twitter_mine_delay)

        # INTERMISSION

        if len(twitterUserTimeline) > 0:
            displayFeedback('SLOT MACHINE','5s')
            ledDisplay(LedDisplayMode.SLOT_MACHINE, '')
            time.sleep(5)

        # OTHERS' TWEETS

        for tweet in reversed(twitterHomeTimeline):
            timeStamp = utc_to_local_datetime(tweet.created_at).strftime('%a %H:%M')
            tweetUser = unicodeHtmlToAscii(tweet.user.name)
            tweetText = unicodeHtmlToAscii(tweet.text)
            displayFeedback('PEER TWEET', '('+timeStamp+') '+tweetUser+': '+tweetText)
            # RED GREEN AMBER DIMRED DIMGREEN BROWN ORANGE YELLOW RAINBOW1 RAINBOW2 MIXED
            ledDisplay(LedDisplayMode.COMPRESSED_ROTATE,
                LedColor.RED+timeStamp+' '+
                LedColor.ORANGE+tweet.user.name+': '+
                LedColor.GREEN+tweetText)
            time.sleep(preferences.twitter_peer_delay)

        # INTERMISSION

        if len(twitterHomeTimeline) > 0:
            displayFeedback('SLOT MACHINE','5s')
            ledDisplay(LedDisplayMode.SLOT_MACHINE, '')
            time.sleep(5)

    # we never get here
    ledSerialPort.close()
'''