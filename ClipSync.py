#!/usr/bin/env python

from CBSLog      import *
from ClipWatcher import ClipWatcher
from CBSServer   import CBSServer
from CBSClient   import CBSClient
from optparse    import OptionParser


import time

if __name__ == '__main__':

    usage = 'usage: ClipSync -s -p xxx\n       ClipSync -c xxx.xxx.xxx.xxx -p xxx'

    optParser = OptionParser(usage)
    optParser.add_option('-s', dest='serverFlag', action='store_true',
                         default=False, help='run as server')
    optParser.add_option('-c', dest='serverIp', help='run as client, set server ip address')
    optParser.add_option('-p', dest='serverPort', help='ClipSync port')
    (options, args) = optParser.parse_args()
    serverFlag = options.serverFlag
    serverIp   = options.serverIp
    serverPort = options.serverPort

    # init logger
    initLog()

    if serverFlag is True: # run as server
        CBSNode = CBSServer(serverPort)
    else: # run as client
        CBSNode = CBSClient(serverIp, serverPort)

    # run CBSNode
    CBS_LOG_INFO('CBSNode running ...')
    CBSNode.start()

    # run clipboard watcher
    watcher = ClipWatcher()
    watcher.registerEventHandler(ClipWatcher.CLIP_EVENT_UPDATE, CBSNode.updateClip)

    CBS_LOG_INFO('ClipBoard Watcher running ...')
    watcher.start()
