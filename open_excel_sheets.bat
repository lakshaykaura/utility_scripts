@echo off
setlocal enabledelayedexpansion

echo Enter the directory path:
set /p "DirectoryPath="

echo Enter the path to the list of files (file_list.txt):
set /p "FileList="

set "TotalFiles=0"
set "OpenedFiles=0"
set "OpenCount=0"
set "OpenedFileNames=|"

for /f "usebackq delims=" %%i in ("%FileList%") do (
    set /a "TotalFiles+=1"
)

for /f "usebackq delims=" %%i in ("%FileList%") do (
    set "FilePath=%DirectoryPath%\%%i"
    set "FilePath=!FilePath:/=\!"
    if exist "!FilePath!" (
        set "FileName=%%~nxi"
		set "fileAlreadyOpened=false"
		call :duplicateCheckLoop
	) else (
        echo File not found: "!FilePath!"
    )
)

if !OpenCount! GTR 0 (
    echo Opened all !OpenedFiles! Excel files out of !TotalFiles!.
    echo Please close all opened Excel files to continue.
    pause
) else (
    echo Opened all !OpenedFiles! Excel files out of !TotalFiles!.
    pause
)

:duplicateCheckLoop
	:: Remove first and last delimiter
	set "inputString=!OpenedFileNames:~1,-1!"
	:: Iterate through the string and print each item
	for %%a in ("%inputString:|=" "%") do (
		if "%%~a"=="!FileName!" (
			set "fileAlreadyOpened=true"
			goto :breakAndProceedNextSteps
		)
	)

:breakAndProceedNextSteps
	if "!fileAlreadyOpened!"=="true" (
		echo Script tried to open another excel file with same name as "!FileName!".
		echo Opened !OpenedFiles! out of !TotalFiles!. Please close all opened Excel files to continue.
		pause
		set "OpenCount=0"
		set "OpenedFileNames=|"
	)
	set "OpenedFileNames=!OpenedFileNames!!FileName!|"
	set /a OpenedFiles+=1
	ping 127.0.0.1 -n 1 -w 500 >nul
	start excel "!FilePath!"
	set /a OpenCount+=1
	
	if !OpenCount! == 50 (
		echo Script limit reached.
		echo Opened !OpenedFiles! out of !TotalFiles!. Please close all opened Excel files to continue.
		pause
		set "OpenCount=0"
		set "OpenedFileNames=|"
	)
