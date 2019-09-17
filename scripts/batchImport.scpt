-- Imports all photos in batches from "Import from " & iPhoneName window; default is 100.
-- Sometimes more consistent for larger imports. Quits after import is finished.
on batchImport(batchNum, filePath)
	tell application "System Events"
		tell process "Preview"
			set firstLoop to true
			set rowNum to 0
			set rowCount to 0
			-- rowCount updates as more photos are identified
			repeat until rowCount = (count rows of table 1 of scroll area 1 of group 1 of window 1)
				set rowCount to count rows of table 1 of scroll area 1 of group 1 of window 1
			end repeat
			set frontmost to true
			repeat until rowNum = rowCount
				perform action "AXRaise" of window 1
				set selectionNum to my getSelectionNum(rowNum, rowCount, batchNum)
				set highlightVars to my highlightSelection(selectionNum, rowNum)
				set rowNum to item 1 of highlightVars
				set vidNum to item 2 of highlightVars
				set firstLoop to my navFilePath(firstLoop, filePath)
				-- Photos begin importing here
				my waitForImport(vidNum, selectionNum)
			end repeat
		end tell
	end tell
end batchImport

-- Returns batchNum if there are batchNum or more photos left, the number of photos left otherwise
on getSelectionNum(rowNum, rowCount, batchNum)
	if batchNum < rowCount - rowNum then
		return batchNum
	else
		return rowCount - rowNum
	end if
end getSelectionNum

-- Selects all photos to be imported in one batch
-- Returns list with updated rowNum and the number of videos in the batch (vidNum)
on highlightSelection(selectionNum, rowNum)
	tell application "System Events"
		tell process "Preview"
			set firstSelect to true
			set vidNum to 0
			repeat selectionNum times
				if firstSelect is true then
					key code 125 -- first keystroke begins new batch selection separate from last
					set rowNum to rowNum + 1
					set firstSelect to false
				else
					key code 125 using shift down
					set rowNum to rowNum + 1
				end if
				if value of static text of UI element 3 of row rowNum of table 1 of scroll area 1 of group 1 of window 1 contains "MOV" then -- or
					set vidNum to vidNum + 1
				end if
			end repeat
		end tell
	end tell
	return {rowNum, vidNum}
end highlightSelection

-- Navigates Preview windows deciding file path after "Import" button is clicked; Returns firstLoop
on navFilePath(firstLoop, filePath)
	tell application "System Events"
		tell process "Preview"
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
		end tell
	end tell
	return firstLoop
end navFilePath

-- Waits for import of batch to complete
on waitForImport(vidNum, selectionNum)
	tell application "System Events"
		tell process "Preview"
			if vidNum = selectionNum then -- there are only videos in the batch
				repeat until enabled of button "Import All" of group 1 of window 1 is true
					delay 3
					my timeLapseCheck()
				end repeat
			else -- there are some photo files
				repeat until name of window 1 does not contain "Import from"
					delay 1
					my timeLapseCheck()
				end repeat
				repeat until enabled of button "Import All" of group 1 of window 2 is true
					delay 3
					my timeLapseCheck()
				end repeat
			end if
			if name of window 1 does not contain "Import from" then
				click button 1 of window 1
			end if
			repeat until name of window 1 contains "Import from"
				delay 0.2
			end repeat
		end tell
	end tell
end waitForImport

-- Checks for time lapse video error
on timeLapseCheck()
	tell application "System Events"
		tell process "Preview"
			if sheet 1 of window 1 exists then -- sheet containing error message
				click button 1 of sheet 1 of window 1
				if button 1 of sheet 1 of window 1 exists then
					click button 1 of sheet 1 of window 1
				end if
				error 1001
			end if
		end tell
	end tell
end timeLapseCheck

on main(batchNum, filePath)
	try
		batchImport(batchNum, filePath)
		return "success"
	on error errStr number errNum
		if errStr = 1001 then
			return "batchImport.scpt has encountered a time-lapse photo on import"
		else if errNum = -1719 or errNum = -1728 then
			return "batchImport.scpt has encountered error " & errNum & ". This is more often than not a result of user manipulation during UI navigation."
		else
			return "batchImport.scpt has encountered an error on import: " & errStr
		end if
	end try
end main

on run (argv)
	main(item 1 of argv, item 2 of argv) --batchNum, filePath
end run