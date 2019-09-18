-- Checks if there are multiple devices connected.
on isMultipleDevices()
	tell application "System Events"
		tell process "Preview"
			if menu item 2 of menu 1 of menu item 18 of menu 1 of menu bar item "File" of menu bar 1 exists then
				return true
			else
				return false
			end if
		end tell
	end tell
end isMultipleDevices

on main()
	try
		isMultipleDevices()
	on error errStr number errNum
		return "isMultipleDevices.scpt has encountered an error on import: " & errStr
	end try
end main

on run()
	main()
end main