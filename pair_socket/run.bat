@echo off
REM Windows CMD version of run.sh
REM Save as run.bat in the same folder as config.txt
REM Requires Windows 10/11 (built‑in curl) or Git for Windows.

set "FILE=config.txt"
set "ENDPOINT=http://192.168.25.1:5000/guideDone"

curl -X POST -H "Content-Type: application/json" --data "@%FILE%" %ENDPOINT%

pause
