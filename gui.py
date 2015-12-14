from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from extractexcel import *

global root
root = Tk()

def OpenFile():
    name = askopenfilename()
    myfile = open(name,'r')
    return myfile
def CleanData(allowed, not_allowed, indeterminate):
    pass
def Run():
    excelfile = OpenFile()
    Excel_File = Excel(excelfile)
    master_allowed, master_not_allowed, master_indeterminate = Excel_File.create_word_lists()
    user_allowed, user_not_allowed = Find(master_allowed, master_not_allowed, master_indeterminate)
    Excel_File.create_user_dicts(user_allowed, user_not_allowed)
    Excel_File.clean_data
    excelfile.close()
def display_list(list_to_display,label_text):
    pass
    
def Find(master_allowed, master_not_allowed, master_indeterminate):
    global root

            
    yScroll = Scrollbar(orient=VERTICAL)
    yScroll.grid(row=0, column=1, sticky=N+S)
    title = Label(root, text='Please select allowed words')
    select = Button(root, text='Select Words', command=SelectWords)
    select.grid(row=
    title.grid(row=0, column=0, sticky=E+W)
    indeterm_list = Listbox(root, yscrollcommand=yScroll.set, activestyle ='dotbox', selectmode=MULTIPLE)
    indeterm_list.grid(row=1, column=0, sticky=N+S+E+W)
    yScroll['command'] = indeterm_list.yview
    spot = 0
    for word in master_indeterminate:
        indeterm_list.insert(spot, word)
        spot = spot + 1
        
    def SelectWords(listbox=indeterm_list):
        print listbox.curselection()

    
    return master_allowed, master_not_allowed    
    

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, indicatoron=0)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
        def state(self):
            return map((lambda var: var.get()), self.vars)

    
def About():
    
    
    showinfo("About","A program to De-Identify data")

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
