@echo off
start cmd /K python start.py --frontend n
timeout 2>nul
exit