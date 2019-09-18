-- Returns true if full time is waited out, false if photos show up before then.
-- Necessary for distinguishing amongst three cases:
----(1) The images are taking a long time to load
----(2) The device is not unlocked
----(3) There are no images to import
on fullDelay()
	tell application "System Events"
		tell process "Preview"
			set maxCounter to 0
			repeat until (maxCounter is 5) or (value of static text 1 of group 1 of window 1 is not "0 items")
				delay 3
				set maxCounter to maxCounter + 1
			end repeat
			if value of static text 1 of group 1 of window 1 is not "0 items" then
				return false
			end if
		end tell
	end tell
	return true
end fullDelay

on main()
	try
		fullDelay()
	on error errStr number errNum
		if errNum = -1719 or errNum = -1728 then
			return "fullDelay.scpt has encountered error " & errNum & ". This is more often than not a result of user interference during UI navigation."
		else
			return "fullDelay.scpt has encountered an error on import: " & errStr
		end if
	end try
end main

on run()
	main()
end main