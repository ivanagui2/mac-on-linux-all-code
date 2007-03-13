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

	def draw(self):
		return Dialog.draw(self)

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
	### Add an OS X OS
	add.add('OS_X','Mac OS X')
	### Add a Mac Classic OS
	add.add('OS_9','Mac OS 9 or earlier')
	### Add a Linux OS
	add.add('Linux','Linux')
	### Exit
	add.add('Back','Cancel')
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

def mol_dialog_ro():
	read = Dialog_menu('Is the device writable?')
	### Read-write
	read.add('rw','Read-Write')
	### Read only
	read.add('ro','Read-Only')
	return read

def mol_cfg_blkdev():
	track = 0
	while (track == 0):
		### FIXME Need regex to validate block device paths
		try:
			blk_dev_p = Dialog_inputbox('Please specify a block device')
			blk_dev = str(blk_dev_p.draw())
			if (not blk_dev):
				warn = Dialog_msgbox('You must specify a block device').draw()
			else:
				track += 1
		except:
			warn = Dialog_msgbox('Not a valid path').draw()
	### Boot device?
	if (Dialog_yesno('Boot from this device?').draw() != 0):
		blk_dev	= blk_dev + ' -boot'
	### CD-Rom?
	if (Dialog_yesno('Is this a CD device?').draw() != 0):
		blk_dev = blk_dev + ' -cd -ro'
	else:
		### Writeable media?
		read_prompt = mol_dialog_ro()
		read = str(read_prompt.draw())
		blk_dev = blk_dev + ' -' + read
	### Configure adavanced options?
	if (Dialog_yesno('Would you like to configure advanced options for this device?').draw() != 0):
		### Force
		if (Dialog_yesno('Force MOL to use this device?\n(required for unformatted volumes)').draw() != 0):
			blk_dev = blk_dev + ' -force'
		### Whole
		if (Dialog_yesno('Export the entire device?').draw() != 0):
			blk_dev = blk_dev + ' -whole'
		### Boot1?
		if (Dialog_yesno('Force MOL to boot from this disk?\n(in spite of other boot options)').draw() != 0):
			blk_dev = blk_dev + ' -boot1'
	return blk_dev	

def mol_cfg_osx():
	### Create a molrc.osx file
	step = 0
	while step == 0:
		name_prompt = Dialog_inputbox('Name this configuation')
		name = str(name_prompt.draw())
		if (len(name) > 0):
			step +=1
		else:
			warn = Dialog_msgbox('You must specify a configuaration name').draw()
	while step == 1:
		try:
			ram_prompt = Dialog_inputbox('RAM (MB)')
			raw_ram = int(ram_prompt.draw())
			ram = str(raw_ram)
			step += 1
		except ValueError:
			warn = Dialog_msgbox('Invalid RAM value').draw()
	if (Dialog_yesno('Disable AltiVec?').draw() == 0):
		dis_altivec = "no"
	else:
		dis_altivec = "yes"
	if (Dialog_yesno('Enable USB?').draw() == 0):
		enable_usb = "no"
	else:
		enable_usb = "yes"
	if (Dialog_yesno('Enable autoprobing of SCSI devices?').draw() == 0):
		auto_scsi = "no"
	else:
		auto_scsi = "yes"
	blk_devs = []
	while step == 2:
		### At least one block device is required
		### TODO: Need to add an option to create a new image
		if (len(blk_devs) == 0):
			### Grab block device and arguments from function
			blk_dev = mol_cfg_blkdev()
			### Add new device to the list
			blk_devs.append(blk_dev)
		else:
			if (Dialog_yesno('Add another block device?').draw() == 0):
				step += 1
			else:
				### Grab block device and arguments from function
				blk_dev = mol_cfg_blkdev()
				### Add new device to the list
				blk_devs.append(blk_dev)
	### Write it to the config file
	### TODO: error handling
	write_osx_config(name,ram,dis_altivec,enable_usb,auto_scsi,blk_devs)
	Dialog_msgbox('Config file written').draw()

def mol_cfg_dialog_init():
	mm = mol_dialog_main()

	while(1):
		result = mm.draw()

		if result == "Quit" or result == 0:
			sys.exit()
		### Create a new MOL machinie configuation
		elif result == "Add":
			add = mol_dialog_add()	
			done = 0
			while(not done):
				result = add.draw()
				if result == "Back" or result == 0:
					done = 1
				elif result == "OS_X":
					mol_cfg_osx()
					done = 1
		### Adjust global mol settings
		elif result == "Configure":
			cfg = mol_dialog_config()	
			done = 0
			while(not done):
				result = cfg.draw()
				if result == "Back" or result == 0:
					done = 1

