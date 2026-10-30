@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0"
title Streamline Master - benchmark

echo ==========================================================
echo   Streamline Master - benchmark dwoch instancji (MC 26.3)
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
if not exist "bench_setup.py" goto :wrongfolder

echo Twoje instancje (launcher, wersja Minecrafta, nazwa):
echo.
%PY% bench_setup.py list
echo.
echo Wpisz nazwe instancji albo jej fragment, np. "Streamline".
echo.
set /p A=Instancja ze Streamline Master: 
if "%A%"=="" goto :noinst
set /p B=Instancja do porownania (np. Fabulously Optimized): 
if "%B%"=="" goto :noinst

echo.
%PY% bench_setup.py install "%A%" --label SLM
if errorlevel 1 goto :failed
%PY% bench_setup.py install "%B%" --label FO
if errorlevel 1 goto :failed

echo.
echo ----------------------------------------------------------
echo Teraz uruchom w launcherze KAZDA z tych dwoch instancji raz.
echo Benchmark sam tworzy swiat, leci po stalej trasie (ok. 2 minut)
echo i zamyka gre. Nie ruszaj myszka w trakcie.
echo Kiedy obie sie zamkna, wroc tutaj i nacisnij dowolny klawisz.
echo ----------------------------------------------------------
pause >nul

echo.
%PY% bench_setup.py compare "%A%" "%B%"
echo.
set /p R=Usunac benchmark z obu instancji? [T/n]: 
if /i "%R%"=="n" goto :end
%PY% bench_setup.py remove "%A%"
%PY% bench_setup.py remove "%B%"
:end
echo.
pause
exit /b 0

:nopython
echo BLAD: nie znaleziono Pythona.
echo   winget install Python.Python.3.12
pause
exit /b 1

:wrongfolder
echo BLAD: w tym folderze nie ma bench_setup.py.
echo Ten plik musi lezec w folderze projektu Streamline Master.
pause
exit /b 1

:noinst
echo Nie podano instancji.
pause
exit /b 1

:failed
echo.
echo Instalacja sie nie udala - powod jest wyzej.
pause
exit /b 1
