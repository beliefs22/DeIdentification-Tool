from Tkinter import *
class CreateListbox:

    def __init__(self, parent, row, column):
        self.parent = parent
        self.yscroll = Scrollbar(orient=VERTICAL)        
        self.xscroll = Scrollbar(orient=HORIZONTAL)        
        self.listboxvar = StringVar() # Holds list box values
        self.main_listbox = Listbox(self.parent,
                                    listvariable=self.listboxvar,
                                    yscrollcommand=self.yscroll.set,
                                    xscrollcommand=self.xscroll.set,
                                    selectmode=MULTIPLE)
        self.yscroll.config(command=self.main_listbox.yview)
        self.xscroll.config(command=self.main_listbox.xview)
        self.row = row
        self.column = column
        self.top = self.main_listbox.winfo_toplevel()
        self.top.rowconfigure(self.row, weight=1)
        self.top.columnconfigure(self.column, weight=1)
        self.main_listbox.rowconfigure(self.row, weight=1)
        self.main_listbox.columnconfigure(self.column, weight=1)


    def update(self,text):
        """Update listbox var with given text.

        Args:
            text (str): string represenation of list for listbox to display

        """

        self.listboxvar.set(text)
    def update_color(self,color):
        """Update color to given color.

        Args:
            color (str): color to change to
            
        """
        self.main_listbox.config(selectbackground=color)

    def load(self):
        """Load Listbox into window at Defaults to initial values.

        Args:
            row (int): row position of Listbox
            column (int): column position of Listbox

        """
        self.xscroll.grid(row=self.row+1, column=self.column, sticky=E+W)
        self.yscroll.grid(row=self.row, column=self.column+1, sticky=N+S)
        self.main_listbox.grid(row=self.row, column=self.column, sticky=N+W+S+E)

    def clear(self):
        """Clear list"""

        self.main_listbox.selection_clear(0, self.main_listbox.size())

    def get_selected(self):
        """Return list of words that are selected"""
        return self.main_listbox.curselection()
    

def main():

    root = Tk()

    headers = "These are Some Headers to put in list"
    main_list_box = CreateListbox(root, 0, 0)
    main_list_box.load()
    main_list_box.update(headers)
    root.mainloop()

if __name__=='__main__':
    main()

    
