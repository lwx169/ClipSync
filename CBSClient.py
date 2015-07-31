#!/usr/bin/env python

import threading
import struct
import pyperclip
import socket
import select

from CBSLog import *
from CBSProtocol import *

# cross platform clipborad operation wrapper library
clipCopy  = pyperclip.copy
clipPaste = pyperclip.paste

class CBSClient(threading.Thread):

    def __init__(self, ip, port):
        self.address = (ip, int(port))
        self.sock = None
        threading.Thread.__init__(self)


    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)

        while True:
            readSet, writeSet, errorSet = select.select([self.sock], [], [])
            if self.sock in readSet:
                self._handleCBSP(self.sock)


    def updateClip(self, data):
        cbsp  = CBSP(data)
        if self.sock is not None:
            try:
                self.sock.send(cbsp.getHeader())
                self.sock.send(cbsp.getContent())
            except Exception, e:
                CBS_LOG_ERROR("Error: %s" % (e))


    def _handleCBSP(self, sock):
        CBS_LOG_DEBUG("hanle CBSP packet")
        header = sock.recv(CBSP_HEADER_LEN)
        if len(header) != CBSP_HEADER_LEN:
            CBS_LOG_ERROR("Error: invalid header length %d" % (len(header)))
            return

        magic, action, version, length = struct.unpack(CBSP_HEADER_FMT, header)
        magic   = socket.ntohl(magic)
        action  = socket.ntohl(action)
        version = socket.ntohl(version)
        length  = socket.ntohl(length)

        if magic != CBSP_MAGIC or version != CBSP_VERSION:
            return

        if action == CBSP_ACT_UPDATE:
            try:
                data = sock.recv(length)
                cbsp = CBSP(data)
                clipCopy(cbsp.getContent())
            except Exception, e:
                CBS_LOG_ERROR("Error: %s" % (e))
