#!/usr/bin/env python
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
import extractexcel as excel
from guiclasses import *
import csv


class MainFrame(Frame):
    """GUI for DeIdentification Program"""

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent  # parent window
        self.initUI()

    def initUI(self):
        self.main_listbox = listboxclass.CreateListbox(self.parent, 1, 0)
        self.main_label = labelclass.CreateLabel(self.parent, 0, 0)
        self.select_button = Button(self.parent)  # used to select words
        self.parent.title("De-Identification Tool")
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        menu_headers = ['File', 'Run', 'Help']
        menu_commands = [[("Open", self._OpenFile), ("Show Headers", self._Headers),
                          ("separator", None), ("Exit", self.parent.quit)],
                         [("Clean Data File", self._Run)],
                         [("About", self._About)]]
        window_menu = menuclass.CreateMenus(menu, menu_headers, menu_commands)

    def _OpenFile(self):
        """Opens files and displays number of subjects in file"""
        name = askopenfilename()
        myfile = open(name,'r')
        self.excelfile = csv.reader(myfile)
        self.ExcelFile = excel.Excel(self.excelfile)
        number_of_sub = self.ExcelFile.get_num_of_subjects()
        self.main_label.update("There are %d subjects in this file" \
                               % number_of_sub)
        self.main_label.load()
        myfile.close()

    def _Headers(self):
        """Displays Headers for file"""
        try:
            self.main_label.update("Headers for your File")
            self.main_listbox.load()
            headers = self.ExcelFile.get_headers()
            header_string = ""
            for index in range(len(headers)):
                header_string = header_string + " " + headers[index]
            self.main_listbox.update(header_string)
        except AttributeError as e:
            self._OpenFile()
            self._Headers()

    def _Run(self):
        """Begins DeIdentification process"""
        try:
            self.master_allowed = list()
            self.master_not_allowed = list()
            self.master_indeterminate = list()
            size = self.ExcelFile.get_num_of_subjects() / 10
            if size <= 1:
                size = self.ExcelFile.get_num_of_subjects()
            self.main_label.update("Doing first pass")
            self.master_allowed, self.master_not_allowed, self.master_indeterminate = \
                self.ExcelFile.one_pass(size)
            self._Find()
        except AttributeError as e:
            self._OpenFile()
            self._Run()

    def _Find(self):
        """Looks for user known words"""
        self.main_listbox.update(" ".join(self.master_indeterminate))
        self.main_listbox.load()
        self.main_listbox.update_color("green")
        self.main_label.update("Please select allowed words")
        self.select_button = Button(self.parent, text="Select Words",
                                    command=self._InitialSelect)
        self.select_button.grid(row=2, column=0, sticky=S + E)

    def _InitialSelect(self):
        """After initial select of known words"""
        self.user_allowed = list()
        allowed_words_index = self.main_listbox.get_selected()
        for index in allowed_words_index:
            self.user_allowed.append(self.master_indeterminate[index])
        for word in self.user_allowed:
            self.master_indeterminate.remove(word)
        self.main_listbox.update(" ".join(self.master_indeterminate))
        self.main_listbox.clear()
        self.select_button.config(command=self._SecondSelect)
        self.main_label.update("Please select not allowed words")
        self.main_listbox.update_color("red")

    def _SecondSelect(self):
        """I'm not sure how to doc guis"""
        self.user_not_allowed = list()
        not_allowed_words_index = self.main_listbox.get_selected()
        for index in not_allowed_words_index:
            self.user_not_allowed.append(self.master_indeterminate[index])
        for word in self.user_not_allowed:
            self.master_indeterminate.remove(word)
        self.ExcelFile.create_user_dictionary(self.user_allowed, self.user_not_allowed)
        self.master_allowed, self.master_not_allowed, self.master_indeterminate \
            = self.ExcelFile.one_pass()
        self.main_listbox.update(" ".join(self.master_indeterminate))
        self.main_listbox.clear()
        self.main_label.update("Please select allowed words")
        showinfo(title="Dictionary Alert", message="Creating Sample User Dictionary")
        self.select_button.config(command=self._ThirdSelect)
        self.main_listbox.update_color("green")

    def _ThirdSelect(self):
        self.user_allowed = list()
        allowed_words_index = self.main_listbox.get_selected()
        for index in allowed_words_index:
            self.user_allowed.append(self.master_indeterminate[index])
        for word in self.user_allowed:
            self.master_indeterminate.remove(word)
        self.main_listbox.update(" ".join(self.master_indeterminate))
        self.main_listbox.clear()
        self.select_button.config(command=self._FinalSelect)
        self.main_label.update("Please select not allowed words")
        self.main_listbox.update_color("red")

    def _FinalSelect(self):
        self.user_not_allowed = list()
        not_allowed_index = self.main_listbox.get_selected()
        for index in not_allowed_index:
            self.user_not_allowed.append(self.master_indeterminate[index])
        for word in self.user_not_allowed:
            if word not in self.master_not_allowed:
                self.master_not_allowed.append(word)
        for word in self.user_not_allowed:
            self.master_indeterminate.remove(word)
        for word in self.user_allowed:
            if word not in self.master_allowed:
                self.master_allowed.append(word)
        self.ExcelFile.create_user_dictionary(self.user_allowed,
                                              self.user_not_allowed)
        self.select_button.config(text="Create csv", command=self._Message)

    def _Message(self):
        self.ExcelFile.deidentify(self.master_not_allowed,
                                  self.master_indeterminate)
        savefile = asksaveasfile(defaultextension='.csv')
        showinfo(title="CSV Creation Alert", message="We are creating your CSV")
        self.ExcelFile.make_csv(savefile)
        self.parent.destroy()

    def _About(self):
        showinfo(title="About", message="A program to DeIdentify an excel file \
containing PHI")


def main():
    root = Tk()
    gui = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
