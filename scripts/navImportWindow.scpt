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
	navImportWindow()
end main

on run()
	main()
end main