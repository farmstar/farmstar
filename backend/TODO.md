Complete overhaul of the setup
Save config values into seperate .py files with dictionaries
(GPGGA.py, Bent0P.py, JohnDeerModelxxx.py, GPRMC.py, etc.)
Or just .db..?... yes

Data -> Dictionary -> Database  -> httpserver

Incorporate scan serial into new setup

Setup:

1 - Understand system invironment (linux, windows)
2 - Check network connectivity (internet / NTP ...)
2 - scan for gps comport
3 - Get GPS time
4 - sync time with NTP else GPS
5 - continue setup

Main:
1 - Run self checks
2 - Run GPS parsing and display (curses)
3 - Log to .db

