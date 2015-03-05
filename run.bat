@echo off
REM Note: Only tested on Windows 7 x64
setLocal EnableDelayedExpansion

REM config
set distro=C:\Anaconda\python.exe 
set target=code
set pycol=0a
set col=0C
REM end config

for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)
cd code
cls

:init
set this=init
set next=settings
call :ColorText 0 "Welcome,"
call :ColorText %col% " NetSci High Team"
echo .
echo This program provides an interface for running the multiple python scrips.
goto choice

:last_choice
echo.
call :ColorText 0 "Sequence is done. Press"
call :ColorText %col% " Q"
echo  to QUIT or choose from the list below:
call :ColorText %col% "1"
echo  - 'settings.py'
call :ColorText %col% "2"
echo  - 'parseCSV.py'
call :ColorText %col% "3"
echo  - 'calculate_stats.py'
call :ColorText %col% "4"
echo  - 'set_threshold.py'
call :ColorText %col% "5"
echo  - 'write_graph.py'
call :ColorText %col% "6"
echo  - 'draw_graph.py'
call :ColorText %col% "R"
echo  - Restart Batch
choice /C 123456QR /N /M "Selection: "
echo.
IF ERRORLEVEL 8 GOTO init
IF ERRORLEVEL 7 GOTO quit
IF ERRORLEVEL 6 GOTO draw_graph
IF ERRORLEVEL 5 GOTO write_graph
IF ERRORLEVEL 4 GOTO set_threshold
IF ERRORLEVEL 3 GOTO calculate_stats
IF ERRORLEVEL 2 GOTO parseCSV
IF ERRORLEVEL 1 GOTO settings

:choice
echo.
call :ColorText 0 "Next in the sequence is"
call :ColorText %pycol% " '!next!.py'"
echo.
call :ColorText 0 "Press"
call :ColorText %col% " C"
echo  or choose from the list below:
call :ColorText %col% "1"
echo  - 'settings.py'
call :ColorText %col% "2"
echo  - 'parseCSV.py'
call :ColorText %col% "3"
echo  - 'calculate_stats.py'
call :ColorText %col% "4"
echo  - 'set_threshold.py'
call :ColorText %col% "5"
echo  - 'write_graph.py'
call :ColorText %col% "6"
echo  - 'draw_graph.py'
call :ColorText %col% "Q"
echo  - Quit
choice /C 123456QC /N /M "Selection: "
echo.
IF ERRORLEVEL 8 GOTO !next!
IF ERRORLEVEL 7 GOTO quit
IF ERRORLEVEL 6 GOTO draw_graph
IF ERRORLEVEL 5 GOTO write_graph
IF ERRORLEVEL 4 GOTO set_threshold
IF ERRORLEVEL 3 GOTO calculate_stats
IF ERRORLEVEL 2 GOTO parseCSV
IF ERRORLEVEL 1 GOTO settings

:quit
echo.
call :ColorText %col% "Press any key to exit... "
pause > nul
goto:eof

:compile
call :ColorText 0 "Ready to compile"
call :ColorText %pycol% " '!this!.py'"
echo .
call :ColorText 0 "Please ("
call :ColorText %col% "C"
call :ColorText 0 ")onfirm, ("
call :ColorText %col% "Q"
call :ColorText 0 ")uit, or choose ("
call :ColorText %col% "A"
choice /C CQA /N /M ")gain. "
IF ERRORLEVEL 3 GOTO choice
IF ERRORLEVEL 2 GOTO quit
IF ERRORLEVEL 1 call :spacer
echo.
%distro% !this!.py
call :spacer
echo.
GOTO choice

:execute
call :ColorText 0 "Ready to run"
call :ColorText %pycol% " '!this!.py'"
echo .
call :ColorText 0 "Please ("
call :ColorText %col% "C"
call :ColorText 0 ")onfirm, ("
call :ColorText %col% "Q"
call :ColorText 0 ")uit, or choose ("
call :ColorText %col% "A"
choice /C CQA /N /M ")gain. "
IF ERRORLEVEL 3 GOTO choice
IF ERRORLEVEL 2 GOTO quit
IF ERRORLEVEL 1 call :spacer
echo.
%distro% !this!.py
call :spacer
echo.
GOTO choice

:last_execute
call :ColorText 0 "Ready to run"
call :ColorText %pycol% " '!this!.py'"
echo .
call :ColorText 0 "Please ("
call :ColorText %col% "C"
call :ColorText 0 ")onfirm, ("
call :ColorText %col% "Q"
call :ColorText 0 ")uit, or choose ("
call :ColorText %col% "A"
choice /C CQA /N /M ")gain. "
IF ERRORLEVEL 3 GOTO last_choice
IF ERRORLEVEL 2 GOTO quit
IF ERRORLEVEL 1 call :spacer
echo.
%distro% !this!.py
call :spacer
echo.
GOTO last_choice

:settings
set this=settings
set next=parseCSV
GOTO compile

:parseCSV
set this=parseCSV
set next=calculate_stats
GOTO execute

:calculate_stats
set this=calculate_stats
set next=set_threshold
GOTO execute

:set_threshold
set this=set_threshold
set next=write_graph
GOTO execute

:write_graph
set this=write_graph
set next=draw_graph
GOTO execute

:draw_graph
set this=draw_graph
set next=quit
GOTO last_execute

:spacer
call :ColorText %pycol% "========================================"
goto :eof

:ColorText
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof