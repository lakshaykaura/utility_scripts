@echo off
setlocal enabledelayedexpansion

echo Enter the directory path:
set /p "DirectoryPath="

echo Enter the output file name (e.g., filenames.txt):
set /p "OutputFile="

if exist "%DirectoryPath%\%OutputFile%" (
    del /q /f "%DirectoryPath%\%OutputFile%"
)

cd /d "%DirectoryPath%"

for /r %%i in (*) do (
    set "FullPath=%%i"
    set "ParentDir=%DirectoryPath%"
    
    call :GetRelativePath "!FullPath!" "!ParentDir!" RelativePath
    echo !RelativePath! >> "%DirectoryPath%\%OutputFile%"
)

echo File paths have been written to %OutputFile%.

goto :eof

:GetRelativePath
set "FullPath=%~1"
set "ParentDir=%~2"
set "RelativePath=!FullPath:%ParentDir%=!"
set "RelativePath=!RelativePath:~1!"
set "%3=!RelativePath!"
exit /b
