from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from cleanextractexcel import *
from guiclasses import *

class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)

        self.parent = parent # parent window

        self.initUI()
    def _OpenFile(self):
        """Opens files and displays number of subjects in file"""
        name = askopenfilename()
        self.excelfile = open(name,'r')
        self.ExcelFile = Excel(self.excelfile)
        number_of_sub = self.ExcelFile.get_num_of_subjects()
        self.main_label_textvar = StringVar() #variable to display number of subjects
        self.main_label_textvar.set("There are %d subjects in this file" % number_of_sub)
        self.main_label = Label(self.parent, textvariable=self.main_label_textvar)
        self.main_label.grid(row=0, column=0, sticky=E+W)
        self.excelfile.close()
    def _Headers(self):
        yscroll = Scrollbar(orient=VERTICAL)
        yscroll.grid(row=1, column=1, sticky= N+S)
        xscroll = Scrollbar(orient=HORIZONTAL)
        xscroll.grid(row=2, column=0, sticky=E+W)
        self.main_label_textvar.set("Headers for your File")
        headers = self.ExcelFile.get_headers()
        header_string = ""
        for index in range(len(headers)):
            header_string = header_string + " " + headers[index]
        self.listboxvar = StringVar() # Holds list box values
        self.listboxvar.set(header_string)
        self.main_listbox = Listbox(self.parent, listvariable=self.listboxvar,
                                    yscrollcommand=yscroll.set,
                                    xscrollcommand=xscroll.set)
        self.main_listbox.grid(row=1, column=0,sticky=N+E+S+W)
        yscroll.config(command=self.main_listbox.yview)
        xscroll.config(command=self.main_listbox.xview)
    def _Run(self):
        self.main_listbox.grid(row=1, column=0, sticky=N+E+W+S)
        self.master_allowed = list()
        self.master_not_allowed = list()
        self.master_indeterminate = list()
        size = self.ExcelFile.get_num_of_subjects() / 10
        if size <= 1:
            size = self.ExcelFile.get_num_of_subjects()
        self.master_allowed, self.master_not_allowed, self.master_indeterminate = self.ExcelFile.one_pass(size)
        self._Find()
        pass
    def _Find(self):
        self.main_listbox.config(selectmode=MULTIPLE)
        print type(self.master_indeterminate), type(self.master_allowed), type(self.master_not_allowed), len(self.master_indeterminate)
        print self.master_indeterminate
        self.listboxvar.set(" ".join(self.master_indeterminate))
        self.main_listbox.config(selectbackground="green")
        self.main_label_textvar.set("Please select allowed words")
        self.select_button = Button(self.parent, text="Select Words", command=self._InitialSelect)
        self.select_button.grid(row=2, column=0, sticky=S+E)        

    def _InitialSelect(self):
        self.user_allowed = list()
        allowed_words_index = self.main_listbox.curselection()
        for index in allowed_words_index:
            self.user_allowed.append(self.master_indeterminate[index])
        for word in self.user_allowed:
            self.master_indeterminate.remove(word)
        self.listboxvar.set(" ".join(self.master_indeterminate))
        self.main_listbox.selection_clear(0,self.main_listbox.size())
        self.main_listbox.index(0)
        self.select_button.config(command=self._SecondSelect)
        self.main_label_textvar.set("Please select not allowed words")
        self.main_listbox.config(selectbackground="red")

    def _SecondSelect(self):
        self.user_not_allowed = list()
        not_allowed_words_index = self.main_listbox.curselection()
        for index in not_allowed_words_index:
            self.user_not_allowed.append(self.master_indeterminate[index])
        for word in self.user_not_allowed:
            self.master_indeterminate.remove(word)
        self.ExcelFile.create_user_dictionary(self.user_allowed, self.user_not_allowed)
        self.master_allowed, self.master_not_allowed,self.master_indeterminate = self.ExcelFile.one_pass()
        self.listboxvar.set(" ".join(self.master_indeterminate))
        self.main_listbox.selection_clear(0,self.main_listbox.size())
        self.main_listbox.index(0)
        self.main_label_textvar.set("Please select allowed words")
        showinfo(title="Dictionary Alert",message="Creating Sample User Dictionary")  
        self.select_button.config(command=self._ThirdSelect)
        self.main_listbox.config(selectbackground="green")
                               

    def _ThirdSelect(self):
        self.user_allowed = list()
        allowed_words_index = self.main_listbox.curselection()
        for index in allowed_words_index:
            self.user_allowed.append(self.master_indeterminate[index])
        for word in self.user_allowed:
            self.master_indeterminate.remove(word)
        self.listboxvar.set(" ".join(self.master_indeterminate))
        self.main_listbox.selection_clear(0,self.main_listbox.size())
        self.main_listbox.index(0)
        self.select_button.config(command=self._FinalSelect)
        self.main_label_textvar.set("Please select not allowed words")
        self.main_listbox.config(selectbackground="red")

    def _FinalSelect(self):
        self.user_not_allowed = list()
        not_allowed_index = self.main_listbox.curselection()
        for index in not_allowed_index:
            self.user_not_allowed.append(self.master_indeterminate[index])
        for word in self.user_not_allowed:
            self.master_indeterminate.remove(word)
        for word in self.user_allowed:
            if word not in self.master_allowed:
                self.master_allowed.append(word)
        for word in self.user_not_allowed:
            if word not in self.user_not_allowed:
                self.master_not_allowed.append(word)        
        self.ExcelFile.create_user_dictionary(self.user_allowed, self.user_not_allowed)
        self.select_button.config(text="Create csv", command=self._Message)

    def _Message(self):
        showinfo(title="CSV Creation Alert", message="We are creating your CSV")
        self.ExcelFile.deidentify(self.master_not_allowed, self.master_indeterminate)
        self.ExcelFile.make_csv()
        self.parent.destroy()
        
    def _About(self):
        pass

    def _update_list(self,new_list):
        self.listboxvar.set(" ".join(new_list))
    def _update_select(self):
        self.main_listbox.config(selectmode=MULTIPLE)

    def _update_label(self,text):
        self.main_label_textvar.set(text)
    
    def initUI(self):
        self.main_listbox = Listbox(self.parent)
        self.listboxvar = StringVar()
        self.main_label = Label(self.parent)
        self.select_button = Button(self.parent)
        self.main_label_textvar = StringVar()
        self.parent.title("De-Identification Tool")
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        menu_headers = ['File','Run','Help']
        menu_commands = [[("Open",self._OpenFile),("Show Headers",self._Headers),
                     ("separator",None),("Exit",self.parent.quit)],
                    [("Clean Data File", self._Run)],
                    [("About", self._About)]]
        window_menu = Menus(menu,menu_headers,menu_commands)

def main():

    root = Tk()
    gui = MainFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
        
