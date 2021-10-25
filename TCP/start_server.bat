@echo off
start cmd /k "python server.py"
TIMEOUT /T 1
for /l %%x in (1, 1, 3) do (
    start cmd /k "python client.py"
)
