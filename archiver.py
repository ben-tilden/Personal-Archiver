# Program: Personal Archiver
# Objective: Archive photos, lists, etc. in order to keep mac organized
# Author: Ben Tilden

import re
import os
import time
import subprocess
import threading
import applescript
import runcmd
import psutil

class photoClient():

	# Opens Preview
	def openPreview():
		applescript.run("./scripts/openPreview.scpt")

	# Checks if there are multiple devices connected. Returns True if there are multiple devices, false otherwise
	def isMultiplePhones():
		if applescript.run("./scripts/isMultiplePhones.scpt").out == "true":
			return True
		else:
			return False

	# Clicks "Import from " + iPhoneName in Preview if there are not multiple devices connected
	# Intended as first action after openPreview()
	def clickImport():
		while photoClient.isMultiplePhones() == True:
			print("Multiple devices connected. Press return when only one iPhone is connected.")
			applescript.tell.app("Terminal", "activate")
			input()
		applescript.tell.app("System Events", 'click menu item 18 of menu 1 of menu bar item "File" of menu bar 1 of process "Preview"')

	# Navigates the window of Preview labelled "Import from " + iPhoneName; occurs after "Import from " + iPhoneName click and device unlock.
	# Intended to immediately follow clickImport() and immediately precede waitPhotoLoad()
	def navImportWindow():
		applescript.run("./scripts/navImportWindow.scpt")

	# Delays functioning in an attempt to catch possible errors
	# Returns True if one of the three cases listed below must be in effect, false otherwise
	# Necessary for distinguishing amongst three cases:
	# (1) The images are taking a long time to load
	# (2) The device is not unlocked / is not recognized by Preview
	# (3) There are no images to import
	def fullDelay():
		if applescript.run("./scripts/fullDelay.scpt").out == "true":
			return True
		else:
			return False

	# Waits for photos to load if iPhone has just been connected; exits if user is unwilling to wait and/or notices there is something wrong
	# Prompts user if load taking a long time - handles 3 possibilities listed in comments above (there is no immediate way via UI interface of knowing whether photos are loading or not)
	# If user does not want to wait, it will return false; otherwise it returns true
	def waitingOnPhotoLoad():
		userExit = False
		while True:
			if photoClient.fullDelay() == False:
				break
			applescript.tell.app("Terminal", "activate")
			userWait = input("Keep waiting? (y/n)\nThis message occurs if\n(1) The images are taking a long time to load\n(2) The iPhone is not unlocked\n(3) There are no images to import\n")
			if userWait.lower() == "n" or userWait.lower() == "no":
				userExit = True
				break
		applescript.tell.app("System Events", 'if exists sheet 1 of window 1 of process "Preview" then click button 1 of sheet 1 of window 1 of process "Preview"') # sheet which notifies of photos being prepared
		if userExit == True:
			print("The program will exit now")
			applescript.tell.app("Preview","quit")
		return userExit

	# Imports 
	def batchImport(batchNum, filePath):
		args = ["osascript", "./scripts/batchImport.scpt", batchNum, filePath]
		r = runcmd.run(args)
		if r.code == 0:
			print("Import complete")
			applescript.tell.app("Preview","quit")
		else:
			print("batchImport.scpt did not run properly")

	def importAll(filePath):
		args = ["osascript", "./scripts/importAll.scpt", filePath]
		r = runcmd.run(args)
		if r.code == 0:
			print("Import complete")
			applescript.tell.app("Preview","quit")
		else:
			print("importAll.scpt did not run properly")


# Ensures the given path does not already contain directories from the users' preset home directory
# For example, if users' home directory is /Users/user then /user/untitled will still save in /Users/user/untitled instead of /Users/user/user/untitled
# Will not allow path directory to be any parent of users' home directory
def checkFilePathRedundancy(userDir, homeDir):
	homeString = ""
	homeDirList = homeDir.strip("/").split("/")
	userDirList = userDir.strip("/").split("/")
	userDirListCopy = userDirList[:]
	pathPastHome = homeCheck(homeDirList, userDirList, False)
	if pathPastHome != None:
		homeString = "/".join(pathPastHome)
	else:
		homeString = "/".join(userDirListCopy)
	if homeDir == "/":
		homeString = homeDir + homeString
	else:
		homeString = homeDir + "/" + homeString
	return homeString

# Recursive method which
# (1) Pops the first directory from both directory lists if they are the same
# (2) Pops only the first directory from the home directory list if it is not the same as the first directory of the user directory list
# (3) Returns only the user directories listed past the home directories if there is a sequence of home directories at the beginning of the user directory, None otherwise
def homeCheck(homeDirList, userDirList, isHomeSequence):
	if len(homeDirList) != 0 and len(userDirList) != 0:
		if homeDirList[0] == userDirList[0]:
			isHomeSequence = True
			homeDirList.pop(0)
			userDirList.pop(0)
			return homeCheck(homeDirList, userDirList, isHomeSequence)
		else:
			if isHomeSequence == True:
				return None
			else:
				homeDirList.pop(0)
				return homeCheck(homeDirList, userDirList, isHomeSequence)
	elif len(homeDirList) != 0 and len(userDirList) == 0: # handles case where homeDir=/Users/user and userDir=/Users (didn't want to mess with permissions in this instance)
		return None
	else:
		if isHomeSequence == True:
			return userDirList
		else:
			return None

# Checks if user is satisfied with interpreted path
# Returns True is user is satisfied, false otherwise
def isUserSatisfied(filePath):
	print("I have " + filePath + " as your file path. Correct? (y/n) (If this directory does not exist it will be created.)")
	while True:
		userSatisfied = input()
		if userSatisfied == "" or userSatisfied.lower() == "y" or userSatisfied.lower() == "ye" or userSatisfied.lower() == "yes":
			return True
		elif userSatisfied.lower() == "n" or userSatisfied.lower() == "no":
			return False
		else:
			print("Please enter either \"y\" or \"n\"")

# Gets the desired file path for the photos from user
# Returns file path in which to save the photos
def getFilePath():
	userDir = ""
	homeDir = os.path.expanduser("~")
	correctFilePath = False
	while correctFilePath == False:
		print("What file would you like your photos to be organized within?")
		print("Default folder: " + homeDir + "/Pictures/Archiver")
		print("Default location: " + homeDir)
		print("Note: This application will not save in any parent directory of " + homeDir)
		userDir = input()
		if userDir == "": # default
			userDir = homeDir + "/Pictures/Archiver"
		if not re.search("^/", userDir): # path must begin with "/"
			userDir = "/" + userDir
		startsWithPeriod = False
		if re.search("/\.", userDir): # path cannot contain "/." as files (in this usage) should not begin with a period
			userDir = userDir.replace("/.", "/")
			startsWithPeriod = True
		startsWithHomeRegex = "^" + homeDir
		if not re.search(startsWithHomeRegex, userDir): # no need to check for redundancy if userDir starts with homeDir
			userDir = checkFilePathRedundancy(userDir, homeDir)
		if re.search(":", userDir): # path cannot contain ":"
			userDir = userDir.replace(":", " ")
			print("Without the colon (which is illegal), your file path is " + userDir)
		if startsWithPeriod == True: # "re.search" needed earlier to address more likely (?) case that period is user error
			print("Without the starting period (which is illegal), your file path is " + userDir)
		correctFilePath = isUserSatisfied(userDir)
	return userDir

# Prompts user asking whether or not to batch import
# Returns true if user wants batch import, false otherwise
def isBatchImport():
	print("Default is import all photos at once rather than in batches. Continue with default? (y/n)")
	while True:
		userSatisfied = input()
		if userSatisfied == "" or userSatisfied.lower() == "y" or userSatisfied.lower() == "ye" or userSatisfied.lower() == "yes":
			return False
		elif userSatisfied.lower() == "n" or userSatisfied.lower() == "no":
			return True
		else:
			print("Please enter either \"y\" or \"n\"")

# Prompts user asking for number per batch
# Returns 100 if user wants default, user input greater than 0 and less than or equal to 1000 otherwise
def getBatchNum():
	print("Default number per batch is 100. Enter a different number to change this (max 1000). Otherwise, press return.")
	while True:
		batchNum = input()
		if batchNum == "":
			return 100
		elif batchNum.isdigit() and int(batchNum) <= 1000 and int(batchNum) > 0:
			return batchNum
		else:
			print("Please enter either an integer number greater than 0 and less than or equal to 1000")

# If Apple device connected, returns serial number of device using ioreg command, otherwise returns None
def getSerialNo():
	ioregOutput = subprocess.check_output("ioreg -w0 -rc IOUSBDevice -k SupportsIPhoneOS", shell=True).decode("utf-8")
	if ioregOutput == "":
		return None
	else:
		serialNoArr = re.findall("\"USB Serial Number\" = \"([A-Za-z0-9]+)\"", ioregOutput)
		if not serialNoArr:
			return None
		else:
			return serialNoArr[0]

# Initial serial number check meant to ensure iPhone is connected before program attempts to navigate Preview
def serialNoCheck():
	serialNo = getSerialNo()
	while serialNo == None:
		input("Press return when iPhone is connected.")
		serialNo = getSerialNo()
	return serialNo

# Serial number check meant to run in background during Preview navigation and import
def connectionCheck(serialNo):
	while getSerialNo() == serialNo:
		time.sleep(.3)
	print("\niPhone disconnected. This program will now exit")
	pythonPID = ""
	for p in psutil.process_iter(attrs=['name']):
		if 'osascript' in p.info['name'] or 'Preview' in p.info['name']:
			p.terminate()
		elif 'Python' in p.info['name']:
			pythonPID = p.pid
	psutil.Process(pythonPID).terminate()

# Method which transfers photos from iPhone to Mac
def transferPhotos():
	batchNum = -1
	print("Welcome to the Archiver")
	print("Press Ctrl+C to quit at any time")
	print("\033[1mTo ignore any parameters press return at the prompts and settings will be set to default\033[0m")
	filePath = getFilePath()
	if not os.path.exists(filePath):
		os.makedirs(filePath)
	if isBatchImport() == True:
		batchNum=getBatchNum()
	print("\033[1mThe program will fail and exit upon finding a time-lapse video. It is recommended to check for time-lapse videos before running.\033[0m")
	print("\033[1mAvoid interacting with the computer other than Terminal while import is occurring.\nUI navigation can very easily fail if interrupted.\033[0m")
	photoClient.openPreview()
	serialNo = serialNoCheck()
	c = threading.Thread(target=connectionCheck, args=(serialNo,), daemon=True)
	c.start()
	photoClient.clickImport()
	applescript.tell.app("Terminal", "activate")
	input("Press return when iPhone is unlocked")
	applescript.tell.app("Preview", "activate")
	photoClient.navImportWindow()
	if photoClient.waitingOnPhotoLoad() == False:
		if int(batchNum) > 0:
			photoClient.batchImport(batchNum, filePath)
		else:
			photoClient.importAll(filePath)

# main()
def main():
	transferPhotos()

# run
if __name__== "__main__":
    main()