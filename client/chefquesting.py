#!/usr/bin/python           # This is client.py file
#
import termios, fcntl, sys, os
import socket               # Import socket module
from thread import *
import Queue
import time

COLOR = '\x1b[3%sm'
RED = '1'
GREEN = '2'
YELLOW = '3'
BLUE = '4'
MAGENTA = '5'
CYAN = '6'
WHITE = '7'

def color_for_type(t):
    if t == 0:
        return WHITE
    elif t == 1:
        return GREEN
    elif t == 2:
        return RED
    elif t == 3:
        return BLUE
    elif t == 4:
        return CYAN
    else:
        return WHITE

def server_down(s, q):
    overflowData = ''
    while 1:
        time.sleep(0.05)
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
                if sizeSoFar > 2:
                    q.put(''.join(data)[2:])
                return
            data += datum
            sizeSoFar += len(datum)
            if sizeSoFar > 1 and packetSize == -1:
                soFar = ''.join(data)
                packetSize = (ord(soFar[0]) * 256) + ord(soFar[1])
            working = packetSize == -1 or sizeSoFar < (packetSize + 2)
        message = ''.join(data)
        #   print 'Done with length ', len(message), ' and contents: ', message
        if len(message) > 2:
            if len(message) == 3:
                if ord(message[2:]) == 127:
                    s.close()
                    return
            q.put(message[2:(packetSize+2)])
            if len(message) > (packetSize + 2):
                overflowData = message[(packetSize+2):]
                #   print 'Used overflow!'


def server_up(s, q):
    while 1:
        time.sleep(0.05)
        while not q.empty():
            m = q.get()
            mLen = len(m)
            if mLen == 1:
                if ord(m) == 127:
                    s.close()
                    return
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

def connection_thread(s):
    qUpload = Queue.Queue()
    qDownload = Queue.Queue()
    start_new_thread(server_up,(s,qUpload,))
    start_new_thread(server_down,(s,qDownload,))
    while 1:
        chars = []
        while 1:
            time.sleep(0.02)
            try:
                while not qDownload.empty():
                    output = qDownload.get()
                    typeStr = output[0]
                    output = output[1:]
                    colorStr = COLOR % (color_for_type(ord(typeStr)),)
                    sys.stdout.write(colorStr + output + '\n')
                c = sys.stdin.read(1)
                sys.stdout.write(COLOR % (WHITE,))
                sys.stdout.write('I shall... ')
                chars += c
                sys.stdout.write(c)
                while 1:
                    time.sleep(0.02)
                    try:
                        cc = sys.stdin.read(1)
                        if cc == '\n':
                            break
                        if ord(cc) == 127:
                            if len(chars) > 0:
                                chars.pop()
                                sys.stdout.write('\b \b')
                        else:
                            sys.stdout.write(cc)
                            chars += cc
                    except IOError: pass
                break
            except IOError: pass
        inputStr = ''.join(chars)
        if inputStr.strip() == 'quit':
            sys.stdout.write('\n')
            return True
        if inputStr.strip() in set(['logout', 'logoff', 'disconnect']):
            qUpload.put(chr(127))
            qDownload.put(chr(127))
            return False
        bksp = '\b' * len('I shall... ' + inputStr)
        bksp += ' ' * len('I shall... ' + inputStr)
        bksp += '\b' * len('I shall... ' + inputStr)
        sys.stdout.write(bksp)
        qUpload.put(inputStr)
        # CURSOR_UP_ONE = '\x1b[1A'
        # ERASE_LINE = '\x1b[2K'
        # print(ERASE_LINE + CURSOR_UP_ONE)


if __name__=="__main__":
    # Dark Magick that turns off Terminal echo and stdin call blocking, which allows our cool keyboard polling
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    # for more info, see https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time
    #
    host_home = "games.aitocir.org"
    port = 27243
    host_pi = "192.168.2.5"
    host_typed = []
    host_typed += host_home
    playtimeover = False
    # start with white color in Terminal
    sys.stdout.write(COLOR % (WHITE,))
    while not playtimeover:
        try:
            sys.stdout.write('Please enter a ChefQuesting server address (default provided): ' + ''.join(host_typed))
            while 1:
                time.sleep(0.02)
                try:
                    c = sys.stdin.read(1)
                    if c == '\n':
                        break
                    if ord(c) == 127:
                        if len(host_typed) > 0:
                            sys.stdout.write('\b \b')
                            host_typed.pop()
                    else:
                        sys.stdout.write(c)
                        host_typed += c
                except IOError: pass
            if ''.join(host_typed) == 'quit':
                sys.stdout.write('\n')
                playtimeover = True
                break
            sys.stdout.write('\nConnecting...')
            s = socket.socket()
            s.connect((''.join(host_typed), port))
            sys.stdout.write('succeeded! All further content provided by server.\n')
            sys.stdout.write('(Use [logoff], [logout], or [disconnect] to join another server, and [quit] to close this program entirely.\n')
            playtimeover = connection_thread(s)
            print 'You have disconnected from the server.'
        except socket.error as se:
            print se
            print 'Tried hostname: ' + ''.join(host_typed)
        except Exception as e:
            print e
            sys.stdout.write('failed. Check your server address spelling, troubleshoot your network connection, or join another server.\n')
    # done, return Terminal to its original state
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    # TODO: print goodbye
