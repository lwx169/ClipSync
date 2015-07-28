#!/usr/bin/env python

import threading
import time
import logging
import pyperclip

from CBSLog import *


# default check interval (1s)
CBS_DFT_CHECK_INTERVAL = 1

# cross platform clipborad operation wrapper library
clipCopy  = pyperclip.copy
clipPaste = pyperclip.paste


''' check clipboard content changed and trigger a event
'''
class ClipWatcher(threading.Thread):

    CLIP_EVENT_UPDATE = 1

    def __init__(self):
        self.eventHanlders   = {}
        self.watchFlag       = True
        self.prevClipContent = None
        self.currClipContent = None
        self.checkInterval   = CBS_DFT_CHECK_INTERVAL

        threading.Thread.__init__(self)


    def setCheckInterval(self, interval):
        self.checkInterval = interval


    def registerEventHandler(self, event, handler):
        self.eventHanlders[event] = handler


    def _callHandler(self, event, args):
        if self.eventHanlders[event] is not None:
            return self.eventHanlders[event](args)


    def run(self):
        self.watchFlag = True
        self.prevClipContent = clipPaste()

        while self.watchFlag:
            time.sleep(self.checkInterval)
            self.currClipContent = clipPaste()
            if self.currClipContent != self.prevClipContent:
                CBS_LOG_DEBUG("clipboard update")
                self._callHandler(self.CLIP_EVENT_UPDATE, self.currClipContent)
                self.prevClipContent = self.currClipContent


    def stop(self):
        self.watchFlag = False
