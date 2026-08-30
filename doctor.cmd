@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0"
title Streamline Master - diagnostyka instancji

echo ==========================================================
echo   Streamline Master - porownanie instancji z paczka
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

if not exist "doctor.py" goto :wrongfolder

set "INST=%~1"
if not "%INST%"=="" goto :haveinst
echo Podaj folder instancji Minecrafta.
echo.
echo Gdzie go znalezc:
echo   Prism Launcher     - klik prawym na instancji, "Folder"
echo   aplikacja Modrinth - w profilu, przycisk "Open folder"
echo.
echo Mozesz tez przeciagnac ten folder na plik doctor.cmd.
echo.
set /p INST=Sciezka do folderu: 
:haveinst
if "%INST%"=="" goto :noinst

set "MC=26.2"
echo.
set /p MC=Wersja Minecrafta [26.2]: 
if "%MC%"=="" set "MC=26.2"

set "PACK=dist\Streamline Master %MC%.mrpack"
if not exist "%PACK%" goto :nopack

echo.
%PY% doctor.py "%PACK%" "%INST%"
echo.
echo ----------------------------------------------------------
echo MISSING  - moda z paczki nie ma w instancji
echo EXTRA    - jar, ktorego paczka nie definiuje
echo ABSENT   - plik z overrides nigdy nie trafil do instancji
echo DIFFERS  - plik z overrides ma w instancji inna tresc
echo.
echo ABSENT albo DIFFERS oznacza, ze launcher nie nadpisal plikow
echo przy aktualizacji paczki w miejscu. Skasuj te pliki w instancji
echo i przeinstaluj, albo zainstaluj do nowej instancji.
echo ----------------------------------------------------------
pause
exit /b 0

:nopython
echo BLAD: nie znaleziono Pythona.
echo   winget install Python.Python.3.12
pause
exit /b 1

:wrongfolder
echo BLAD: w tym folderze nie ma doctor.py.
echo Ten plik musi lezec w folderze projektu Streamline Master.
echo Aktualny folder: %CD%
pause
exit /b 1

:noinst
echo Nie podano folderu instancji.
pause
exit /b 1

:nopack
echo BLAD: nie ma pliku "%PACK%".
echo Najpierw uruchom build.cmd.
pause
exit /b 1
