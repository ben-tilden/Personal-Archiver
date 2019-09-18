-- Navigates the window labelled "Import from " & iPhoneName.
on navImportWindow()
	tell application "System Events"
		tell process "Preview"
			set maxCounter to 0
			repeat until (maxCounter is 5) or (sheet 1 of window 1 exists)
				delay 0.2
				set maxCounter to maxCounter + 1
			end repeat
			if exists sheet 1 of window 1 then -- sheet which requests iPhone unlock
				click button 1 of sheet 1 of window 1
			end if
		end tell
	end tell
end navImportWindow

on main()
	try
		navImportWindow()
		return "success"
	on error errStr number errNum
		if errNum = -1719 or errNum = -1728 then
			return "navImportWindow.scpt has encountered error " & errNum & ". This is more often than not a result of user interference during UI navigation."
		else
			return "navImportWindow.scpt has encountered an error on import: " & errStr
		end if
	end try
end main

on run()
	main()
end main