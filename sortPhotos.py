#!/usr/bin/env python3

# Program: sortPhotos
# Objective: Sort photos in a given directory
# Author: Ben Tilden

import os
import time
import traceback

# Global constants
MONTH_DICT = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "November",
    11: "November",
    12: "December"
}

PHOTO_EXTENSION_LIST = [
    ".JPG",
    ".JPEG",
    ".JP2",
    ".GIF",
    ".PNG",
    ".TIF",
    ".TIFF",
    ".BMP"
]

VIDEO_EXTENSION_LIST = [
    ".MOV",
    ".M4V",
    ".MP4",
    ".3G2",
    ".3GP",
    ".3GP2",
    ".3GPP"
]

RAW_EXTENSION_LIST = [
    ".3FR",
    ".ARI",
    ".ARW",
    ".BAY",
    ".CR2",
    ".CR3",
    ".CRW",
    ".CS1",
    ".CXI",
    ".DCR",
    ".DNG",
    ".EIP",
    ".ERF",
    ".FFF",
    ".IIQ",
    ".J6I",
    ".K25",
    ".KDC",
    ".MEF",
    ".MFW",
    ".MOS",
    ".MRW",
    ".NEF",
    ".NRW",
    ".ORF",
    ".PEF",
    ".RAF",
    ".RAW",
    ".RW2",
    ".RWL",
    ".RWZ",
    ".SR2",
    ".SRF",
    ".SRW",
    ".X3F"
]

def createDict(filePath):
    """Create dictionary of file names.

    key : value
    file name without extension : [list of extensions, date modified]
    "IMG_2820" : [[".JPG", ".MOV"], "July 2019"]

    Also delete .AAE files.

    Arguments:
    filePath -- file path
    """
    fileDict = {}
    monthDirList = []
    aaeList = []
    for fileName in os.listdir(filePath):
        fileSplit = os.path.splitext(fileName)
        if fileSplit[1] == ".AAE":
            aaeList.append(fileName)
        elif ((fileSplit[1] not in PHOTO_EXTENSION_LIST) and 
             (fileSplit[1] not in VIDEO_EXTENSION_LIST) and 
             (fileSplit[1] not in RAW_EXTENSION_LIST)):
            pass
        else:
            if fileSplit[0] in fileDict.keys():
                fileDict[fileSplit[0]][0].append(fileSplit[1])
            else:
                fileName = filePath + "/" + fileName
                dateModified = time.localtime(os.path.getmtime(fileName))
                monthYear = (MONTH_DICT[dateModified.tm_mon] + 
                            " " + 
                            str(dateModified.tm_year))
                fileDict[fileSplit[0]] = [[fileSplit[1]], monthYear]
                if monthYear not in monthDirList:
                    monthDirList.append(monthYear)
    print("sortPhotos found " + 
          str(len(fileDict)) + 
          " unique file name groupings in import.")
    print("This counts both edited photos and "
          "their original copies (if they exist).")
    if len(aaeList) > 0:
        print("The following files will be deleted if the program continues:")
        for element in aaeList:
            print(element)
        input("Press return to continue")
        for element in aaeList:
            os.remove(filePath + "/" + element)
    return fileDict

def iterateDict(fileDict, filePath):
    """Iterate through dictionary created by createDict

    Add photos to files based on dictionary values

    Arguments:
    fileDict -- dictionary from createDict
    filePath -- file path
    """
    for x, y in fileDict.items():
        elementFilePath = filePath + "/"
        if (len(y[0]) == 1 and
        (y[0][0] == ".MOV" or y[0][0] == ".M4V" or 
         y[0][0] == ".MP4" or y[0][0] == ".3GP" or 
         y[0][0] == ".3G2" or y[0][0] == ".3GP2" or 
         y[0][0] == ".3GPP")):
            elementFilePath += "Movies/"
            elementFilePath += y[1]
        else:
            elementFilePath = elementFilePath + "Pictures/"
            elementFilePath = elementFilePath + y[1] + "/"
            if ".JPG" in y[0] or ".JPEG" in y[0]: # picture
                elementFilePath += "Pictures"
            else:
                elementFilePath += "Screenshots"
        if not os.path.exists(elementFilePath):
            os.makedirs(elementFilePath)
        for extension in y[0]:
            fileName = x + extension
            os.rename(filePath + "/" + fileName, 
                      elementFilePath + "/" + fileName)


def sortPhotos(filePath):
    """Sort photos in a given directory."""
    try:
        iterateDict(createDict(filePath), filePath)
    except Exception:
        print("Something went wrong in the photo sort:")
        traceback.print_exc()
