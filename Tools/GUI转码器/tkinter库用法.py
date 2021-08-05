import tkinter as tk


def main():
    string = var_txt1.get()
    string = "this is a test: " + string
    var_txt2.set(string)



# 定义GUI主体框架
window = tk.Tk()
window.title('转码器')
window.geometry('610x650')

# 定义输入的变量
var_txt1 = tk.StringVar()
var_txt2 = tk.StringVar()

# 设置画布
tk.Label(window, text='代转字符串:', font=('华文仿宋', 15)).place(x=10, y=20)
tk.Label(window, text='测试字符串:', font=('华文仿宋', 15)).place(x=10, y=50)

# 设置输入框的位置
_var_txt1 = tk.Entry(window, textvariable=var_txt1, width=45)
_var_txt1.place(x=130, y=20)

_var_txt2 = tk.Entry(window, textvariable=var_txt2, width=45)
_var_txt2.place(x=10, y=80)

# 定义button
button_text = tk.Button(window, text='转码', command=main)
button_text.place(x=510, y=20)

window.mainloop()
