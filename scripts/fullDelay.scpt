-- Returns true if full time is waited out, false if photos show up before then
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
	fullDelay()
end main

on run()
	main()
end main