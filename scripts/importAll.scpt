-- Imports all photos from "Import from " & iPhoneName window. Quits after import is finished.
on importAll(filePath)
	set vidOnly to isVidOnly()
	navFilePath(filePath)
	waitForImport(vidOnly)
end importAll

on navFilePath(filePath)
	tell application "System Events"
		tell process "Preview"
			click button "Import All" of group 1 of window 1
			set frontmost to true
			repeat until sheet 1 of window 1 exists
				delay 0.1
			end repeat
			keystroke "g" using {shift down, command down}
			repeat until sheet 1 of sheet 1 of window 1 exists
				delay 0.1
			end repeat
			keystroke filePath
			key code 36
			click button "Choose Destination" of sheet 1 of window 1
		end tell
	end tell
end navFilePath

-- Returns true if all elements to be imported are videos, false otherwise
on isVidOnly()
	tell application "System Events"
		tell process "Preview"
			repeat with x from 1 to (count the rows of table 1 of scroll area 1 of group 1 of window 1)
				if (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "MOV") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "M4V") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "MP4") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "3G2") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "3GP") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "3GP2") or (value of static text of UI element 3 of row x of table 1 of scroll area 1 of group 1 of window 1 does not contain "3GPP") then
					return false
				end if
			end repeat
			return true
		end tell
	end tell
end isVidOnly

-- Waits for import of batch to complete
on waitForImport(vidOnly)
	tell application "System Events"
		tell process "Preview"
			if vidOnly is true then -- there are only videos in the import
				repeat until not (button "Cancel" of group 1 of window 1 exists)
					delay 3
					my timeLapseCheck()
				end repeat
			else -- there are some photo files
				repeat until name of window 1 does not contain "Import from"
					delay 1
					my timeLapseCheck()
				end repeat
				repeat until not (button "Cancel" of group 1 of window 1 exists)
					delay 3
					my timeLapseCheck()
				end repeat
			end if
		end tell
	end tell
end waitForImport

-- Checks for time lapse video error
on timeLapseCheck()
	tell application "System Events"
		tell process "Preview"
			if sheet 1 of window 1 exists then -- sheet containing error message
				click button 1 of sheet 1 of window 1
				if button 1 of sheet 1 of window 1 exists then
					click button 1 of sheet 1 of window 1
				end if
				error 1001
			end if
		end tell
	end tell
end timeLapseCheck

on main(filePath)
	try
		importAll(filePath)
		return "success"
	on error errStr number errNum
		if errStr = 1001 then
			return "importAll.scpt has encountered a time-lapse photo on import"
		else if errNum = -1719 or errNum = -1728 then
			return "importAll.scpt has encountered error " & errNum & ". This is more often than not a result of user interference during UI navigation."
		else
			return "importAll.scpt has encountered an error on import: " & errStr
		end if
	end try
end main

on run(argv)
	main(item 1 of argv)
end run