from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from extractexcel import *


def OpenFile():
    name = askopenfilename()
    myfile = open(name,'r')
    return myfile
def CleanData(allowed, not_allowed, indeterminate):
    pass
def Run():
    excelfile = OpenFile()
    Excel_File = Excel(excelfile)
    allowed, not_allowed, indeterminate = Excel_File.create_word_list()
    
    Excel_File.create_final_csv()
    excelfile.close()
    
    
def About(hello):
    print hello
    
    showinfo("About","A program to De-Identify data")


root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
helpmenu = Menu(menu)
runmenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
menu.add_cascade(label="Run", menu=runmenu)
menu.add_cascade(label="Help", menu=helpmenu)
filemenu.add_command(label="Open", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
helpmenu.add_separator()
helpmenu.add_command(label="About", command=About)
runmenu.add_command(label="Clean Data File", command=Run)


mainloop()
