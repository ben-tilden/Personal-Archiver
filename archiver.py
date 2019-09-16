# Program: Personal Archiver
# Objective: Archive photos, lists, etc. in order to keep mac organized
# Author: Ben Tilden

import re
import os
import sys
import time
import traceback
import threading
import applescript
import runcmd
import psutil


class previewClient():
    """Class used for Preview UI navigation via applescript."""

    def openPreview():
        """Open Preview."""
        applescript.run("./scripts/openPreview.scpt")

    def isMultiplePhones():
        """Return true if multiple devices are connected."""
        if applescript.run("./scripts/isMultiplePhones.scpt").out == "true":
            return True
        else:
            return False

    def clickImport():
        """Click "Import from " + iPhoneName in Preview.

        Utilize isMultiplePhones().
        Intended to immediately follow openPreview().
        """
        while previewClient.isMultiplePhones():
            print("Multiple devices connected. Press return when only one "
                  "iPhone is connected.")
            applescript.tell.app("Terminal", "activate")
            input()
        applescript.tell.app(
            "System Events",
            'click menu item 18 of menu 1 of menu bar item "File" '
            'of menu bar 1 of process "Preview"')

    def navImportWindow():
        """Navigate Preview window labelled "Import from " + iPhone.

        Intended to immediately follow clickImport() and device unlock.
        Intended to immediately precede waitPhotoLoad().
        """
        applescript.run("./scripts/navImportWindow.scpt")

    def fullDelay():
        """Delay functioning in an attempt to catch possible errors.

        Return True if one of the three cases below must be in effect:
        (1) The images are taking a long time to load.
        (2) The device is not unlocked / is not recognized by Preview.
        (3) There are no images to import.
        """
        if applescript.run("./scripts/fullDelay.scpt").out == "true":
            return True
        else:
            return False

    def waitingOnPhotoLoad():
        """Wait for photos for load if iPhone has just been connected.

        Prompt user if load taking a long time.
        Exit if user is unwilling to wait or notices something wrong.
        If user does not want to wait, return False, else True.
        """
        userExit = False
        while True:
            if previewClient.fullDelay() == False:
                break
            applescript.tell.app("Terminal", "activate")
            userWait = input(
                "Keep waiting? (y/n)\n"
                "This message occurs if\n"
                "(1) The images are taking a long time to load\n"
                "(2) The iPhone is not unlocked\n"
                "(3) There are no images to import\n")
            if userWait.lower() == "n" or userWait.lower() == "no":
                userExit = True
                break
        # sheet which notifies of photos being prepared
        applescript.tell.app(
            "System Events",
            'if exists sheet 1 of window 1 of process "Preview" then '
            'click button 1 of sheet 1 of window 1 of process "Preview"')
        if userExit:
            print("The program will exit now")
            applescript.tell.app("Preview", "quit")
        return userExit

    def batchImport(batchNum, filePath):
        """Import photos in batches.

        Arguments:
        batchNum -- number in batch
        filePath -- file path
        """
        args = ["osascript", "./scripts/batchImport.scpt", batchNum, filePath]
        r = runcmd.run(args)
        if r.out == "true":
            print("Import complete")
            applescript.tell.app("Preview", "quit")
        elif r.out == "false":
            print("Preview is unresponsive as a result of finding "
                  "a time-lapse video")
            print("The program will exit now")
            applescript.tell.app("Preview", "quit")
        else:
            print(r.out)  # throw error new
            print("The program will exit now")

    def importAll(filePath):
        """Import all photos.

        Arguments:
        filePath -- file path
        """
        args = ["osascript", "./scripts/importAll.scpt", filePath]
        r = runcmd.run(args)
        if r.out == "true":
            print("Import complete")
            applescript.tell.app("Preview", "quit")
        elif r.out == "false":
            print("Preview is unresponsive as a result of finding "
                  "a time-lapse video")
            applescript.tell.app("Preview", "quit")
        else:
            print(r.out)  # throw error new
            print("The program will exit now")


def checkFilePathRedundancy(userDir, homeDir):
    """Ensure given path doesn't begin with end directories of home.

    Return string of directory with user's home directory attached.
    Example: if user's home directory is /Users/user then /user/folder
    will save in /Users/user/folder instead of /Users/user/user/folder

    Will not allow path directory to be any parent of users' home.

    Arguments:
    userDir -- directory given by user
    homeDir -- home directory of user
    """
    homeString = ""
    homeDirList = homeDir.strip("/").split("/")
    userDirList = userDir.strip("/").split("/")
    userDirListCopy = userDirList[:]
    pathPastHome = homeCheck(homeDirList, userDirList, False)
    if pathPastHome is not None:
        homeString = "/".join(pathPastHome)
    else:
        homeString = "/".join(userDirListCopy)
    if homeDir == "/":
        homeString = homeDir + homeString
    else:
        homeString = homeDir + "/" + homeString
    return homeString


def homeCheck(homeDirList, userDirList, isHomeSequence):
    """Return series of home directories that are not in user's path.

    Possible outcomes:
    (1) Pop the first directory from both directory lists if equal
    (2) Pop only the first directory from homeDirList if it is not
        equal to the first directory of userDirList
    (3) Return only the user directories past the home directories if
        there is a sequence of home directories at the beginning of the
        user directory, None otherwise

    Arguments:
    homeDirList -- list of directories in the user's home directory
    userDirList -- list of directories in path given by user
    isHomeSequence -- bool indicates if there is a sequence of matches
    """
    if len(homeDirList) != 0 and len(userDirList) != 0:
        if homeDirList[0] == userDirList[0]:
            isHomeSequence = True
            homeDirList.pop(0)
            userDirList.pop(0)
            return homeCheck(homeDirList, userDirList, isHomeSequence)
        else:
            if isHomeSequence:
                return None
            else:
                homeDirList.pop(0)
                return homeCheck(homeDirList, userDirList, isHomeSequence)
    elif len(homeDirList) != 0 and len(userDirList) == 0:
        # Handle case where homeDir=/Users/user and userDir=/Users
        # (didn't want to mess with permissions in this instance)
        return None
    else:
        if isHomeSequence:
            return userDirList
        else:
            return None


def isUserSatisfied(filePath):
    """Check if user is satisfied with interpreted path.

    Return True is user is satisfied, False otherwise.

    Arguments:
    filePath -- file path shown to user
    """
    print(
        "I have " +
        filePath +
        " as your file path. Correct? (y/n) (If this directory does not exist "
        "it will be created.)")
    while True:
        userSatisfied = input()
        if (userSatisfied == "" or
            userSatisfied.lower() == "y" or
            userSatisfied.lower() == "ye" or
                userSatisfied.lower() == "yes"):
            return True
        elif userSatisfied.lower() == "n" or userSatisfied.lower() == "no":
            return False
        else:
            print("Please enter either \"y\" or \"n\"")


def getFilePath():
    """Get file path from user; return file path for saving."""
    userDir = ""
    homeDir = os.path.expanduser("~")
    correctFilePath = False
    while correctFilePath == False:
        print("What file would you like your photos to be organized within?")
        print("Default folder: " + homeDir + "/Pictures/Archiver")
        print("Default location: " + homeDir)
        print("Note: This application will not save in any parent directory of"
              " " + homeDir)
        userDir = input()
        if userDir == "":  # default
            userDir = homeDir + "/Pictures/Archiver"
        if not re.search("^/", userDir):
            # path must begin with "/"
            userDir = "/" + userDir
        startsWithPeriod = False
        if re.search(r"/\.", userDir):
            # Path cannot contain "/." as files (in this usage)
            # should not begin with a period
            userDir = userDir.replace("/.", "/")
            startsWithPeriod = True
        startsWithHomeRegex = "^" + homeDir
        if not re.search(startsWithHomeRegex, userDir):
            # No need to check for redundancy if userDir starts with homeDir
            userDir = checkFilePathRedundancy(userDir, homeDir)
        if re.search(":", userDir):  # path cannot contain ":"
            userDir = userDir.replace(":", " ")
            print("Without the colon (which is illegal), your file path is " +
                  userDir)
        if startsWithPeriod:
            # "re.search" needed earlier to address more likely case that
            # period is user error
            print("Without the starting period (which is illegal), your file "
                  "path is " +
                  userDir)
        correctFilePath = isUserSatisfied(userDir)
    return userDir


def isBatchImport():
    """Return True if user wants batch import, false otherwise."""
    print("Default is import all photos at once rather than in batches. "
          "Continue with default? (y/n)")
    while True:
        userSatisfied = input()
        if (userSatisfied == "" or
            userSatisfied.lower() == "y" or
            userSatisfied.lower() == "ye" or
                userSatisfied.lower() == "yes"):
            return False
        elif userSatisfied.lower() == "n" or userSatisfied.lower() == "no":
            return True
        else:
            print("Please enter either \"y\" or \"n\"")


def getBatchNum():
    """Return number of photos per batch; default = 100."""
    print("Default number per batch is 100. Enter a different number to "
          "change this (max 1000). Otherwise, press return.")
    while True:
        batchNum = input()
        if batchNum == "":
            return 100
        elif batchNum.isdigit() and int(batchNum) <= 1000 and int(batchNum) > 0:
            return batchNum
        else:
            print("Please enter either an integer number greater than 0 and "
                  "less than or equal to 1000")


def getSerialNo():
    """Return serial number of apple device if connected, None otherwise."""
    args = ["ioreg", "-w0", "-rc", "IOUSBDevice", "-k", "SupportsIPhoneOS"]
    ioregOutput = runcmd.run(args).out
    if ioregOutput == "":
        return None
    else:
        serialNoArr = re.findall(
            "\"USB Serial Number\" = \"([A-Za-z0-9]+)\"",
            ioregOutput)
        if not serialNoArr:
            return None
        else:
            return serialNoArr[0]


def serialNoCheck():
    """Return serial number of connected device."""
    serialNo = getSerialNo()
    while serialNo is None:
        input("Press return when iPhone is connected.")
        serialNo = getSerialNo()
    return serialNo

# Serial number check meant to run in background during Preview navigation
# and import


def connectionCheck(serialNo):
    """Continually check if serial number of connected device equals
    serialNo. terminate all processes associated with program if device
    disconnected.

    Arguments:
    serialNo: initial serial number of device for import
    """
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


def transferPhotos():
    """Transfer photos from iDevice to Mac."""
    try:
        batchNum = -1
        print("Welcome to the Archiver")
        print("Press Ctrl+C to quit at any time")
        print("\033[1mTo ignore any parameters press return at the prompts "
              "and settings will be set to default\033[0m")
        filePath = getFilePath()
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        if isBatchImport():
            batchNum = getBatchNum()
        print("\033[1mThe program will fail and exit upon finding a time-lapse"
              " video. It is recommended to check for time-lapse videos before"
              " running.\033[0m")
        print("\033[1mAvoid interacting with the computer other than Terminal "
              "while import is occurring.\nUI navigation can very easily fail "
              "if interrupted.\033[0m")
        previewClient.openPreview()
        serialNo = serialNoCheck()
        c = threading.Thread(
            target=connectionCheck, args=(
                serialNo,), daemon=True)
        c.start()
        previewClient.clickImport()
        applescript.tell.app("Terminal", "activate")
        input("Press return when iPhone is unlocked")
        applescript.tell.app("Preview", "activate")
        previewClient.navImportWindow()
        if previewClient.waitingOnPhotoLoad() == False:
            if int(batchNum) > 0:
                previewClient.batchImport(batchNum, filePath)
            else:
                previewClient.importAll(filePath)
    except KeyboardInterrupt:
        print("\nUser exited.")
        sys.exit()
        # exit preview and osascript as well new
    except Exception as e:
        print("Something went wrong in the photo transfer:")
        traceback.print_exc()


def main():
    """Transfer photos from iDevice to Mac"""
    transferPhotos()


# run
if __name__ == "__main__":
    main()
