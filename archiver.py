# Program: Personal Archiver
# Objective: Archive photos, lists, etc. in order to keep mac organized
# Author: Ben Tilden

from transferPhotos import transferPhotos
from sortPhotos import sortPhotos


def main():
    """Transfer photos from iDevice to Mac"""
    filePath = transferPhotos()
    if filePath != None:
    	sortPhotos(filePath)



# run
if __name__ == "__main__":
    main()
