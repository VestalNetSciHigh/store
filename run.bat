@echo off
setLocal EnableDelayedExpansion

REM config
set distro=C:\Anaconda\python.exe 
set target=code
REM end config

for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)
cd code

:init
set this=init
set next=settings
echo Welcome, NetSci High Team.
echo This program provides an interface for running the multiple python scrips.
echo.
goto choice

:last_choice
echo Next in the queue is '!next!.py'.
echo Press ^C to continue or choose from the list below:
echo 1 - 'settings.py'
echo 2 - 'parseCSV.py'
echo 3 - 'calculate_stats.py'
echo 4 - 'set_threshold.py'
echo 5 - 'write_graph.py'
echo 6 - 'draw_graph.py'
echo Q - quit
echo R - Restart Batch
choice /C 123456QCR /N /M "Selection: "
echo.
IF ERRORLEVEL 9 GOTO init
IF ERRORLEVEL 8 GOTO !next!
IF ERRORLEVEL 7 GOTO quit
IF ERRORLEVEL 6 GOTO draw_graph
IF ERRORLEVEL 5 GOTO write_graph
IF ERRORLEVEL 4 GOTO set_threshold
IF ERRORLEVEL 3 GOTO calculate_stats
IF ERRORLEVEL 2 GOTO parseCSV
IF ERRORLEVEL 1 GOTO settings

:choice
echo Next in the queue is '!next!.py'.
echo Press ^C to continue or choose from the list below:
echo 1 - 'settings.py'
echo 2 - 'parseCSV.py'
echo 3 - 'calculate_stats.py'
echo 4 - 'set_threshold.py'
echo 5 - 'write_graph.py'
echo 6 - 'draw_graph.py'
echo Q - quit
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
echo Press any key to exit...
pause > nul
goto:eof

:compile
choice /C CQ /N /M "Ready to compile '!this!', please (C)onfirm or (Q)uit."
IF ERRORLEVEL 2 GOTO quit
IF ERRORLEVEL 1 %distro% !this!.py
echo.
GOTO choice

:execute
choice /C CQ /N /M "Ready to run '!this!', please (C)onfirm or (Q)uit."
IF ERRORLEVEL 2 GOTO quit
IF ERRORLEVEL 1 %distro% !this!.py
echo.
GOTO choice

:last_execute
choice /C CQ /N /M "Ready to run '!this!', please (C)onfirm or (Q)uit."
%distro% !this!.py
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
set this=set_threshold
set next=write_graph
GOTO execute

:draw_graph
set this=draw_graph
set next=quit
GOTO last_execute

:ColorText
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof