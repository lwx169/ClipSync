#!/usr/bin/env python

import struct
import socket

'''
ClipBoard Sync Protocol (TCP)

 0        32        64        96      128
 +--------+---------+---------+--------+
 | Magic  | Action  | Version | Length |    Header (16 Byte)
 |-------------------------------------+
 |                                     |
 |                Data                 |    Content
 |                                     |
 +-------------------------------------+

'''

# packet format
CBSP_HEADER_FMT = "IIII"        # magic | action | version | length

# header length
CBSP_HEADER_LEN = 16

# magic definition
CBSP_MAGIC = 0xcbcb

# versiton definition
CBSP_VERSION = 10000

# action definition
CBSP_ACT_UPDATE = 1


''' Class: ClipBoard Sync Packet
'''
class CBSP(object):

    magic   = socket.htonl(CBSP_MAGIC)
    action  = socket.htonl(CBSP_ACT_UPDATE)
    version = socket.htonl(CBSP_VERSION)

    def __init__(self, data):
        self.content = data
        self.length  = socket.htonl(len(data))
        self.header  = None
        self._packHeader()

    def setAction(self, action):
        self.action = action
        self._packHeader()

    def getVersion(self):
        return self.version

    def getAction(self):
        return self.action

    def getContent(self):
        return self.content

    def getHeader(self):
        return self.header

    def _packHeader(self):
        self.header = struct.pack(CBSP_HEADER_FMT,
                                  self.magic, self.action,
                                  self.version, self.length)
