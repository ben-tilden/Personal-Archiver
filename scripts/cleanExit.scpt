-- Exits Preview cleanly
on cleanExit()
	tell application "System Events"
		if (exists (processes where name is "Preview")) and (name of window 1 of process "Preview" contains "Import from") then
			if exists sheet 1 of window 1 of process "Preview" then
				click button 1 of sheet 1 of window 1 of process "Preview"
			else if exists sheet 1 of sheet 1 of window 1 of process "Preview" then
				click button 1 of sheet 1 of sheet 1 of window 1 of process "Preview"
			end if
			if exists sheet 1 of window 1 of process "Preview" then -- in case of time-lapse video
				click button 1 of sheet 1 of window 1 of process "Preview"
			end if
			tell application "Preview" to quit
		end if
	end tell
end cleanExit

on main()
	try
		cleanExit()
		return "success"
	on error errStr number errNum
		if errNum = -1719 or errNum = -1728 then
			return "cleanExit.scpt has encountered error " & errNum & ". This is more often than not a result of user interference via Preview manipulation or otherwise."
		else
			return "cleanExit.scpt has encountered an error on import: " & errStr
		end if
	end try
end main

on run()
	main()
end run