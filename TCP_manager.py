from collections import deque
import socket
import netifaces

TCP_SPLITTER = ';'
SOCKETS_TO_CLOSE = deque()
MSG_TIME_OUT = 1/50

def get_my_ip_addr():
    ip = "127.0.0.1"
    for i in netifaces.interfaces():
        try:
            tmp_ip = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
            if tmp_ip[:3] != "127":
                ip = tmp_ip
        except Exception:
            pass
    return ip

MY_IP = get_my_ip_addr()

class TCP_manager():
    def __init__(self, tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM), connect_addr=None, connect_time_out = 1):
        self.__tcp_socket = tcp_socket
        SOCKETS_TO_CLOSE.append(self.__tcp_socket)
        self.__tcp_socket.settimeout(connect_time_out)
        if connect_addr:
            self.__tcp_socket.connect(connect_addr)
        self.__tcp_socket.settimeout(MSG_TIME_OUT)
        self.__got_data_deque = deque()
        self.__tmp_buffer = ""
    
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
            for i in raw_data_str.decode():
                if i != TCP_SPLITTER:
                    self.__tmp_buffer += i
                else:
                    self.__got_data_deque.append(self.__tmp_buffer)
                    self.__tmp_buffer = ""
                    
        if self.__got_data_deque:
            result_data_str = self.__got_data_deque.popleft()
        return connected, result_data_str

    def close(self):
        SOCKETS_TO_CLOSE.remove(self.__tcp_socket)
        self.__tcp_socket.close()

def close_all():
    for i_socket in SOCKETS_TO_CLOSE:
        i_socket.close()

if __name__ == "__main__":
    print(MY_IP)