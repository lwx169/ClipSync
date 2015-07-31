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


CBS_CONN_MAX = 5

class CBSServer(threading.Thread):

    def __init__(self, port):
        self.address    = ('', int(port))
        self.listenSock = None
        self.sockSet    = []
        threading.Thread.__init__(self)


    def run(self):
        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenSock.bind(self.address)
        self.listenSock.listen(CBS_CONN_MAX)
        self.sockSet.append(self.listenSock)

        while True:
            readSet, writeSet, errorSet = select.select(self.sockSet, [], [])
            for sock in readSet:
                if sock is self.listenSock:
                    connSock, connAddr = self.listenSock.accept()
                    if connSock not in self.sockSet:
                        CBS_LOG_INFO("New client %s connected" % (connAddr[0]))
                        self.sockSet.append(connSock)
                else:
                    self._handleCBSP(sock)


    def updateClip(self, data):
        cbsp  = CBSP(data)
        for sock in self.sockSet:
            if sock is not None and sock is not self.listenSock:
                try:
                    sock.send(cbsp.getHeader())
                    sock.send(cbsp.getContent())
                except Exception, e:
                    CBS_LOG_ERROR("updateClip Error: %s" % (e))


    def _handleCBSP(self, sock):
        CBS_LOG_DEBUG("hanle CBSP packet")
        header = sock.recv(CBSP_HEADER_LEN)
        if len(header) != CBSP_HEADER_LEN:
            CBS_LOG_ERROR("_handleCBSP Error: invalid header length %d" % (len(header)))
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
                CBS_LOG_ERROR("_handleCBSP Error: %s" % (e))
