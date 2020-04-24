import socketserver
import tkinter as tk
from threading import Thread
import time
import json
import logging
import os

# user_pool = ["yy"]
socket_pool = []
user_pool = []
bufsize = 1024
base_path = os.path.abspath('.')
file_path = base_path + '\\user\\'

class MyServer(socketserver.BaseRequestHandler):
    
    username = None
    
    def setup(self):
        print('setup')
        socket_pool.append(self.request)
    
    def handle(self):
        print(self.client_address)
        while True:
            data = json.loads(self.request.recv(bufsize).decode())
            _type = data.get('type')
            print('=====recv_data====')
            print(data)
            if _type == 'check_user':
                username = data.get('username')
                password = data.get('password')
                data_dict = {}
                data_dict['type'] = 'check_user'
                filename = "%s.txt" % username
                if os.path.exists(file_path + filename):
                    with open(file_path + filename, 'r') as f:
                        if f.readline().strip() == password:
                            data_dict['data'] = 'ok'
                            self.username = username
                            user_pool.append(username)
                        else:
                            data_dict['data'] = 'perror'
                else:
                    data_dict['data'] = 'uerror'
                msg = json.dumps(data_dict)
                self.request.sendall(msg.encode())
            elif _type == 'register_user':
                username = data.get('username')
                password = data.get('password')
                data_dict = {}
                data_dict['type'] = 'register_user'
                filename = "%s.txt" % username
                if os.path.exists(file_path + filename):
                    data_dict['data'] = "exists"
                else:
                    with open(file_path + filename, 'a') as f:
                        f.write(password)
                    data_dict['data'] = "ok"
                msg = json.dumps(data_dict)
                self.request.sendall(msg.encode())
            elif _type == 'online':
                data_dict = {}
                data_dict['type'] = 'online'
                data_dict['data'] = user_pool
                print('======发送线上用户=====')
                print(data_dict)
                self.send_message_to_all(data_dict)
            elif _type == 'message':
                data_dict = {}
                username = data.get('username')
                message = data.get('message')
                send_time = time.strftime('%Y-%m-%d %H:%M:%S')
                data_dict['type'] = 'message'
                data_dict['data'] = {"username": username, "send_time":send_time,"message":message}
                print('======发送消息=====')
                print(data_dict)
                self.send_message_to_all(data_dict)
            elif _type == 'logout':
                msg = '{"type":"logout"}'
                self.request.sendall(msg.encode())
                break
    
    def send_message_to_all(self, data):
        for server in socket_pool:
            server.sendall(json.dumps(data).encode())
    
    def finish(self):
        print('finish')
        try:
            user_pool.remove(self.username)
            socket_pool.remove(self.request)
        except Exception as e:
            logger.error(e)

def callCloseWindow():
    window.destroy()
    s.server_close()
    
def startServer():
    global s
    setMessageBox('服务器启动成功，正在监听...')
    s = socketserver.ThreadingTCPServer(('', 12346), MyServer)
    try:
        s.serve_forever()
    except Exception as e:
        logger.error(e)
        s.server_close()

def setMessageBox(msg):
    varSet.set(msg)

def main():
    global varSet, window, logger
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    
    window = tk.Tk()
    # 设置主窗体大小
    winWidth = 600
    winHeight = 400
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    # 计算主窗口在屏幕上的坐标
    x = int((screenWidth - winWidth)/ 2)
    y = int((screenHeight - winHeight) / 2)
    
    # 设置主窗口标题
    window.title("server")
    # 设置主窗口大小
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # 创建滚动条，置于窗口右侧，y方向填充
    scroll_bar = tk.Scrollbar(window)
    scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
    varSet = tk.StringVar()
    list_box = tk.Listbox(window, font=("宋体", 14), bg='black', fg='white', listvariable = varSet, yscrollcommand = scroll_bar.set, state=tk.DISABLED)
    list_box.pack(expand=1, fill=tk.BOTH)
    scroll_bar.config(command=list_box.yview)
    
    t = Thread(target=startServer)
    t.setDaemon(True)
    t.start()


    # 监听window关闭
    window.protocol("WM_DELETE_WINDOW", lambda : callCloseWindow())
    window.mainloop()

if __name__ == '__main__':
    main()
