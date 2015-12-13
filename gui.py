from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from extractexcel import *

def NewFile():
    print "New File!"
def OpenFile():
    name = askopenfilename()
    myfile = open(name,'r')
    return myfile

def Run():
    excelfile = OpenFile()
    Excel_File = Excel(excelfile)
    Excel_File.clean_data()
    Excel_File.create_final_csv()
    excelfile.close()
    
    
def About():
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
