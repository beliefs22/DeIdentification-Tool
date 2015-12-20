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
        self.textvar = StringVar() #variable to display number of subjects
        self.textvar.set("There are %d subjects in this file" % number_of_sub)
        self.main_label = Label(self.parent, textvariable=self.textvar)
        self.main_label.grid(row=0, column=0, sticky=E+W)
        self.excelfile.close()
    def _Headers(self):
        yscroll = Scrollbar(orient=VERTICAL)
        yscroll.grid(row=1, column=1, sticky= N+S)
        xscroll = Scrollbar(orient=HORIZONTAL)
        xscroll.grid(row=2, column=0, sticky=E+W)
        self.textvar.set("Headers for your File")
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
        self.master_allowed, self.master_not_allowed,
        self.master_indeterminate = self.ExcelFile.first_pass()
        self.Find()
        pass
    def Find(self):
        self.main_listbox.config(selectmode=MULTIPLE)
        self.listboxvar.set(" ".join(self.master_indeterminate))
        self.textvar.set("Please select allowed words")

        self.select_button = Button(self.parent,text="Select Words")
        self.select_button.grid(row=2, column=0, sticky=S+E)

    def InitialSelect():
        pass

    
        
        
        
    def _About(self):
        pass

    def _update_list(self,new_list):
        self.listboxvar.set(" ".join(new_list))
    def _update_select(self):
        self.main_listbox.config(selectmode=MULTIPLE)

    def _update_label(self,text):
        self.textvar.set(text)
    
    def initUI(self):
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
        
