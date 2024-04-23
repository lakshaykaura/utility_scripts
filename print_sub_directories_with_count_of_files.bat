@echo off
setlocal enabledelayedexpansion

echo Enter the directory path:
set /p "directory="

if "%directory%"=="" set directory=.

echo Scanning subdirectories in %directory%...

for /D %%i in ("%directory%\*") do (
    set /a count=0
    for %%x in ("%%i\*") do (
        if not "%%~dpx"=="%%i\" (
            set /a count+=1
        )
    )
    echo %%~nxi, !count!
)

endlocal