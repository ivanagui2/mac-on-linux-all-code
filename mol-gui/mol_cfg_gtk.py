#! /usr/bin/env python
#
# (c) 2007 by Nathan Smith (ndansmith@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys, os
from threading import Thread
from mol_cfg_helper import *

try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	import gtk.glade
except:
	print "Error importing modules.  Did you install Mac-on-Linux \
	correctly?"

class MOL_GUI:
	def __init__(self):
		### Load the glade file
		self.gladefile="mol-gui.glade"
		self.gui = gtk.glade.XML(self.gladefile)
		self.window = self.gui.get_widget("main_window")
		### Connect events to callbacks
		dic = { "on_boot_osx_b_clicked" : self.boot_os_x,
			"on_boot_macos_b_clicked" : self.boot_macos,
			"on_boot_linux_b_clicked" : self.boot_linux,
			"on_quit_mol_b_clicked" : gtk.main_quit }
		self.gui.signal_autoconnect(dic)
		### Quit on attempted close
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)
	
	#######################################################################
	### Callback functions
	#######################################################################
	
	### Boot OS X
	def boot_os_x(self,w):
		os_x_boot = BOOT_MOL("osx")
		os_x_boot.start()

	### Boot Mac Classic
	def boot_macos(self,w):
		macos_boot = BOOT_MOL()
		macos_boot.start()

	### Boot Linux
	def boot_linux(self,w):
		linux_boot = BOOT_MOL("linux")
		linux_boot.start()

	### Main Loop
	def main(self):
		gtk.main()

### Start 'er up
mol = MOL_GUI()
mol.main()

###
# TODO
# Need a register of active threads
# Need to find a way to alter BOOT_MOL handler names for multiple instances of
#	one Guest-OS type
# Configure a new OS
# Configure mol options (video etc)
