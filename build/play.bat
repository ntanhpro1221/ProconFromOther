@echo off

set URL=http://127.0.0.1:8080
set WORKING_PATH=%~dp0
set WORKING_PATH=%WORKING_PATH:\=/%
set INPUT_PATH=%WORKING_PATH%input.json
set OUTPUT_PATH=%WORKING_PATH%output.json
set GET_INPUT_PATH=%WORKING_PATH%get_input.py
set SUBMIT_PATH=%WORKING_PATH%submit.py
set SOLVER_PATH=%WORKING_PATH%solver_faster.exe
set TOKEN=tadz

py %GET_INPUT_PATH% %URL% %TOKEN% %INPUT_PATH%
set startTime=%time%
%SOLVER_PATH% %INPUT_PATH% %OUTPUT_PATH%
set endTime=%time%
py %SUBMIT_PATH% %URL% %TOKEN% %OUTPUT_PATH% %INPUT_PATH%

for /F "tokens=1-4 delims=:.," %%a in ("%startTime%") do (
    set /A "startMs=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)
for /F "tokens=1-4 delims=:.," %%a in ("%endTime%") do (
    set /A "endMs=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)
set /A elapsedMs=endMs-startMs
set /A elapsedSec=elapsedMs/100
set /A ms=elapsedMs %% 100
echo Elapsed time: %elapsedSec%.%ms% second
