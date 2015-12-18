from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from extractexcel import *
from guiclasses import *
global root, master_allowed, master_not_allowed, master_indeterminate
global user_allowed, user_not_allowed, Excel_File

root = Tk()
master_allowed = []
master_not_allowed = []
master_indeterminate = []
user_allowed = []
user_not_allowed = []

def OpenFile():
    global root, Excel_File
    name = askopenfilename()
    myfile = open(name,'r')
    Excel_File = Excel(myfile)
    number_of_sub = Excel_File.show_subjects()    
    textvar = StringVar()
    textvar.set("There are %d subjects in this file" % number_of_sub) 
    sub_label = Label(root, textvariable=textvar)
    sub_label.grid(row=1, column=0, sticky=N+E+S+W)    
    myfile.close()
    return myfile


def Run():
    global Excel_File
    global master_allowed, master_not_allowed
    global master_indeterminate, user_allowed,user_not_allowed
    master_allowed, master_not_allowed, \
                    master_indeterminate = Excel_File.create_word_lists()
    Find()
    
def Find():
    global Excel_File
    global root, master_allowed, master_not_allowed
    global master_indeterminate,user_allowed,user_not_allowed
    
    yScroll = Scrollbar(orient=VERTICAL)
    yScroll.grid(row=1, column=1, sticky=N+S)
    
    listvar = StringVar()
    listvar.set(" ".join(master_indeterminate))
    
    title = Label(root, text='Please select allowed words') 
    title.grid(row=0, column=0, sticky=E+W)
    
    indeterm_list = Listbox(root, listvariable=listvar, yscrollcommand=yScroll.set, \
                            activestyle ='dotbox', selectmode=MULTIPLE)
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

def Headers():
    global Excel_File, root
    yscroll = Scrollbar(orient=VERTICAL)
    yscroll.grid(row=1, column=1, sticky=N+S)
    title = Label(root, text='Headers for your File')
    title.grid(row=0, column=0, sticky=E+W)
    headers = Excel_File.show_headers()
    header_string = ""
    for pair in headers:
        header_string = header_string + " " + pair[1]
    head_var = StringVar()
    head_var.set(header_string)
    header_list = Listbox(root, listvariable=head_var, yscrollcommand=yscroll.set)
    header_list.grid(row=1,column=0,sticky=N+E+S+W)
    yscroll.config(command=header_list.yview)
    
        
def About():  
    
    showinfo("About","A program to De-Identify data")

def Quits():
    global root
    root.quit()

menu = Menu(root)
root.config(menu=menu)
headers = ['File','Run','Help']
commands = [[("Open", OpenFile), ("Show Headers", Headers),("separator",None),("Exit",Quits)]\
            ,[("Clean Data File", Run)],[("About",About)]]
window_menu = Menus(menu,headers,commands)
mainloop()
