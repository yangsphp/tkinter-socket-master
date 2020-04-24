import tkinter as tk
from tkinter import scrolledtext

class MainWindow():
    def __init__(self, send_message, close_main_window):
        self.send_message = send_message
        self.close_main_window = close_main_window
    
    def show(self):
        window = tk.Tk()
        self.window = window
        # 设置主窗体大小
        winWidth = 600
        winHeight = 500
        # 获取屏幕分辨率
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        # 计算主窗口在屏幕上的坐标
        x = int((screenWidth - winWidth)/ 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置主窗口标题
        window.title("聊天室")
        # 设置主窗口大小
        window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        # 设置窗口宽高固定
        window.resizable(0,0)
        
        left_frame = tk.Frame(window, width=200)
        left_frame.pack(fill=tk.Y, side=tk.LEFT)
        
        scroll_bar = tk.Scrollbar(left_frame)
        scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
        
        self.user_list = tk.StringVar()
        self.list_box = tk.Listbox(left_frame, yscrollcommand = scroll_bar.set, listvariable = self.user_list, state=tk.DISABLED)
        
        self.list_box.pack(expand=1, fill=tk.BOTH)
        scroll_bar.config(command=self.list_box.yview)


        right_frame = tk.Frame(window, bg="yellow")
        right_frame.pack(expand=1, fill=tk.BOTH)

        self.text_box = scrolledtext.ScrolledText(right_frame, state=tk.DISABLED)
        self.text_box.pack(expand=1, fill=tk.BOTH)

        # text_frame = tk.Frame(right_frame, bg="blue")
        # text_frame.pack(expand=1, fill=tk.BOTH)
        # scroll_bar = tk.Scrollbar(text_frame)
        # scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
        # self.text_box = tk.Text(window,font=("宋体", 14) , yscrollcommand = scroll_bar.set, state=tk.DISABLED)
        # self.text_box.pack(side = tk.LEFT)
        # scroll_bar.config(command=self.text_box.yview)

        self.message_var = tk.StringVar()
        entry_box = tk.Entry(right_frame, textvariable=self.message_var)
        entry_box.pack(fill=tk.X, ipady=5)


        
        send_btn = tk.Button(window, text="发送", width=10,bg="blue", fg="white", command=self.send_message)
        send_btn.pack(side=tk.LEFT, pady=10)

        reset_btn = tk.Button(window, text="清空", width=10, bg="red", fg="white", command=self.clear_message)
        reset_btn.pack(side=tk.LEFT, padx = 15)

        # 监听window关闭
        window.protocol("WM_DELETE_WINDOW", self.close_main_window)
        window.mainloop()
    
    def clear_message(self):
        self.message_var.set('')
    
    def set_user_list(self, username_list):
        self.list_box.config(state = tk.NORMAL)
        self.list_box.delete(0, tk.END)
        for i in username_list:
            self.list_box.insert(tk.END, str(i))
        self.list_box.config(state = tk.DISABLED)
        self.window.update()
    
    def get_message(self):
        return self.message_var.get()
    
    def set_user_message(self, data):
        username = data.get('username')
        send_time = data.get('send_time')
        message = data.get('message')
        self.text_box.config(state = tk.NORMAL)
        self.text_box.insert(tk.END, username + ' ' + send_time + '\n')
        self.text_box.insert(tk.END, message + '\n\n')
        self.text_box.config(state = tk.DISABLED)
        self.clear_message()
        
