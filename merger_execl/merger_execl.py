# coding:utf-8

import tkMessageBox
import xlwt
import xlrd
import glob
from numpy import *

# 下面这些变量需要您根据自己的具体情况选择
biaotou = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', \
           ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', \
           ' ', ' ', ' ']

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()



# 在哪里搜索多个表格
filelocation = filedialog.askdirectory() + "\\"
# filelocation = "D:\\soft\\exj\\conf\\"

# 当前文件夹下搜索的文件名后缀
fileform = "xlsx"

# 将合并后的表格存放到的位置
# filedestination = "D:\\soft\\exj\\conf\\"
filedestination = filelocation


# 合并后的表格命名为new
file = "new"


# 首先查找默认文件夹下有多少文档需要整合
filearray = []
for filename in glob.glob(filelocation + "*." + fileform):
    if filename != "new.xlsx":
        filearray.append(filename)

# 以上是从pythonscripts文件夹下读取所有excel表格，并将所有的名字存储到列表filearray
# print("在默认文件夹下有%d个文档" % len(filearray))
ge = len(filearray)
matrix = [None] * ge

# 实现读写数据0
# 下面是将所有文件读数据到三维列表cell[][][]中（不包含表头）
for i in range(ge):
    fname = filearray[i]
    bk = xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_index(0)
    except:
        tkMessageBox.showinfo(title='提示', message='在文件%s中没有找到工作表，读取文件数据失败,要不你换换表格的名字？' % fname)
        # print("在文件%s中没有找到工作表，读取文件数据失败,要不你换换表格的名字？" % fname)
    nrows = sh.nrows
    matrix[i] = [0] * (nrows - 1)

    ncols = sh.ncols
    for m in range(nrows - 1):
        matrix[i][m] = ["0"] * ncols

    for j in range(1, nrows):
        for k in range(0, ncols):
            matrix[i][j - 1][k] = sh.cell(j, k).value



# 下面是写数据到新的表格test.xls中哦
filename = xlwt.Workbook()
sheet = filename.add_sheet("hel")
# 下面是把表头写上
for i in range(0, len(biaotou)):
    sheet.write(0, i, biaotou[i])
# 求和前面的文件一共写了多少行
zh = 1
for i in range(ge):
    for j in range(len(matrix[i])):
        for k in range(len(matrix[i][j])):
            sheet.write(zh, k, matrix[i][j][k])
        zh = zh + 1
tkMessageBox.showinfo(title='提示', message='在默认文件夹下有{}个文档\r\n已经将{}个文件合并成1个文件，并命名为{}.xls.快打开看看正确不？'.format(len(filearray), ge, file))
# print("我已经将%d个文件合并成1个文件，并命名为%s.xls.快打开看看正确不？" % (ge, file))
filename.save(filedestination + file + ".xls")