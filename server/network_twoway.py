
import socket
import time
import Queue

def socket_inbound(s, q):
   overflowData = ''
   while 1:
      time.sleep(0.02)
      working = True
      packetSize = -1
      sizeSoFar = 0
      data = []
      if len(overflowData) > 0:
         data += overflowData
         sizeSoFar += len(overflowData)
         overflowData = ''
      while working:
         datum = s.recv(1024)
         if len(datum) == 0:
            s.close()
            if sizeSoFar > 0:
               q.put(''.join(data))
            q.put('')
            return
         data += datum
         sizeSoFar += len(datum)
         if sizeSoFar > 1 and packetSize == -1:
            soFar = ''.join(data)
            packetSize = (ord(soFar[0]) * 256) + ord(soFar[1])
         working = packetSize == -1 or sizeSoFar < (packetSize + 2)
      message = ''.join(data)
      if len(message) > 2:
         q.put(message[2:(packetSize+2)])
         if len(message) > (packetSize + 2):
            overflowData = message[(packetSize+2):]


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
