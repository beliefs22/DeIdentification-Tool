from Tkinter import *
class Menus:
        def __init__(self,menu,headers,commands):                
                self.headers = headers
                self.commands = commands
                for position, header in enumerate(headers):
                        newmenu = Menu(menu)
                        menu.add_cascade(label=header, menu=newmenu)
                        for commandlist in commands[int(position)]:
                                if commandlist[0] == 'separator':
                                        newmenu.add_separator()
                                else:
                                        
                                        print commandlist, commandlist[0], commandlist[1]
                                        newmenu.add_command(label=commandlist[0], command=commandlist[1])

def main():
        def test():
                    print "Hello world"
        headers = ['File','Edit','Help']
        commands = [[('Open',test),('separator',None)],[('Run',test)],[('About',test)]]        
        root = Tk()
        menu = Menu(root)
        root.config(menu=menu)
        window_menu = Menus(menu,headers,commands)
        mainloop()
if __name__ == '__main__':
	main()
