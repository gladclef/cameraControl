# This server acts as the go-between in many php tasks that are running on behalf of long-poll clients.

import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import select

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
clients = { "": [] }

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    conn = None
    ip = "127.0.0.1"
    port = 0
    camera = ""
 
    def __init__(self,conn,ip,port,camera=""):
        Thread.__init__(self)
        if (ip != "127.0.0.1"):
            raise Exception()
        self.conn = conn
        self.ip = ip
        self.port = port
        self.camera = camera
        print "[+] New server socket thread started for " + ip + ":" + str(port)

    def __del__(self):
        self.conn.close()
        self.tryRemove()
        print("[-] Client connection closed")

    def tryRemove(self):
        try:
            clients[self.camera].remove(self)
        except Exception as e:
            pass

    def checkConn(self):
        try:
            if (self.conn.fileno() < 0):
                return False
        except Exception as e:
            return False
        return True

    def tryRecv(self, default = ""):
        try:
            return self.conn.recv(2048)
        except Exception as e:
            return default

    def trySend(self, msg):
        try:
            self.conn.send(msg)
            return True
        except Exception as e:
            return False
 
    def run(self): 
        while True:
            if not self.checkConn():
                break
            ready = select.select([self.conn], [], [], 1)
            if ready[0]:
                data = self.tryRecv()
                a_data = data.split("\n")
                b_stop = False
                for s_data in a_data:
                    s_data = s_data.strip()
                    if (len(s_data) <= 0):
                        continue
                    print("[:] Received message \"" + s_data + "\" from client")
                    if (s_data.startswith("disconnect")):
                        b_stop = True
                        break
                    if (s_data.startswith("subscribe ")):
                        self.tryRemove()
                        self.camera = s_data.strip()[len("subscribe "):]
                        if not (self.camera in clients):
                            clients[self.camera] = []
                        clients[self.camera].append(self)
                        continue
                    for otherClient in clients[self.camera]:
                        if (otherClient != self):
                            if not otherClient.trySend(s_data):
                                otherClient.__del__()
                if b_stop:
                    break
        self.__del__()

# Multithreaded Python server : TCP Server Socket Program Stub
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
 
while True:
    conn = None
    try:
        tcpServer.listen(4)
        print "Multithreaded Python server : Waiting for connections from TCP clients..."
        (conn, (ip,port)) = tcpServer.accept()
        if conn is None:
            break
        try:
            conn.setblocking(0)
            newthread = ClientThread(conn,ip,port)
            newthread.start()
            clients[""].append(newthread)
        except Exception as e:
            print "Bad ip \"" + ip + "\", port \"" + port + "\", or camera name \"\""
    except KeyboardInterrupt:
        if conn:
            conn.close()
        break

for camName in clients:
    for t in clients[camName]:
        t.join()