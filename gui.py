from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from extractexcel import *

global root, master_allowed, master_not_allowed, master_indeterminate, user_allowed, user_not_allowed, Excel_File

root = Tk()
master_allowed = []
master_not_allowed = []
master_indeterminate = []
user_allowed = []
user_not_allowed = []

def OpenFile():
    name = askopenfilename()
    myfile = open(name,'r')
    return myfile
def CleanData(allowed, not_allowed, indeterminate):
    pass
def Run():
    global Excel_File
    global master_allowed, master_not_allowed, master_indeterminate,user_allowed,user_not_allowed
    excelfile = OpenFile()
    Excel_File = Excel(excelfile)
    excelfile.close()
    master_allowed, master_not_allowed, master_indeterminate = Excel_File.create_word_lists()
    Find()
    
def display_list(list_to_display,label_text):
    pass
    
def Find():
    global Excel_File
    global root, master_allowed, master_not_allowed, master_indeterminate,user_allowed,user_not_allowed
    
    yScroll = Scrollbar(orient=VERTICAL)
    yScroll.grid(row=1, column=1, sticky=N+S)
    
    listvar = StringVar()
    listvar.set(" ".join(master_indeterminate))
    
    title = Label(root, text='Please select allowed words') 
    title.grid(row=0, column=0, sticky=E+W)
    
    indeterm_list = Listbox(root, listvariable=listvar, yscrollcommand=yScroll.set, activestyle ='dotbox', selectmode=MULTIPLE)
    indeterm_list.grid(row=1, column=0, sticky=N+S+E+W)
    yScroll['command'] = indeterm_list.yview
    select = Button(root, text="Select")
    select.grid(row=2, column=0, sticky=S+E)

    def Message():
        global Excel_File        
        showinfo(title="Alert",message="We are creating CSV")
        Excel_File.clean_data(master_not_allowed,master_indeterminate)
        showinfo(title="All done", message="All done")
        root.destroy()
        
        
    def SelectWords1(listbox=indeterm_list, button=select, label=title):
        global master_indeterminate, user_allowed
        listvar = StringVar()
        allowed_words_index = listbox.curselection()
        for index in allowed_words_index:
            user_allowed.append(master_indeterminate[index])
        for word in user_allowed:
            master_indeterminate.remove(word)
                    
        listvar.set(" ".join(master_indeterminate))
        listbox.config(listvariable=listvar)
        listbox.selection_clear(0,listbox.size())
        button.config(command=SelectWords2)
        title.config(text="Select not allowed words")

    def SelectWords2(listbox=indeterm_list,button = select ):
        global master_indeterminate, user_not_allowed
        not_allowed_words_index =  listbox.curselection()
        for index in not_allowed_words_index:
            user_not_allowed.append(master_indeterminate[index])
        for word in user_not_allowed:
            master_indeterminate.remove(word)
            
        button.config(text="create csv", command=Message)
        Excel_File.create_user_dicts(user_allowed, user_not_allowed)

    select.config(command=SelectWords1)    

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
