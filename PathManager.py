"""
WINDOWS PATH ENTRIES MANAGER
Licenced as GPL
@author: Marius Munthe-Kaas 
@email: mariussmk@gmail.com
"""

import os
import sys
import winreg


class PathSettings:
	""" Path-settings class

	Contains all neccessary methods to append, remove and list path entries
	"""

	def __init__(self):
		
		self.checkOs()
		self.openPathString()
		self.makePathList()
		self.pathList.pop()

	def checkOs(self):
		""" Check if os is win. If not terminate """

		if not(sys.platform.startswith("win")):
			print("*** ERROR ***\n Operating system not supported (win-only)\n Exits...")
			sys.exit()

	def openPathString(self):
		""" Make a path string from windows registry entry 
			Raise: WindowsError if the key cannot be opened """

		try:
			t = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",0, winreg.KEY_READ)
			s = winreg.QueryValueEx(t, "Path")
			self.pathString = s[0]

		except WindowsError as e:
			print("Windows error {}".format(e))

	def makePathList(self):
		""" Make a path list from the path string """

		self.pathList = self.pathString.split(";")

	def listAll(self):
		""" List all path entries """

		for count,pathVar in enumerate(self.pathList):
			print("{}: {}".format(count, pathVar))

	def append(self):
		""" Append a new path entry to the list """

		readLine = input("Type a path entry")
		if(len(readLine) > 0):
			self.pathList.append(readLine)

	def remove(self):
		""" Remove a path entry from the list """

		self.listAll()
		read = self.readNumber("Choose the number of which the lines to be delete from")
		num = int(read)
		while num > len(self.pathList) or num < 0:
			num = self.readNumber("Error. Type a valid number")

		self.pathList.pop(num)
		self.savePath()


	def commandLoop(self):
		""" Print the user command loop """

		self.printMenu()
		num = self.readNumber("\nChoose a menu option (5 to exit)")
		if(num == "5"):
			return False
		self.initiateAction(num)

	def readNumber(self, msg):
		""" Read a number. Don't stop until a valid number has been chosen """

		sentinel = False
		while sentinel != True:
			command = input("{}:\n".format(msg))
			if command.isdigit():
				sentinel = True
				return command

	def initiateAction(self, actionInt):
		""" Call the correct method based on user input

		 Keyword arguments:
		 actionInt -- Number read from readNumber()
		 """

		if actionInt == "1":
			self.listAll()

		elif actionInt == "2":
			self.append()

		elif actionInt == "3":
			self.remove()

		elif actionInt == "4":
			self.savePath()

		elif actionInt == "5":
			return False

	def printMenu(self):
		""" Print the menu """

		print ("\nMenu:")
		print ("1: List all path entries")
		print ("2: Add new path entry")
		print ("3: Delete path entry")
		print ("4: Save path entries")
		print ("5. EXIT\n")


	def generatePathString(self):
		""" Make a new path string based on the list """

		pathString = ""
		for pathVar in self.pathList:
			pathString += pathVar + ";"
		self.pathString = pathString


	def savePath(self):
		""" Save the new path string to the registry

		Raise:
		WindowsError -- If it cannot be saved
		"""

		self.generatePathString()
		print(self.pathString)
		try:
			t = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",0, winreg.KEY_WRITE)
			winreg.SetValueEx(t, "Path", 0, winreg.REG_SZ, "{}".format(self.pathString))

		except WindowsError as e:
			print("Windows error" + e)

"""
Run the program
"""

var = PathSettings()
print ("\n**************************")
print ("** Manage path-settings **")
print ("**************************")

while True:
	choose = var.commandLoop()
	if choose == False:
		break

