from Tkinter import *

class CreateMenus:
    """Class to add cascades to a menu.

    Args:
        menu (tk menu): parent menu to place cascades in
        headers (list): list containing titles of cascades
        commands (list): list of groups of tupples where
            tuple[0] = title of command
            tuple[1] = command function
            Ex: [[('Open',OpenFile), ('Exit', root.quit)],
                  [('Run',CleanFile)],
                  [('About', Info)]
                  ]
    
    """
    
    def __init__(self, menu, headers, commands):
        self.headers = headers
        self.commands = commands
        for position, header in enumerate(headers):
            newmenu = Menu(menu) # create new Menu in parent Menu
            menu.add_cascade(label=header, menu=newmenu) #add menu info
            for commandinfo in commands[position]:
                if commandinfo[0] == 'separator':
                    newmenu.add_separator()
                else:
                    newmenu.add_command(label=commandinfo[0],
                                        command=commandinfo[1])
def main():
    def test():
        print "Hello world"

    def Quit():
        print "quit"        
        
    headers = ['File', 'Edit', 'Help']
    commands = [[('Open', test),('separator',None),('Exit',Quit)],
                [('Run', test)],
                [('About', test)]
                ]
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    root_menu = CreateMenus(menu, headers, commands)
    print "hello"
    root.mainloop()
if __name__ =='__main__':
    main()
