@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0"
title Streamline Master - strojenie instancji

echo ==========================================================
echo   Streamline Master - argumenty JVM, pamiec i GPU
echo ==========================================================
echo.
echo Paczka .mrpack nie przenosi argumentow JVM ani wyboru karty
echo graficznej. Ten skrypt ustawia je w instancji Prism Launchera.
echo.
echo ZAMKNIJ Prism Launcher przed kontynuacja - przy wyjsciu
echo nadpisuje instance.cfg i zmiany by przepadly.
echo.

set "PY="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if defined PY goto :havepy
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
:havepy
if not defined PY goto :nopython

if not exist "tune.py" goto :wrongfolder

set "INST=%~1"
if not "%INST%"=="" goto :haveinst
echo Podaj folder instancji Prism Launchera.
echo   Prism: klik prawym na instancji, "Folder" (ten z instance.cfg)
echo.
echo Mozesz tez przeciagnac ten folder na plik tune.cmd.
echo.
set /p INST=Sciezka do folderu: 
:haveinst
if "%INST%"=="" goto :noinst

echo.
%PY% tune.py "%INST%" --gpu
echo.
echo ----------------------------------------------------------
echo Zmiany dzialaja od nastepnego uruchomienia instancji.
echo Kopia poprzedniego instance.cfg lezy obok jako instance.cfg.bak.
echo Wybor GPU cofniesz w: Ustawienia, Ekran, Grafika.
echo ----------------------------------------------------------
pause
exit /b 0

:nopython
echo BLAD: nie znaleziono Pythona.
echo   winget install Python.Python.3.12
pause
exit /b 1

:wrongfolder
echo BLAD: w tym folderze nie ma tune.py.
echo Ten plik musi lezec w folderze projektu Streamline Master.
echo Aktualny folder: %CD%
pause
exit /b 1

:noinst
echo Nie podano folderu instancji.
pause
exit /b 1
