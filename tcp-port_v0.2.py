# coding:utf-8

# 对话框选择文件

import Tkinter
import tkFileDialog
import tkMessageBox


from tkinter import *


def getInput(title, message):
    def return_callback(event):
        # print('quit...')
        root.quit()
    def close_callback():
        root.quit()
    root = Tk(className=title)
    root.wm_attributes('-topmost', 1)
    screenwidth, screenheight = root.maxsize()
    width = 300
    height = 100
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)
    root.resizable(0, 0)
    lable = Label(root, height=2)
    lable['text'] = message
    lable.pack()
    entry = Entry(root)
    entry.bind('<Return>', return_callback)
    entry.pack()
    entry.focus_set()
    root.protocol("WM_DELETE_WINDOW", close_callback)
    root.mainloop()
    str = entry.get()
    root.destroy()
    return str



# 选择端口文件
root = Tkinter.Tk()
root.withdraw()
file_path = tkFileDialog.askopenfilename()

# 打开选择的文件
# f = open(r'C:\Users\feiboke\Desktop\port.txt', 'r')
f = open(file_path, 'r')
port_list = f.readlines()
f.close()


# 打开新的文件保存
if file_path.endswith('.txt'):
    save_file = file_path.split('.txt')[0] + '_tcp.txt'
    # new_f = codecs.open(save_file, 'w', encoding='utf-8')
    new_f = open(save_file, 'w')
else:
    tkMessageBox.showerror(title='警告', message='请选择正确的txt文件 ')
    sys.exit()


# 输入源IP
server_ip = getInput("请输入IP", "源服务器IP")
server_ip = server_ip.strip()


# 判断输入IP是否合理
if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", server_ip):
    for port in port_list:
        port = port.strip()
        if port.strip() == "":
            continue
        else:
            # 判断端口是否为数字
            if not re.match('^\d+$', port):
                tkMessageBox.showerror(title='警告', message='port文件中存在非数字端口，请检查')
                sys.exit(1)
            # 判断端口是都小于65535
            elif  int(port) > 65535 or int(port) < 0:
                tkMessageBox.showerror(title='警告', message='port文件中存在非1-65534的端口，请检查')
                sys.exit(1)
            # 判断是否包含80
            elif int(port) == 80:
                tkMessageBox.showerror(title='警告', message='port文件中存在80端口，请检查')
                sys.exit(1)
            # 判断是否包含已用端口
            elif int(port) == 63333 or int(port) == 62222:
                tkMessageBox.showerror(title='警告', message='port文件中存在占用端口，请检查')
                sys.exit(1)
            else:
                # 处理字符并保存
                msg = "#" + port + "\r\n"
                msg = "{0}{1}:{2}\r\n".format(msg, server_ip, port)
                # print msg
                new_f.write(msg)
    tkMessageBox.showinfo(title='提示', message='完成，请查看port_tcp.txt')
    new_f.close()
else:
    tkMessageBox.showerror(title='警告', message='请输入正确的ip地址')
    sys.exit(1)