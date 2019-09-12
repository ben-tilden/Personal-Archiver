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
	openPreview()
end main

on run()
	main()
end run