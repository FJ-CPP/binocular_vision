@echo off
REM Save the current directory
set "root_dir=%CD%"

REM Create a new directory if it doesn't exist and navigate into it
if not exist "data\MiddleBury_2021\" (
    mkdir "data\MiddleBury_2021"
)
cd "data\MiddleBury_2021"

REM Download the dataset zip file using PowerShell
powershell -command "Invoke-WebRequest -Uri 'https://vision.middlebury.edu/stereo/data/scenes2021/zip/all.zip' -OutFile 'all.zip'"

REM Extract the contents of the zip file and delete the zip file
powershell -command "Expand-Archive -Path 'all.zip' -DestinationPath '.'"
del "all.zip"

REM Move the files up from the 'data' subdirectory and remove it
powershell -command "move 'data\*' '.'"
rmdir /s /q "data"

REM Navigate back to the original directory
cd %root_dir%

@echo on