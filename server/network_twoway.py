
import socket
import time
import Queue

def socket_inbound(s, q):
    overflowData = ''
    packetSize = -1
    sizeSoFar = 0
    while 1:
        time.sleep(0.05)
        working = True
        data = []
        if len(overflowData) > 0:
            data += overflowData
            sizeSoFar = len(data)
            overflowData = ''
        while working:
            datum = s.recv(16384)
            if len(datum) == 0:
                s.close()
                if sizeSoFar > 2:
                    q.put(''.join(data)[2:])
                return
            data += datum
            sizeSoFar = len(data)
            if sizeSoFar > 1 and packetSize == -1:
                soFar = ''.join(data)
                packetSize = (ord(soFar[0]) * 256) + ord(soFar[1])
            working = packetSize == -1 or sizeSoFar < (packetSize + 2)
        message = ''.join(data)
        messagesLeft = True
        while messagesLeft:
            if len(message) > 2:
                if len(message) == 3:
                    if ord(message[2:]) == 127:
                        s.close()
                        return
                q.put(message[2:(packetSize+2)])
                message = message[(packetSize+2):]
                if len(message) < 2:
                    packetSize = -1
                    messagesLeft = False
                    sizeSoFar = len(message)
                else:
                    packetSize = (ord(message[0]) * 256) + ord(message[1])
                    messagesLeft = (packetSize + 2) <= len(message)


def socket_outbound(s, q):
   while 1:
      time.sleep(0.02)
      while not q.empty():
         m = q.get()
         mLen = len(m)
         byte0 = mLen // 256
         byte1 = mLen % 256
         message = chr(byte0) + chr(byte1) + m
         messLen = mLen + 2
         totalSent = 0
         while totalSent < messLen:
            sent = s.send(message[totalSent:])
            if sent == 0:
               s.close()
               return
            totalSent += sent
