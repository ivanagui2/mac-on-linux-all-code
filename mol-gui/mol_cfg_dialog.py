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

def delete_blkdev_menu(volumes):
	menu = Dialog_menu('Select the device you would like to delete')
	### Populate the menu
	for i in range(len(volumes)):
		menu.add(str(i+1),volumes[i][0])
	menu.add('Done','Done')
	return menu

def mol_delete_blkdev(volumes):
	done = 0
	while (not done):
		delete_menu = delete_blkdev_menu(volumes)
		sel = delete_menu.draw()
		if (sel == 0):
			done = 1
		elif (sel == 'Done'):
			done = 1
		else:
			volumes.pop(int(sel)-1) 
			print volumes
	return volumes

def edit_bootflags_menu(device):
	opts = ""
	for option in device[1:]:
		opts = opts + " -" + option
	### Draw the menu
	menu = Dialog_menu('MOL - Edit device options\n\nSelected device:\n\t' + device[0] + opts +'\n\nToggle which option?')
	### List boot options
	menu.add('boot','Boot from this device')
	menu.add('cd','This is a CD-ROM device')
	menu.add('ro','This device is read-only')
	menu.add('rw','This device is writeable')
	menu.add('force','Force MOL to use this device')
	menu.add('whole','Export the whole device to MOL')
	menu.add('boot1','Boot from this device above any others')
	menu.add('Done','Done')
	return menu

def edit_bootflags(device):
	done = 0
	while (not done):
		boot_menu = edit_bootflags_menu(device)
		sel = boot_menu.draw()
		### Cancel escpaes the function
		if (sel == 0):
			return
		### End the loop
		elif (sel == 'Done'):
			done = 1
		### Toggle the selected bootflag
		else:
			device = mol_edit_bootflag(device,sel) 
	return device

def blkdev_menu(volumes):
	menu = Dialog_menu('Select which device you want to edit')
	### Populate menu with a list of devices and options
	for d in range(len(volumes)):
		opts = ""
		for option in volumes[d][1:]:
			opts = opts + " -" + option
		menu.add(str((d+1)),str(volumes[d][0])+ opts)
	menu.add('Done','Done')
	return menu

def mol_edit_blkdev(volumes):
	done = 0
	while (not done):
		edit_menu = blkdev_menu(volumes)
		sel = edit_menu.draw()
		### Bail if user cancels
		if (sel == 0):
			return
		### All done
		if (sel == 'Done'):
			done = 1
		### Send selected device to have its bootflags tweaked (ouch!)
		else:
			index = (int(sel)-1)
			volumes[index] = edit_bootflags(volumes[index])
	return volumes

def mol_dialog_blkdev(volumes):
	device_list = ""
	if (len(volumes) > 0):
		device_list = "\n\nList of currently configured devices and options:"
		### Print a list of configured volumes
		for item in volumes:
			opts = ""
			for option in item[1:]:
				opts = opts + " -" + option
			device_list = device_list + '\n\t' + item[0] + opts
	response = Dialog_menu('MOL - Add block device menu' + device_list)
	### Add a new device
	response.add('Add','Add a new device or volume')
	### Option to edit or delete previously entered block devices
	if (len(volumes) > 0):
		### Edit a device's boot flags
		response.add('Edit',"Edit a device's options")
		### Delete a device
		### TODO add delete menu
		response.add('Delete','Delete a device')
	### Help prompt
	response.add('Help','Help')
	### Continue
	response.add('Done','Finished')
	return response

def mol_cfg_blkdev():
	track = 0
	blk_dev=[]
	### Addition dialog
	while (track == 0):
		### FIXME Need regex to validate block device paths
		try:
			blk_dev_p = Dialog_inputbox('Please specify a block device')
			blk_dev.append(str(blk_dev_p.draw()))
			if (not blk_dev):
				warn = Dialog_msgbox('You must specify a block device').draw()
			else:
				track += 1
		except:
			warn = Dialog_msgbox('Not a valid path').draw()
	### Boot device?
	if (Dialog_yesno('Boot from this device?').draw() != 0):
		blk_dev.append('boot')
	### CD-Rom?
	if (Dialog_yesno('Is this a CD device?').draw() != 0):
		blk_dev.append('cd')
		blk_dev.append('ro')
	else:
		### Writeable media?
		read_prompt = mol_dialog_ro()
		blk_dev.append(str(read_prompt.draw()))
	### Configure adavanced options?
	if (Dialog_yesno('Would you like to configure advanced options for this device?').draw() != 0):
		### Force
		if (Dialog_yesno('Force MOL to use this device?\n(required for unformatted volumes)').draw() != 0):
			blk_dev.append('force')
		### Whole
		if (Dialog_yesno('Export the entire device?').draw() != 0):
			blk_dev.append('whole')
		### Boot1?
		if (Dialog_yesno('Force MOL to boot from this disk?\n(in spite of other boot options)').draw() != 0):
					blk_dev.append('boot1')
	return blk_dev	

def mol_cfg_osx():
	### Create a molrc.osx file
	osx_cfg = MOL_OS()
	osx_cfg.type = "osx"
	step = 0
	### Configuration needs a name
	while step == 0:
		name_prompt = Dialog_inputbox('Name this configuation')
		osx_cfg.name = str(name_prompt.draw())
		if (len(osx_cfg.name) > 0):
			step +=1
		else:
			warn = Dialog_msgbox('You must specify a configuaration name').draw()
	### Guest OS RAM (MB)
	while step == 1:
		try:
			ram_prompt = Dialog_inputbox('RAM (MB)')
			raw_ram = int(ram_prompt.draw())
			osx_cfg.ram = str(raw_ram)
			step += 1
		except ValueError:
			warn = Dialog_msgbox('Invalid RAM value').draw()
	### Give option to disable AltiVec
	if (Dialog_yesno('Disable AltiVec?').draw() == 0):
		osx_cfg.altivec = "no"
	else:
		osx_cfg.altivec = "yes"
	### Enable USB suppot
	if (Dialog_yesno('Enable USB?').draw() == 0):
		osx_cfg.usb = "no"
	else:
		osx_cfg.usb = "yes"
	### SCSI autoprobing
	if (Dialog_yesno('Enable autoprobing of SCSI devices?').draw() == 0):
		osx_cfg.auto_scsi = "no"
	else:
		osx_cfg.auto_scsi = "yes"
	### FIXME Need function to add SCSI devices if there is no autoprobing
	### Add block devices to the config
	while step == 2:
		volumes_menu = mol_dialog_blkdev(osx_cfg.volumes)
		sel = volumes_menu.draw()
		if (sel == 0):
			return
		elif (sel == "Done"):
			if (len(osx_cfg.volumes) > 0):
				step += 1
			else:
				warn = Dialog_msgbox('You must specify at least one device.').draw()
		elif (sel == "Add"):
			blk_dev = mol_cfg_blkdev()
			### Add new device to the list
			osx_cfg.volumes.append(blk_dev)
		### Edit the block devices
		elif (sel == "Edit"):
			osx_cfg.volumes = mol_edit_blkdev(osx_cfg.volumes)
		elif (sel == "Delete"):
			osx_cfg.volumes = mol_delete_blkdev(osx_cfg.volumes)
		### Help display
		### TODO: make help text for block devices
		elif (sel == "Help"):
			print "Help"

### Write it to the config file
	### TODO: error handling
	osx_cfg.write()
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

