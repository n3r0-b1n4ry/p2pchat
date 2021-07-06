# import module alternative
import sys
import socket
import threading
import errno

# import module for message encoding/decoding
import base64


class recv_session(threading.Thread):

    host_sock = None

    client_sock = None
    client_addr = None
    client_user = ""

    def __init__(self):
        self.host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_listening()
    
    def create_listening(self):
        try:
            # self.host_sock.bind((socket.gethostname(), 54818))
            self.host_sock.bind(("0.0.0.0", 54818))
            self.host_sock.listen(5)
            return True
        except Exception as e:
            print(e)
            return False

    def listen(self):
        try:
            (self.client_sock, self.client_addr) = self.host_sock.accept()
            self.client_user = (socket.gethostbyaddr(self.client_addr[0]))[0]
            return True
        except Exception as e:
            print(e)
            return False

    def recv_msg(self):
        try:
            while True:
                data_temp = self.client_sock.recv(4096)
                if data_temp == b'\x00\x01\x02\x03':
                    sent = self.client_sock.send(data_temp)
                    return None
                if data_temp == b'':
                    return None
                else:
                    msg = (base64.b64decode(data_temp)).decode()
                    if msg != "":
                        return "{}: {}".format(self.client_user,msg)
            return None
        except socket.error as e:
            if e.errno == errno.WSAECONNRESET:
                self.listen()
                return None
        except Exception as e:
            print(e)
            return None

    def close_connection(self):
        try:
            self.client_sock.close()
        except Exception as e:
            print(e)


class send_session(threading.Thread):

    host_sock = None
    host_user = socket.gethostname()
    
    client_addr = None
    client_user = ""

    # def __init__(self):
    #     self.host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_connection(self, hostname):
        self.host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.host_sock.connect((hostname, 54818))
            self.client_addr = hostname
            self.client_user = (socket.gethostbyaddr(self.client_addr))[0]
            return True
        except Exception as e:
            print(e)
            return False

    def is_active(self):
        try:
            sent = self.host_sock.send(b'\x00\x01\x02\x03')
            if self.host_sock.recv(4096) == b'\x00\x01\x02\x03':
                return True
            else:
                raise "Connection was closed"
        except:
            print("Connection was closed")
            return False

    def send_msg(self, msg):        
        try:
            sent = self.host_sock.send(base64.b64encode(str(msg).encode("utf-8")))
            return True
        except Exception as e:
            print(e)
            self.close_connection()
            return False

    def close_connection(self):
        try:
            self.host_sock.close()
        except Exception as e:
            print(e)

