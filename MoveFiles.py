from tkinter import *
from tkinter import font,filedialog
import tkinter as tk
from os import *
import os as os
from shutil import *
import shutil as shutil
import time as time 
import sqlite3

db = sqlite3.connect("Text_Files.db")


class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)

        self.master = master
        self.master.minsize(890,342)
        self.master.title("Move text files to new directory")
        load_gui(self)


def load_gui(self):

    standard_font=font.Font(size=14)

    entry_font=font.Font(size=18,weight="bold")
    
    Font_Size = tk.StringVar(value='')
    
    self.btn_source = tk.Button(self.master,width=15,font=standard_font,text="Source...",command=lambda: select_file1(self))
    self.btn_source.grid(row=1,column=0,padx=(25,0),pady=(100,0))
    self.btn_destin = tk.Button(self.master,width=15,font=standard_font,text="Destination...",command=lambda: select_file2(self))
    self.btn_destin.grid(row=2,column=0,padx=(25,0),pady=(20,0))
    self.btn_move = tk.Button(self.master,width=15,font=standard_font,text="Move Text Files...",command=lambda: move_file(self))
    self.btn_move.grid(row=3,column=0,padx=(25,0),ipady=15,pady=(20,0))

      
    self.txt_source = tk.Text(self.master,width=60,height=2)
    self.txt_source.grid(row=1,column=1,columnspan=2,padx=(55,0),pady=(100,0),sticky=W)
    self.txt_destin = tk.Text(self.master,width=60,heigh=2)
    self.txt_destin.grid(row=2,column=1,columnspan=2,padx=(55,0),pady=(15,0),sticky=W)

def select_file1(self):
    directory1 = filedialog.askdirectory()
    self.txt_source.insert(tk.INSERT,directory1)

def select_file2(self):
    directory2 = filedialog.askdirectory()
    self.txt_destin.insert(tk.INSERT,directory2)

def move_file(self):
    directory3 = self.txt_source.get('1.0','end-1c')
    directory4 = self.txt_destin.get('1.0','end-1c')
    file_list = os.listdir(directory3)
    i = 0
    db_list = []
    while i >= 0:
        if file_list[i].endswith("txt"):
            db_list.append(file_list[i])
            i +=1
        else: i +=1
        if file_list[i]==file_list[-1] and file_list[i].endswith("txt"):
            db_list.append(file_list[i])
            break
        if file_list[i]==file_list[-1] and not file_list[i].endswith("txt"):
            break
    for item in db_list:
        src = os.path.join(directory3,item)
        dst = directory4
        newfile = shutil.move(src,dst)
        mod_time = os.path.getmtime(newfile)
        real_time = time.ctime(mod_time)
        mod_timesql = str(mod_time)
        print("\nFilename:{}\nM time:{}\nLast Modified Time in Real Time:{}".format(item,mod_time,real_time))
        with db:
                cur = db.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS tbl_Files( \
                FileName TEXT, \
                ModTime TEXT, \
                RealTimeModTime TEXT)")
                cur.execute("INSERT INTO tbl_Files Values (?,?,?)",(item,mod_time,real_time))
                db.commit()
    db.close()
        
                

if __name__== "__main__":
    root = tk.Tk()
    App = Window(root)
    root.mainloop()

