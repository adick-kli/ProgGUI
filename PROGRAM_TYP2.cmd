@echo off
setlocal enableextensions enabledelayedexpansion

: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
: !!! Achtung!  
: !!! Hier muss der Pfad zu dem atbackend in der Atmel Studio 6.2
: !!! eingetragen sein!!!
: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:path D:\Programme\Atmel\Atmel Studio 6.2\atbackend
path C:\Program Files (x86)\Atmel\Studio\7.0\atbackend

color 17

echo.
echo.
echo Komplette Flashbereich loeschen
atprogram -t atmelice -i jtag -d at32uc3b1256 chiperase
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

echo.
echo Komplette User Page loeschen
atprogram -t atmelice -i jtag -d at32uc3b1256 erase -up
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

:echo Programming Userpage word1
:atprogram -t avrdragon -i jtag -d at32uc3b1256 write -o 0x808001FC --values E11EFFD7
:echo Programming Userpage word2
:atprogram -t avrdragon -i jtag -d at32uc3b1256 write -o 0x808001F8 --values 929E1523

echo.
echo Komplette User Page beschreiben mit USER_PAGE_HWZ.hex
:atprogram -t atmelice -i jtag -d at32uc3b1256 program -f  USER_PAGE_HWZ.hex --verify
avr32-objcopy -I ihex -O binary USER_PAGE_HWZ.hex USER_PAGE_HWZ.bin
atprogram -t atmelice -i jtag -d at32uc3b1256 program -o 0x80800000 -e --verify -f  USER_PAGE_HWZ.bin
del USER_PAGE_HWZ.bin
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

echo.
echo Programmiere den Bootloader und setze die Fuse Bits
:atprogram -t atmelice -i jtag -d at32uc3b1256 program -f  QT_HAND_BOOT.hex --verify write -fs -o 0xFFFE1410 --values F675FFFF

:**********************
:Auswahl zwischen alten und neuen Bootloader

:avr32-objcopy -I ihex -O binary QT_HAND_BOOT.hex QT_HAND_BOOT.bin
avr32-objcopy -I ihex -O binary QT_HAND_BOOT_EST01.hex QT_HAND_BOOT.bin

:*** ENDE

:es ist ein Bug. Die Adresse 0xFFFE1410 soll gegen 0x0 ersetzt werden. Mit neue AS7 oder höher drauf achten
atprogram -t atmelice -i jtag -d at32uc3b1256 program -o 0x80000000 -e --verify -f  QT_HAND_BOOT.bin write -o 0x0 -fs --values F675FFFF 
del QT_HAND_BOOT.bin
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

echo.  
echo Setze die Security Bit
atprogram -t atmelice -i jtag -d at32uc3b1256 secure
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

echo.
echo Wait
color 27 
pause