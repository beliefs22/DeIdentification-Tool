from Tkinter import *
class CreateLabel:

    def __init__(self,parent,row,column):
        self.parent = parent
        self.row = row
        self.column = column
        self.text = StringVar()
        self.label = Label(self.parent, textvariable=self.text)

    def load(self):
        self.label.grid(row=self.row, column=self.column, sticky=E+W)

    def update(self,newtext):
        self.text.set(newtext)

def main():

    root = Tk()
    main_label = CreateLabel(root,0,0)
    text = "welcome"
    main_label.update(text)
    main_label.load()
    root.mainloop()

if __name__=='__main__':
    main()  
