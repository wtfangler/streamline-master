@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0"
title Streamline Master - build

echo ==========================================================
echo   Streamline Master - budowanie paczek
echo ==========================================================
echo.

set "PY="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if defined PY goto :havepy
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
:havepy
if not defined PY goto :nopython

if not exist "manifest.json" goto :wrongfolder

echo [1/3] Rozwiazywanie wersji modow i budowanie...
echo.
%PY% build.py --clean
if errorlevel 1 goto :buildfailed

echo.
echo [2/3] Walidacja paczek...
echo.
%PY% validate.py "dist\*.mrpack" --online
if errorlevel 1 goto :validatefailed

echo.
echo [3/3] Gotowe.
echo.
echo Paczki leza w folderze: %CD%\dist
echo.
echo Co dalej:
echo   1. Otworz launcher (Prism albo aplikacja Modrinth)
echo   2. Dodaj instancje z pliku .mrpack - jako NOWA instancje,
echo      nie aktualizuj starej
echo   3. W ustawieniach instancji wklej argumenty JVM z docs\tuning.md
echo.
start "" explorer "%CD%\dist"
pause
exit /b 0

:nopython
echo BLAD: nie znaleziono Pythona.
echo.
echo Zainstaluj go jedna z dwoch drog:
echo   - w PowerShellu:  winget install Python.Python.3.12
echo   - albo ze strony python.org, zaznaczajac przy instalacji
echo     "Add python.exe to PATH"
echo.
echo Potem uruchom ten plik jeszcze raz.
pause
exit /b 1

:wrongfolder
echo BLAD: w tym folderze nie ma manifest.json.
echo.
echo Ten plik musi lezec w folderze projektu Streamline Master,
echo obok manifest.json, build.py i validate.py.
echo To NIE jest folder instancji Minecrafta.
echo.
echo Aktualny folder: %CD%
pause
exit /b 1

:buildfailed
echo.
echo BLAD podczas budowania. Tresc bledu jest wyzej.
echo Najczestsza przyczyna: brak dostepu do api.modrinth.com.
pause
exit /b 1

:validatefailed
echo.
echo Walidacja znalazla problemy - lista jest wyzej.
echo Paczki sa w folderze dist, ale nie publikuj ich, dopoki to nie przejdzie.
pause
exit /b 1
