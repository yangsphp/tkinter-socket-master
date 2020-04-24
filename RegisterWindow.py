from PIL import Image, ImageTk
import tkinter as tk

class RegisterWindow(object):
    def __init__(self, do_cancel, do_register, close_register_window):
        self.do_cancel = do_cancel
        self.do_register = do_register
        self.close_register_window = close_register_window
        
    def show(self):
        window = tk.Tk()
        self.window = window
        # 设置主窗体大小
        winWidth = 250
        winHeight = 240
        # 获取屏幕分辨率
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        # 计算主窗口在屏幕上的坐标
        x = int((screenWidth - winWidth)/ 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置主窗口标题
        window.title("注册")
        # 设置主窗口大小
        window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        # 设置窗口宽高固定
        window.resizable(0,0)
        
        tk.Label(window, text="python聊天室 - 注册", height=2, font=('楷体', 14)).pack(fill = tk.X, side=tk.TOP)
        
        content_frame = tk.Frame(window)
        content_frame.pack()
        
        username_im=Image.open("username.png")
        username_im=ImageTk.PhotoImage(username_im)
        tk.Label(content_frame, image=username_im).grid(row=0, column = 0, pady=12)
        tk.Label(content_frame, text="用户名：").grid(row=0, column = 1)
        self.username_var = tk.StringVar()
        tk.Entry(content_frame, textvariable = self.username_var).grid(row=0, column=2)
        
        password_im=Image.open("password.png")
        password_im=ImageTk.PhotoImage(password_im)
        tk.Label(content_frame, image=password_im).grid(row=1, column = 0)
        tk.Label(content_frame, text="密   码：").grid(row=1, column = 1)
        self.pwd_var = tk.StringVar()
        tk.Entry(content_frame, show="*", textvariable=self.pwd_var).grid(row=1, column=2, pady=12)
        
        rpassword_im=Image.open("password.png")
        rpassword_im=ImageTk.PhotoImage(rpassword_im)
        tk.Label(content_frame, image=rpassword_im).grid(row=2, column = 0)
        tk.Label(content_frame, text="确认密码：").grid(row=2, column = 1)
        self.rpwd_var = tk.StringVar()
        tk.Entry(content_frame, show="*", textvariable=self.rpwd_var).grid(row=2, column=2, pady=12)
        
        btn_frame = tk.Frame(window, padx = 10)
        btn_frame.pack(expand = 1, fill = tk.X)
        tk.Button(btn_frame, text="取消", command=self.do_cancel, width=10).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="注册", command=self.do_register, width=10).pack(side=tk.RIGHT)
        
        window.protocol("WM_DELETE_WINDOW", self.close_register_window)
        window.mainloop()
        
    def get_input(self):
        return self.username_var.get().strip(), self.pwd_var.get().strip(), self.rpwd_var.get().strip()
    
    def close_register_window(self):
        self.window.destroy()
    
# if __name__ == '__main__':
#     RegisterWindow(None, None).show()
