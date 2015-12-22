from Tkinter import *

root = Tk()
yscroll = Scrollbar(orient=VERTICAL)
xscroll = Scrollbar(orient=HORIZONTAL)
yscroll.grid(row=0,column=1, sticky=N+S)
xscroll.grid(row=1,column=0, sticky=E+W)
canvas = Canvas(root,background="white", yscrollcommand=yscroll.set,
                xscrollcommand=xscroll.set)
yscroll.config(command=canvas.yview)
xscroll.config(command=canvas.xview)
canvas.grid(row=0,column=0, sticky=N+S+E+W)

top = canvas.winfo_toplevel()
top.rowconfigure(0, weight=1)
top.rowconfigure(1, weight=1)
top.columnconfigure(1, weight=1)
top.columnconfigure(0, weight=1)

root.mainloop()
