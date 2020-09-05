# coding: utf-8
# %%
from bs4 import BeautifulSoup
from urllib import parse
import requests
import json
import re
import base64
import sys
import os
import tkinter
import threading
import webbrowser
import emoji
from icon import img
from tkinter.ttk import Treeview
from tkinter import Tk, Scrollbar, Frame, ttk, messagebox
program_directory = sys.path[0]

root = Tk()
root.geometry('1095x700+400+200')
root.resizable(False, False)
root.title('南台消息查詢程式')
tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()
root.iconbitmap('tmp.ico')
os.remove("tmp.ico")

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def exit_func():
    MsgBox = tkinter.messagebox.askquestion('確認', '要離開程式了嗎?', icon='warning')
    if MsgBox == 'yes':
        root.destroy()
    else:
        tkinter.messagebox.showinfo('返回', '繼續查詢')


def load_4page_btn_func():
    if tree.get_children():
        for i in tree.get_children():
            tree.delete(i)
    single_page(1)
    single_page(2)
    single_page(3)
    single_page(4)


def load_4page_btn_func_thread():
    t = threading.Thread(target=load_4page_btn_func)
    t.start()


def program_info_btn_func():
    MsgBox = tkinter.messagebox.askquestion(
        "南台消息查詢程式", "程式版本 : V 0.0.4\n是否前往 GITHUB?", icon='warning')
    if MsgBox == 'yes':
        webbrowser.open(
            "https://github.com/vincent-chang-rightfighter/PYTHON-STUSTNEWS-VIEWER")
    else:
        tkinter.messagebox.showinfo('返回', '繼續查詢')


def clear_treeview_btn_func():
    if tree.get_children():
        for i in tree.get_children():
            tree.delete(i)


def search_btn_func():
    X = search_entrytext.get()
    if tree.get_children():
        for i in tree.get_children():
            tree.delete(i)
    search_page(X)


def search_btn_func_thread():
    t1 = threading.Thread(target=search_btn_func)
    t1.start()


def treeview_click_func(event):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        string_ = item_text[3]
        webbrowser.open(string_)


def combobox_click_func():
    cv = int(page_combobox.get())
    if tree.get_children():
        for i in tree.get_children():
            tree.delete(i)
    single_page(cv)


def combobox_click_func_thread(event):
    t2 = threading.Thread(target=combobox_click_func)
    t2.start()


def single_page(n):
    res = requests.get(
        "https://news.stust.edu.tw/User/RwdNewsList.aspx?page="+str(n), headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.select('tbody .hoverable'):
        s = item.a.get('href')
        hyper = "https://news.stust.edu.tw"+s[2:]
        title = emoji.demojize(item.select('td a')[0].text)
        title_new = re.sub(r':(.*?):', '', title).strip()
        tree.insert("", "end",  values=(title_new, item.select(
            'td.hide-on-small-only.center span')[0].text,  item.select('td.center span')[3].text,  hyper))


def search_page(x):
    n = 1
    res = requests.get("https://news.stust.edu.tw/User/RwdNewsList.aspx?page="+str(n) +
                       "&classid=&DDLItem=%E5%85%AC%E5%91%8A%E6%A8%99%E9%A1%8C&SCont="+str(parse.quote(x.encode('utf8')))+"&SSdate=&SEdate=&dept=", headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.select('tbody .hoverable'):
        s = item.a.get('href')
        hyper = "https://news.stust.edu.tw"+s[2:]
        title = emoji.demojize(item.select('td a')[0].text)
        title_new = re.sub(r':(.*?):', '', title).strip()
        tree.insert("",  "end",  values=(title_new, item.select(
            'td.hide-on-small-only.center span')[0].text,  item.select('td.center span')[3].text,  hyper))

# GUI SETTINGS

# button
load_4page_btn = tkinter.Button(text="載入第1頁至第4頁", command=lambda: [
    load_4page_btn_func_thread()], relief=tkinter.GROOVE)
exit_btn = tkinter.Button(text="Click & Quit", command=lambda: [
    exit_func()], relief=tkinter.GROOVE)
program_info_btn = tkinter.Button(text="應用程式詳情", command=lambda: [
    program_info_btn_func()], relief=tkinter.GROOVE)
clear_treeview_btn = tkinter.Button(text="清空列表", command=lambda: [
    clear_treeview_btn_func()], relief=tkinter.GROOVE)
search_btn = tkinter.Button(text="搜尋", command=lambda: [
    search_btn_func_thread()], relief=tkinter.GROOVE)
    
load_4page_btn.place(x=10, y=20)
exit_btn.place(x=910, y=20)
program_info_btn.place(x=990, y=20)
clear_treeview_btn.place(x=850, y=20)
search_btn.place(x=690, y=20)

# label
treeview_guide_label = tkinter.Label(text="點擊兩下開啟列表詳情網頁")
page_label1 = tkinter.Label(text="單頁顯示第 :")
page_label2 = tkinter.Label(text="頁")
search_label = tkinter.Label(text="標題關鍵字 :")

treeview_guide_label.place(x=10, y=70)
page_label1.place(x=200, y=23)
page_label2.place(x=360, y=23)
search_label.place(x=450, y=23)

# combobox
page_combobox = ttk.Combobox(root, state="readonly", width=7)
page_combobox["value"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
page_combobox.current(0)
page_combobox.place(x=280, y=23)
page_combobox.bind("<<ComboboxSelected>>", combobox_click_func_thread)

search_entrytext = tkinter.Entry(root, width=20, relief=tkinter.SUNKEN)
search_entrytext.place(x=530, y=25)

# frame
frame = Frame(root)
frame.place(x=10, y=100, width=1080, height=580)
scrollBar = tkinter.Scrollbar(frame)
scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# treeview
tree = Treeview(frame, columns=('c1', 'c2', 'c3', 'c4'),
                show="headings", yscrollcommand=scrollBar.set)
tree.column('c1', width=860, stretch=False)
tree.column('c2', width=120, stretch=False)
tree.column('c3', width=80, stretch=False)
tree.column('c4', width=0, stretch=False)
tree.heading('c1', text='標題', anchor='w')
tree.heading('c2', text='公告單位', anchor='w')
tree.heading('c3', text='公告日期', anchor='w')
tree.heading('c4', text='網址', anchor='w')
tree.pack(side=tkinter.LEFT, fill=tkinter.Y)
tree.bind('<Double-Button-1>', treeview_click_func)
scrollBar.config(command=tree.yview)
root.protocol("WM_DELETE_WINDOW", exit_func)
root.mainloop()

