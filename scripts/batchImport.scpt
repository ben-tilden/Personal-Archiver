-- Imports all photos in batches from "Import from " & iPhoneName window; default is 100.
-- Sometimes more consistent for larger imports. Quits after import is finished.
on batchImport(batchNum, filePath)
	tell application "System Events"
		tell process "Preview"
			set firstLoop to true
			set rowNum to 0
			set rowCount to 0
			set windowNum to 0
			-- rowCount updates as more photos are identified
			repeat until rowCount = (count rows of table 1 of scroll area 1 of group 1 of window 1)
				set rowCount to count rows of table 1 of scroll area 1 of group 1 of window 1
			end repeat
			set frontmost to true
			repeat until rowNum = rowCount
				key code 125 -- first keystroke begins new batch selection separate from last
				set rowNum to rowNum + 1
				-- if statement ensures no extra work is done if the last selection is smaller than batchNum
				if batchNum - 1 < rowCount - rowNum then -- batchNum - 1 because the first down keystroke is already done
					set windowNum to batchNum
					repeat batchNum - 1 times
						key code 125 using shift down
						set rowNum to rowNum + 1
					end repeat
				else
					set windowNum to rowCount - rowNum + 1
					repeat rowCount - rowNum times
						key code 125 using shift down
						set rowNum to rowNum + 1
					end repeat
				end if
				click button "Import" of group 1 of window 1
				repeat until sheet 1 of window 1 exists
					delay 0.1
				end repeat
				keystroke "g" using {shift down, command down}
				repeat until sheet 1 of sheet 1 of window 1 exists
					delay 0.1
				end repeat
				if firstLoop then -- defaults to last given path after first enter
					keystroke filePath
					set firstLoop to false
				end if
				key code 36
				click button "Choose Destination" of sheet 1 of window 1
				-- Photos begin importing here
				-- if rowCount = 1 then rowCount & " documents" will not appear in name of window 1
				if windowNum = 1 then
					repeat until name of window 1 does not contain "Import from"
						delay 0.5
					end repeat
				else
					repeat until (name of window 1 contains windowNum & " documents") and (name of window 1 does not contain "Import from")
						-- second conditional covers edge case in which iPhone is named windowNum & " documents"
						-- window 1 for the first few iterations of this is still "Import from " & iPhoneName
						delay 5
						if (name of window 1 contains "Import from") and (sheet 1 of window 1 exists) then -- sheet containing error message
							click button 1 of sheet 1 of window 1
							error 1001
						end if
					end repeat
				click button 1 of window 1
				repeat until name of window 1 contains "Import from"
					delay 0.2
				end repeat
				end if
			end repeat
		end tell
	end tell
end batchImport

on main(batchNum, filePath)
	try
		batchImport(batchNum, filePath)
	on error 1001
		return "error"
	end try
end main

on run(argv)
	main(item 1 of argv, item 2 of argv) --batchNum, filePath
end run