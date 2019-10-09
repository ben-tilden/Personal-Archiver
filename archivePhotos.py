# Program: archivePhotos
# Objective: Import photos from iDevice and organize them
# Author: Ben Tilden

from transferPhotos import transferPhotos
from sortPhotos import sortPhotos


def main():
    """Transfer and organize photos from iDevice"""
    filePath = transferPhotos()
    if filePath != None:
    	sortPhotos(filePath)


# run
if __name__ == "__main__":
    main()
