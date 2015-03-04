@echo off
REM __author__ = 'VestalNetSciHigh'
set distro=C:\Anaconda\python.exe 
set target=code

set this=init
set next=settings
:init
echo Welcome, NetSci High Team.
echo This program provides an interface for running the multiple python scrips.
echo.

:choice
echo Next in the queue is '%next%.py'.
echo Press ^C to continue or choose from the list below:
echo 1 - 'settings.py'
echo 2 - 'parseCSV.py'
echo 3 - 'calculate_stats.py'
echo 4 - 'set_threshold.py'
echo 5 - 'write_graph.py'
echo 6 - 'draw_graph.py'
echo Q - quit
echo.
choice /C 123456QC /N /M "Selection: "
echo.
IF ERRORLEVEL 1 GOTO settings
IF ERRORLEVEL 2 GOTO parseCSV
IF ERRORLEVEL 3 GOTO calculate_stats
IF ERRORLEVEL 4 GOTO set_threshold
IF ERRORLEVEL 5 GOTO write_graph
IF ERRORLEVEL 6 GOTO draw_graph
IF ERRORLEVEL 7 GOTO quit
IF ERRORLEVEL 8 GOTO %next%

:quit
echo.
echo Press any key to exit...
pause > nul
goto:eof

:change_dest

set next=parseCSV
GOTO choice

:compile
echo Ready to compile '%this%'
pause
%distro% %target%\%this%.py
echo.
GOTO choice

:execute
chioce /C CQ /N /M "Ready to run '%this%', please (C)onfirm or (Q)uit."
%distro% %target%\%this%.py
echo.
GOTO choice

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
GOTO execute