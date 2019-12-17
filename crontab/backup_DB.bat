@echo off
set yy=%date:~0,4%
set mm=%date:~5,2%
set dd=%date:~8,2%
set hh=%time:~0,2%
set mn=%time:~3,2%
rename C:\data\mydb mydb_backup%yy%%mm%%dd%%hh%%mn%
pause
cd C:\Program Files\MongoDB\Server\4.0\bin
mongodump -h 127.0.0.1:27017 -d mydb -o C:\data