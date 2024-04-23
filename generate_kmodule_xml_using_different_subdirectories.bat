@echo off
setlocal enabledelayedexpansion

set /p BASE_PATH="Enter the base directory path: "

echo ^<kmodule xmlns="http://www.drools.org/xsd/kmodule"^> > kmodule.xml

set /p DRLS_PACKAGE_STR ="Enter the DRLs package: "
set /p DTABLES_PACKAGE_STR ="Enter the DTables package: "

for /l %%i in (0,1,210) do (
    set "DRLS_PACKAGE=%DRLS_PACKAGE_STR%.L%%i"
    set "DTABLES_PACKAGE=%DTABLES_PACKAGE_STR%.L%%i"
    
    if exist "%BASE_PATH%\drls\L%%i" (
        if exist "%BASE_PATH%\dtables\L%%i" (
            echo    ^<kbase name="rulesL%%i" default="true" packages="!DRLS_PACKAGE!,!DTABLES_PACKAGE!"^> >> kmodule.xml
        ) else (
            echo    ^<kbase name="rulesL%%i" default="true" packages="!DRLS_PACKAGE!"^> >> kmodule.xml
        )
    ) else (
        if exist "%BASE_PATH%\dtables\L%%i" (
            echo    ^<kbase name="rulesL%%i" default="true" packages="!DTABLES_PACKAGE!"^> >> kmodule.xml
        )
    )
    
    if exist "%BASE_PATH%\drls\L%%i" (
        echo        ^<ksession name="sessionL%%i" default="true" type="stateless"/^> >> kmodule.xml
    ) else (
        if exist "%BASE_PATH%\dtables\L%%i" (
            echo        ^<ksession name="sessionL%%i" default="true" type="stateless"/^> >> kmodule.xml
        )
    )
    
    if exist "%BASE_PATH%\drls\L%%i" (
        echo    ^</kbase^> >> kmodule.xml
    ) else (
        if exist "%BASE_PATH%\dtables\L%%i" (
            echo    ^</kbase^> >> kmodule.xml
        )
    )
)

for /l %%i in (0,1,210) do (
    for /l %%j in (0,1,9) do (
        set "DTABLES_PACKAGE=abc.ruleengine.rules.dtables.L%%i.%%j"
        
        if exist "%BASE_PATH%\dtables\L%%i.%%j" (
            echo ^<kbase name="rulesL%%i_%%j" default="true" packages="!DTABLES_PACKAGE!"^> >> kmodule.xml
            echo     ^<ksession name="sessionL%%i_%%j" default="true" type="stateless"/^> >> kmodule.xml
            echo ^</kbase^> >> kmodule.xml
        )
    )
)

echo ^</kmodule^> >> kmodule.xml