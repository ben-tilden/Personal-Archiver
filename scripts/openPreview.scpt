-- Opens Preview.
on openPreview()
	tell application "Preview" to activate
	tell application "System Events"
		repeat until window 1 of "Preview" exists
			delay 1
		end repeat
	end tell
end openPreview

on main()
	try
		openPreview()
		return "success"
	on error errStr number errNum
		return "openPreview.scpt has encountered an error on import: " & errStr
	end try
end main

on run()
	main()
end run