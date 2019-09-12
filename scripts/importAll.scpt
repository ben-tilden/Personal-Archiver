-- Imports all photos from "Import from " & iPhoneName window. Quits after import is finished.
on importAll(filePath)
	tell application "System Events"
		tell process "Preview"
			log ("Begin")
			set rowCount to 0
			-- rowCount updates as more photos are identified
			repeat until rowCount = (count rows of table 1 of scroll area 1 of group 1 of window 1)
				set rowCount to count rows of table 1 of scroll area 1 of group 1 of window 1
			end repeat
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
			-- Photos begin importing here
			-- if rowCount = 1 then rowCount & " documents" will not appear in name of window 1
			if rowCount = 1 then
				-- if rowCount = 1 then rowCount & " documents" will not appear in name of window 1
				repeat until name of window 1 does not contain "Import from"
					delay 0.5
				end repeat
			else
				repeat until (name of window 1 contains rowCount & " documents") and (name of window 1 does not contain "Import from")
					-- second conditional covers edge case in which iPhone is named rowCount & " documents"
					-- window 1 for the first few iterations of this is still "Import from " & iPhoneName
					delay 5
					if (name of window 1 contains "Import from") and (sheet 1 of window 1 exists) then -- sheet containing error message
						click button 1 of sheet 1 of window 1
						error 1001
					end if
				end repeat
			end if
		end tell
	end tell
end importAll

on main(filePath)
	try
		importAll(filePath)
	on error 1001
		return "error"
	end try
end main

on run(argv)
	main(item 1 of argv)
end run