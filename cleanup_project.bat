@echo off
setlocal enabledelayedexpansion

:: Set working directory (change if needed)
set "TARGET_DIR=."

cd /d "%TARGET_DIR%"

:: Preserve these files
set "KEEP1=pyproject.toml"
set "KEEP2=cleanup_project.bat"

:: Delete all files except the ones we want to keep
for %%f in (*.*) do (
    if /I not "%%f"=="%KEEP1%" (
    if /I not "%%f"=="%KEEP2%" (
        del /f /q "%%f"
    ))
)

:: Preserve these folders
set "KEEPDIR1=.git"
set "KEEPDIR2=.github"
set "KEEPDIR3=data"
set "KEEPDIR4=docs"

:: Delete all directories except the preserved ones
for /d %%d in (*) do (
    set "folder=%%d"
    if /I not "!folder!"=="%KEEPDIR1%" (
    if /I not "!folder!"=="%KEEPDIR2%" (
    if /I not "!folder!"=="%KEEPDIR3%" (
    if /I not "!folder!"=="%KEEPDIR4%" (
        rd /s /q "!folder!"
    ))))
)

echo Cleanup complete.