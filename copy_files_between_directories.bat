@echo off
setlocal enabledelayedexpansion

echo Enter the source directory:
set /p "Directory_A="

echo Enter the destination directory:
set /p "Directory_B="

echo Enter the path to the list of files (file_list.txt):
set /p "fileList="

set "successCount=0"
set "failureCount=0"

for /f "usebackq delims=" %%i in ("%fileList%") do (
    set "source=%Directory_A%\%%i"
    set "destination=%Directory_B%\%%i"
    set "source=!source:/=\!"
    set "destination=!destination:/=\!"
    set "destination_folder=!destination!\.."
    if not exist "!source!" (
        echo File not found: "!source!"
        set /a "failureCount+=1"
    ) else (
        robocopy "!source!\.." "!destination_folder!" "%%~nxi" /is
        if errorlevel 2 (
            echo Failed to copy: "!source!" to "!destination!"
            set /a "failureCount+=1"
        ) else (
            echo Successfully copied: "!source!" to "!destination!"
            set /a "successCount+=1"
        )
    )
)

echo Total successful copies: %successCount%
echo Total failures: %failureCount%

endlocal