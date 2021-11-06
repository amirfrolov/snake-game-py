from collections import deque
import socket
TCP_SPLITTER = ';'
SOCKETS_TO_CLOSE = deque()
class TCP_manager():
    def __init__(self, tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM), addr = "127.0.0.1"):
        self.__tcp_socket = tcp_socket
        SOCKETS_TO_CLOSE.append(tcp_socket)
        tcp_socket.settimeout(1/50)
        self.__got_data_deque = deque()
        self.__addr = addr
    
    def connect(self, ip, port):
        self.__tcp_socket.connect((ip, port))
    def send(self, data_to_send):
        data_to_send += TCP_SPLITTER
        self.__tcp_socket.send(data_to_send.encode())

    def recv(self):
        connected = True
        raw_data_str = ""
        result_data_str = ""
        try:
            raw_data_str = self.__tcp_socket.recv(1024)
            connected = raw_data_str != b''
        except socket.timeout:
            pass #time out
        except ConnectionResetError:
            pass #the other side sending a msg
        if raw_data_str:
            for i in raw_data_str.decode().split(TCP_SPLITTER):
                if i:
                    self.__got_data_deque.append(i)
        if self.__got_data_deque:
            result_data_str = self.__got_data_deque.popleft()
        return connected, result_data_str
    def close(self):
        SOCKETS_TO_CLOSE.remove(self.__tcp_socket)
        self.__tcp_socket.close()

def close_all():
    for i_socket in SOCKETS_TO_CLOSE:
        i_socket.close()