@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:menu
cls
echo ----------------------------------
echo Windows Makefile - Summer Camp Project
echo ----------------------------------
echo 1. Setup (Create venv and install requirements)
echo 2. Run Django server
echo 3. Freeze requirements.txt
echo 4. Clean (Delete virtual environment)
echo 5. Exit
echo ----------------------------------
set /p choice=Choose an option:

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto run
if "%choice%"=="3" goto freeze
if "%choice%"=="4" goto clean
if "%choice%"=="5" exit

goto menu

:setup
if not exist env (
    echo Creating virtual environment...
    python -m venv env
)
echo Activating virtual environment and installing requirements...
call env\Scripts\activate
pip install -r requirements.txt
pause
goto menu

:run
echo Activating virtual environment...
call env\Scripts\activate
echo Starting Django development server...
python manage.py runserver
pause
goto menu

:freeze
echo Activating virtual environment...
call env\Scripts\activate
echo Freezing current dependencies into requirements.txt...
pip freeze > requirements.txt
pause
goto menu

:clean
echo Deleting virtual environment...
rmdir /s /q env
pause
goto menu
