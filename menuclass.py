from Tkinter import *
Class Menus:
	def__init__(self,menu,headers,commands):
		self.headers = headers
		self.commands = commands
		for header, position in enumerate(headers):
			newmenu = Menu(menu)
			menu.add_cascade(label=header, newmenu)
				for commandlist in commands[position]:
					if commandlist[0] == 'separator':
						newmenu.add_separator()
					else:
						newmenu.add_command(label=commandlist[0], command=commandlist[1])

def main():
	
	headers = ['File','Edit','Help']
	commands = [[('Open',test),('separator',None)],[('Run',test)],[('About',test)]
	
	def test():
		print "Hello world"
	
	root = Tk()
	menu = Menu(root)
	
	window_menu = Menus(menu,headers,commands)
	
	root.mainloop()

if __name__ == '__main__':
	main()
				
