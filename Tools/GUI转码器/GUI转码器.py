import tkinter as tk
from urllib import parse
import base64
import binascii
from hashlib import md5
import html

# 1. 定义url编码函数
def url_encoding(string):
    return parse.quote(string)

# 2. 定义url解码函数
def url_decoding():
    url = var_url.get()
    var_txt.set(parse.unquote(url))


# 3. 定义base64编码函数
def base64_encoding(string):
    string = base64.b64encode(string.encode())
    return string.decode()

# 4. 定义base64解码函数
def base64_decoding():
    string = var_enb64.get()
    string = base64.b64decode(string.encode())
    var_deb64.set(string)

# 5. 定义Hex 十六进制编码函数
def hex_encoding(string):
    Hex = binascii.b2a_hex(string.encode())
    return "0x"+Hex.decode()

# 6. 定义Hex 十六进制解码函数
def hex_decoding():
    Hex = var_hex.get()
    string = Hex.replace("0x", "")
    string = binascii.a2b_hex(string)
    var_txt.set(string.decode())

# 7. 定义Ascii 编码函数
def ascii_encoding(string):
    Ascii = list(map(ord, string))
    return Ascii

# 8. 定义Ascii解码函数
# 请将要解码的Ascii写成列表形式
def ascii_decoding():
    Ascii = []
    for i in var_ascii.get().split(' '):
        Ascii.append(int(i))
    string = list(map(chr, Ascii))
    var_txt.set(''.join(string))

# 9. 定义md5加密函数
def md5_enc(string):
    return md5(string.encode()).hexdigest()

# 10. 定义unicode编码函数
# 关键：string.encode('unicode_escape')
def unicode_encoding(string):
    return string.encode('unicode_escape').decode()

# 11. 定义unicode解码函数
def unicode_decoding():
    string = var_unicode.get()
    var_txt.set(string.encode().decode('unicode_escape'))

# 12. 定义html实体编码函数
def htmlescape(string):
    return html.escape(string)

# 13. 定义html实体解码函数
def htmlunescape():
    string = var_html.get()
    var_txt.set(html.unescape(string))

def main():
    # 将编码后的值替换到GUI相应的位置
    string = var_txt.get()
    var_url.set(url_encoding(string))
    var_html.set(htmlescape(string))
    var_unicode.set(unicode_encoding(string))
    var_hex.set(hex_encoding(string))
    var_ascii.set(ascii_encoding(string))
    var_md5.set(md5_enc(string))
    var_enb64.set(base64_encoding(string))


# 定义GUI主体框架
window = tk.Tk()
window.title('转码器')
window.geometry('610x650')

# 定义输入的变量
var_txt = tk.StringVar()
var_url = tk.StringVar()
var_enb64 = tk.StringVar()
var_deb64 = tk.StringVar()
var_hex = tk.StringVar()
var_ascii = tk.StringVar()
var_md5 = tk.StringVar()
var_unicode = tk.StringVar()
var_html = tk.StringVar()

# 设置画布
tk.Label(window, text='待转字符串:', font=('Arial', 15)).place(x=10, y=20)
tk.Label(window, text='url编码:', font=('Arial', 15)).place(x=10, y=50)
tk.Label(window, text='html编码:', font=('Arial', 15)).place(x=10, y=120)
tk.Label(window, text='unicode编码:', font=('Arial', 15)).place(x=10, y=190)
tk.Label(window, text='十六进制:', font=('Arial', 15)).place(x=10, y=260)
tk.Label(window, text='Ascii编码:', font=('Arial', 15)).place(x=10, y=330)
tk.Label(window, text='md5加密:', font=('Arial', 15)).place(x=10, y=400)
tk.Label(window, text='base64编码:', font=('Arial', 15)).place(x=10, y=470)
tk.Label(window, text='base64解码:', font=('Arial', 15)).place(x=10, y=540)

# 设置输入框位置
_var_txt = tk.Entry(window, textvariable=var_txt, width=45)
_var_txt.place(x=130, y=20)

_var_url = tk.Entry(window,textvariable=var_url, width=60)
_var_url.place(x=10, y=80)

_var_html = tk.Entry(window, textvariable=var_html, width=60)
_var_html.place(x=10, y=150)

_var_unicode = tk.Entry(window, textvariable=var_unicode, width=60)
_var_unicode.place(x=10, y=220)

_var_hex = tk.Entry(window, textvariable=var_hex, width=60)
_var_hex.place(x=10, y=290)

_var_ascii = tk.Entry(window, textvariable=var_ascii, width=60)
_var_ascii.place(x=10, y=360)

_var_md5 = tk.Entry(window, textvariable=var_md5, width=60)
_var_md5.place(x=10, y=430)

_var_base64_encode = tk.Entry(window,textvariable=var_enb64, width=60)
_var_base64_encode.place(x=10, y=500)

_var_base64_decode = tk.Entry(window, textvariable=var_deb64, width=60)
_var_base64_decode.place(x=10, y=570)


# 定义button
button_text = tk.Button(window, text='转码', command=main)
button_text.place(x=510, y=20)

button_url = tk.Button(window, text='url解码', command=url_decoding)
button_url.place(x=510, y=80)

button_html = tk.Button(window, text='html解码', command=htmlunescape)
button_html.place(x=510, y=150)

button_unicode = tk.Button(window, text='unicode解码', command=unicode_decoding)
button_unicode.place(x=510, y=220)

button_hex = tk.Button(window, text='hex解码', command=hex_decoding)
button_hex.place(x=510, y=290)

button_ascii = tk.Button(window, text='Ascii解码', command=ascii_decoding)
button_ascii.place(x=510, y=360)

button_base64 = tk.Button(window, text='base64解码', command=base64_decoding)
button_base64.place(x=510, y=500)

window.mainloop()







