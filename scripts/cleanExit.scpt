-- Exits Preview cleanly
on cleanExit()
	tell application "System Events"
		if (exists (processes where name is "Preview")) then
			if (exists window 1 of process "Preview") and (name of window 1 of process "Preview" contains "Import from") then
				if exists sheet 1 of window 1 of process "Preview" then
					click button 1 of sheet 1 of window 1 of process "Preview"
					if exists sheet 1 of window 1 of process "Preview" then -- in case of time-lapse video
						click button 1 of sheet 1 of window 1 of process "Preview"
					end if
				else if exists sheet 1 of sheet 1 of window 1 of process "Preview" then
					click button 1 of sheet 1 of sheet 1 of window 1 of process "Preview"
				end if
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
		if errStr starts with "osascript" then
			set errStr to ((characters 10 thru -1 of errStr) as string)
			set errStr to "Terminal" & errStr
		end if
		return "cleanExit.scpt has encountered an error on import: " & errStr
	end try
end main

on run()
	main()
end run