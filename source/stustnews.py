#!/usr/bin/env python
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
import textwrap
from icon import img
from tkinter.ttk import Treeview
from tkinter import Tk, Scrollbar, Frame, StringVar, PhotoImage, ttk, messagebox, font
program_directory = sys.path[0]
string_ = ""

root = Tk()
style = ttk.Style()
root.geometry('1100x800+100+100')
root.resizable(False, False)
root.title('南台消息查詢程式')
tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()
root.iconbitmap('tmp.ico')
os.remove("tmp.ico")

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

fontset = font.Font(family="Microsoft JhengHei", size=11, weight="normal")
fontset2 = font.Font(family="Microsoft JhengHei", size=12, weight="normal")
LARGE_FONT = 12
style.configure("Treeview.Heading", font=("Microsoft JhengHei", LARGE_FONT),
                rowheight=int(LARGE_FONT*2.5))
style.configure("Treeview", font=("Microsoft JhengHei", LARGE_FONT),
                rowheight=int(LARGE_FONT*4.5))


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
    single_page_crawler(1)
    single_page_crawler(2)
    single_page_crawler(3)
    single_page_crawler(4)


def load_4page_btn_func_thread():
    t = threading.Thread(target=load_4page_btn_func)
    t.start()


def program_info_btn_func():
    MsgBox = tkinter.messagebox.askquestion(
        "南台消息查詢程式", "程式版本 : V 0.0.5\n是否前往GITHUB?", icon='warning')
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
    search_page_crawler(X)
    search_entrytext.delete(0, 'end')


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
    single_page_crawler(cv)


def combobox_click_func_thread(event):
    t2 = threading.Thread(target=combobox_click_func)
    t2.start()


def wrap(string, lenght=50):
    return '\n'.join(textwrap.wrap(string, lenght))


def single_page_crawler(n):
    res = requests.get(
        "https://news.stust.edu.tw/User/RwdNewsList.aspx?page="+str(n), headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.select('tbody .hoverable'):
        s = item.a.get('href')
        hyper = "https://news.stust.edu.tw"+s[2:]
        title = emoji.demojize(item.select('td a')[0].text)
        title_new = re.sub(r':(.*?):', '', title).strip()
        tree.insert("", "end",  values=(wrap(title_new), item.select(
            'td.hide-on-small-only.center span')[0].text,  item.select('td.center span')[3].text,  hyper))


def search_page_crawler(x):
    n = 1
    res = requests.get("https://news.stust.edu.tw/User/RwdNewsList.aspx?page="+str(n) +
                       "&classid=&DDLItem=%E5%85%AC%E5%91%8A%E6%A8%99%E9%A1%8C&SCont="+str(parse.quote(x.encode('utf8')))+"&SSdate=&SEdate=&dept=", headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.select('tbody .hoverable'):
        s = item.a.get('href')
        hyper = "https://news.stust.edu.tw"+s[2:]
        title = emoji.demojize(item.select('td a')[0].text)
        title_new = re.sub(r':(.*?):', '', title).strip()
        tree.insert("",  "end",  values=(wrap(title_new), item.select(
            'td.hide-on-small-only.center span')[0].text,  item.select('td.center span')[3].text,  hyper))

# GUI SETTINGS

# button
load_4page_btn = tkinter.Button(text="載入第1頁至第4頁", command=lambda: [
    load_4page_btn_func_thread()], relief=tkinter.GROOVE, font=fontset)
exit_btn = tkinter.Button(text="Click & Quit", command=lambda: [
    exit_func()], relief=tkinter.GROOVE, font=fontset)
program_info_btn = tkinter.Button(text="應用程式詳情", command=lambda: [
    program_info_btn_func()], relief=tkinter.GROOVE, font=fontset)
clear_treeview_btn = tkinter.Button(text="清空列表", command=lambda: [
    clear_treeview_btn_func()], relief=tkinter.GROOVE, font=fontset)
search_btn = tkinter.Button(text="搜尋", command=lambda: [
    search_btn_func_thread()], relief=tkinter.GROOVE, font=fontset)
load_4page_btn.place(x=10, y=20)
search_btn.place(x=670, y=20)
clear_treeview_btn.place(x=803, y=20)
exit_btn.place(x=880, y=20)
program_info_btn.place(x=980, y=20)

# label
treeview_guide_label = tkinter.Label(text="點擊兩下開啟列表詳情網頁", font=fontset)
page_label1 = tkinter.Label(text="單頁顯示第 :", font=fontset)
page_label2 = tkinter.Label(text="頁", font=fontset)
search_label = tkinter.Label(text="標題關鍵字 :", font=fontset)

treeview_guide_label.place(x=8, y=70)
page_label1.place(x=180, y=23)
page_label2.place(x=330, y=23)
search_label.place(x=430, y=23)

# combobox
page_combobox = ttk.Combobox(root, state="readonly", width=4, font=fontset)
page_combobox["value"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
page_combobox.current(0)
page_combobox.place(x=270, y=23)
page_combobox.bind("<<ComboboxSelected>>", combobox_click_func_thread)

search_entrytext = tkinter.Entry(
    root, width=15, relief=tkinter.SUNKEN, font=fontset2)
search_entrytext.place(x=520, y=25)

# frame
frame = Frame(root)
frame.place(x=10, y=100, width=1080, height=680)
scrollBar = tkinter.Scrollbar(frame)
scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# treeview
tree = Treeview(frame, columns=('c1', 'c2', 'c3', 'c4'),
                show="headings", yscrollcommand=scrollBar.set)
tree.column('c1', width=825, stretch=False)
tree.column('c2', width=135, stretch=False)
tree.column('c3', width=100, stretch=False)
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

