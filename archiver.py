# Program: Personal Archiver
# Objective: Archive photos, lists, etc. in order to keep mac organized
# Author: Ben Tilden

from transferPhotos import transferPhotos


def main():
    """Transfer photos from iDevice to Mac"""
    transferPhotos()


# run
if __name__ == "__main__":
    main()
