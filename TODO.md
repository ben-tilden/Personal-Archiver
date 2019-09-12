# TODO (Notes)
* connectionCheck() method
	* Insert after line 242, running in background
	* Add functionality which kills Preview and applescript processes if iPhone disconnected
	* Kill connectionCheck() process if imports are successful
* Test to see if program works with iPads
	* If so, change all instances of "phone" or "iPhone" to "device"
	* If not, change all instances of "device" to "iPhone"
	* Lines: 18, 24, 28, 33
* For functions with no return values, possibly add "return 0 on success, 1 otherwise" functionality (Line No: 69, 78, etc.)
	* Might be necessary to add more error catching procedures via delay or otherwise
	* Possibly avoid line 240
* Clean up error handling for import functions (error 1001 in applescript) (Line No: 76, 85, as well as applescript code)
	* Ensure that time-lapse photos are not able to be processed by importAll() as well
* Check .codes of applescript processes before returning from methods which use them
* Make transferPhotos() even more modular?
* Reduce line lengths to 80 characters
* Re-test edges cases to ensure successful porting from bash for each
* Check edge case in which Python is already open upon running of the program
* Check edge case in which photo is deleted while iphone connected
* Change photoClient to previewClient for clarity

# Possible future updates for transferPhotos:
* Updating ReadMe
* Forking applescript package to include parameters (Line No: 70, 79)
	* applescript.run("./scripts/batchImport.scpt") with argv
* Updating Terminal output with while loop to say "x files imported of y files"
	* Inserted after line 240 would be getting original fileCount of directory if necessary
		* fileNumOrig="$(find "$filePath" ! -path "$filePath" ! -path "*/\.*" -prune -print | grep -c /)"
	* Inserted after line 252 would be while loop until Preview exits which updates files imported

# Future updates for archiver
* Sort through imported pictures based on month, and whether picture is a screenshot or photo
* More...