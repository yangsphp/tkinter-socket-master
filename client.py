import json
import time
from tkinter import messagebox
from threading import Thread

from socketClient import SocketClient
from LoginWindow import LoginWindow
from MainWindow import MainWindow
from RegisterWindow import RegisterWindow

ip = '127.0.0.1'
port = 12346


def open_main_window():
    global main_window
    main_window = MainWindow(send_message, close_main_window)
    t = Thread(target=recv_data)
    t.setDaemon(True)
    t.start()
    main_window.show()
    

def recv_data():
    time.sleep(1)
    client_socket = client.get_client()
    while True:
        try:
            data = client_socket.recv(1024).decode()
            print('=====recv_data====')
            data = json.loads(data)
            print(data)
            _type = data.get('type')
            if _type == 'logout':
                break
            elif _type == 'online':
                user_name_list = data.get('data')
                user_name_list.reverse()
                print('在线用户：')
                print(user_name_list)
                main_window.set_user_list(user_name_list)
            elif _type == 'message':
                main_window.set_user_message(data.get('data'))
        except Exception as e:
            print(e)
            break
    client.disconnect()
    
def close_main_window():
    client.send_message('{"type": "logout"}')
    main_window.window.destroy()

def login():
    global username
    username, password = login_window.get_input()
    if username == '' or password == '':
        messagebox.showerror(title='提示', message='请输入用户名或密码')
        return
    result = client.check_user(username, password)
    data = json.loads(result)
    data = data.get('data')
    if data == 'uerror':
        messagebox.showerror(title="错误", message="用户名不存在")
    elif data == 'perror':
        messagebox.showerror(title="错误", message="密码不正确")
    elif data == 'ok':
        login_window.window.destroy()
        client.get_online_user()
        open_main_window()
    
def register():
    print('register...')
    global register_window
    login_window.window.destroy()
    register_window = RegisterWindow(do_cancel, do_register, close_register_window)
    register_window.show()

def close_register_window():
    client.send_message('{"type": "logout"}')
    register_window.close_register_window()
    
def do_cancel():
    register_window.window.destroy()
    login_window.show()

def do_register():
    username, password, rpassword = register_window.get_input()
    if username == '':
        messagebox.showerror(title='提示', message='请输入用户名')
        return
    if password == '':
        messagebox.showerror(title='提示', message='请输入密码')
        return
    if rpassword == '':
        messagebox.showerror(title='提示', message='请再次输入密码')
        return
    if password != rpassword:
        messagebox.showerror(title='提示', message='两次密码输入不一致')
        return
    result = client.register_user(username, password)
    data = json.loads(result)
    data = data.get('data')
    print(data)
    if data == 'exists':
        messagebox.showerror(title='错误', message='用户已经被注册')
        return
    elif data == 'ok':
        messagebox.showinfo(title='提示', message='注册用户成功')
        do_cancel()
    
def close_login_window():
    print('close_login_window...')
    client.send_message('{"type": "logout"}')
    login_window.close_login_window()
    
def send_message():
    print('send_message...')
    message = main_window.get_message()
    if len(message) == 0:
        messagebox.showerror(title='提示', message='请输入消息')
        return
    msg = '{"type":"message", "username": "%s", "message": "%s"}' % (username, message)
    client.send_message(msg)

def main():
    global client, login_window
    client = SocketClient(ip, port)
    login_window = LoginWindow(login, register, close_login_window)
    login_window.show()
    

if __name__ == '__main__':
    main()