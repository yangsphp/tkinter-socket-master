import socket

bufsize = 1024

class SocketClient(object):
    def __init__(self, ip, port):
        self.socket_client = socket.socket()
        self.socket_client.connect((ip, port))
        
    def get_client(self):
        return self.socket_client
    
    def check_user(self, username, password):
        msg = '{"type": "check_user","username":"%s", "password":"%s"}' % (username, password)
        self.send_message(msg)
        data = self.socket_client.recv(bufsize).decode()
        print('login用户结果：'+data)
        return data
    
    def register_user(self, username, password):
        msg = '{"type": "register_user","username":"%s", "password":"%s"}' % (username, password)
        self.send_message(msg)
        data = self.socket_client.recv(bufsize).decode()
        print('注册用户结果：'+data)
        return data
        
    def send_message(self, msg):
        print(msg)
        self.socket_client.sendall(msg.encode())
        
    def get_online_user(self):
        msg = '{"type": "online"}'
        self.send_message(msg)
    
    def disconnect(self):
        self.socket_client.close()
        print('close socket ok')