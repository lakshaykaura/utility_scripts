@echo off
setlocal enabledelayedexpansion

echo Enter the directory path:
set /p "DirectoryPath="

echo Enter the comma-separated extensions (e.g., txt,properties) or leave empty for all extensions:
set /p "Extensions="

set "TotalFileCount=0"

if not "%Extensions%"=="" (
    echo Running for extensions: [%Extensions%]
    for %%a in (%Extensions%) do (
        set "FileCount=0"
        for /r "%DirectoryPath%" %%i in (*.%%a) do (
            set /a "FileCount+=1"
            set /a "TotalFileCount+=1"
        )
        echo Files with extension '.%%a': !FileCount!
    )
) else (
    echo Running for all extensions...
    for /r "%DirectoryPath%" %%i in (*) do (
        set /a "TotalFileCount+=1"
        set "Ext=%%~xi"
        if not defined CountPerExtension[!Ext!] (
            set /a CountPerExtension[!Ext!]=1
        ) else (
            set /a CountPerExtension[!Ext!]+=1
        )
    )
    for /f "tokens=2,3 delims=[]=" %%a in ('set CountPerExtension[') do (
        echo Files with extension '%%a': %%b
    )
)

echo Total number of files with all extensions: !TotalFileCount!
