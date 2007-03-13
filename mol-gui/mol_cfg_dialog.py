#!/usr/bin/python

###############################################################################
### Provide a default dialog based frontend
###############################################################################

try:
	import sys, os, commands
	### Import the backend
	from mol_cfg_helper import *

except ImportError, e:
	print "Module loading failed with: " + str(e)
	print "Please check that MOL is installed correctly!"
	sys.exit()

###############################################################################
### Dialog Wrapper
###############################################################################

### Main Dialog Class
class Dialog:
	def __init__(self, text):	
		self.type = "none"
		self.text = text
		self.height = 0
		self.width = 0
		self.defaultno = 0

	def height(self, height):
		if height != None:
			self.height = hieght
		return self.height

	def width(self, width):
		if width != None:
			self.width = width
		return self.width

	### Draws the object with dialog
	def draw(self, cmd=""):
		c = '"' + str(self.text) + '"'
		c = c + " " + str(self.height)
		c = c + " " + str(self.width) + " "
		if cmd:
			cmd = c + cmd
		else:
			cmd = c

		if self.defaultno:
			cmd = "--defaultno " + cmd

		c = 'dialog --' + self.type + ' ' + cmd + ' 2>&1 > /dev/tty'	

		### Call dialog	
		result = os.popen(c)
		value = result.read()
		if result.close():
			return 0
		else:
			return value

	### Add something to the Dialog object (depends on the type)
	def add(self, item):
		pass

### Dialog box with some text and an ok button
class Dialog_msgbox(Dialog):
	def __init__(self, text):
		Dialog.__init__(self,text)
		self.type = "msgbox"

### Yes/No dialog
class Dialog_yesno(Dialog):
	def __init__(self, text):
		Dialog.__init__(self, text)
		self.type = "yesno"

### Type in a line of text
class Dialog_inputbox(Dialog):
	def __init__(self, text):
		Dialog.__init__(self,text)
		self.type = "inputbox"
		self.start_value = None

	def add(self, value):
		if value:
			self.start_value = value
		else:
			self.start_value = None

	def draw(self):
		return Dialog.draw(self, self.start_value)			

### Menu
class Dialog_menu(Dialog):
	def __init__(self, text):
		Dialog.__init__(self,text)
		self.type = "menu"
		self.options = []
		self.menu_height = 0

	def draw(self):
		if len(self.options) > 0:
			c = str(self.menu_height) + " " + " ".join(self.options)
			return Dialog.draw(self, c)
		
		### No result if the menu can't be drawn
		return 0

	def add(self, tag, item):
		if tag and item:
			self.options.append('"' +  tag + '" "' + item + '"')

###############################################################################
### Configuration menu 
###############################################################################

def mol_dialog_main():
	### Main dialog instance
	mm = Dialog_menu('MOL - Main Menu')
	### Get available Boot Targets

	### List available Boot Targets

	### Add a Boot Target
	mm.add('Add','Add an OS')	
	### Configuration menu
	mm.add('Configure','Configure MOL')
	### Exit
	mm.add('Quit', 'Quit without saving')
	return mm

### Add an OS
def mol_dialog_add():
	add = Dialog_menu('MOL - Add an OS')
	return add
	
def mol_dialog_config():
	### Main dialog instance
	cfg = Dialog_menu('MOL - Configuration Menu')
	### Configure Video
	cfg.add('Video', 'Configure MOL Video')
	### Configure Sound
	cfg.add('Sound', 'Configure MOL Sound')
	### Configure Input
	cfg.add('Input', 'Configure MOL Input')
	### Save
	cfg.add('Save', 'Save your configuration')
	### Exit
	cfg.add('Back', 'Quit without saving')
	return cfg

def mol_cfg_dialog_init():
	mm = mol_dialog_main()

	while(1):
		result = mm.draw()

		if result == "Quit" or result == 0:
			sys.exit()
		elif result == "Configure":
			cfg = mol_dialog_config()	
			done = 0
			while(not done):
				result = cfg.draw()
				if result == "Back" or result == 0:
					done = 1

