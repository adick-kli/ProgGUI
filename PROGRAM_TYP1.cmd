@echo off
setlocal enableextensions enabledelayedexpansion
color 17



: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
: !!! Achtung!  
: !!! Hier muss der Pfad zu dem atbackend in der Atmel Studio 6.2
: !!! eingetragen sein!!!
: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:path D:\Programme\Atmel\Atmel Studio 6.2\atbackend
path C:\Program Files (x86)\Atmel\Studio\7.0\atbackend




echo.
echo.
echo Komplette Flashbereich loeschen
atprogram -t atmelice -i jtag -d at32uc3a1512 chiperase
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)

echo. 
echo Komplette User Page loeschen
atprogram -t atmelice -i jtag -d at32uc3a1512 erase -up
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)
echo.  
echo Schreibe WORD_1 in User Page
atprogram -t atmelice -i jtag -d at32uc3a1512 write -o 0x808001FC --values E11EFFD7
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)
echo.  
echo Schreibe WORD_2 in User Page
atprogram -t atmelice -i jtag -d at32uc3a1512 write -o 0x808001F8 --values 929E0977
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)
echo.  
echo Programmiere den Bootloader
avr32-objcopy -I ihex -O binary QUANTEC_XMODEM_BOOTLOADER_V1_004.hex QUANTEC_XMODEM_BOOTLOADER_V1_004.bin
:atprogram -t atmelice -i JTAG -d at32uc3a1512 program -o 0x80000000 -e --verify -f at32uc3a-isp-1.0.3.bin write -o 0xFFFE1410 -fs --values F675FFFF
atprogram -t atmelice -i jtag -d at32uc3a1512 program -o 0x80000000 -e --verify -f  QUANTEC_XMODEM_BOOTLOADER_V1_004.bin 
:write -fs -o 0xFFFE1410 -fs --values F675FFFF 
del QUANTEC_XMODEM_BOOTLOADER_V1_004.bin

echo Setze die Fuse Bits
:es ist ein Bug. Die Adresse 0xFFFE1410 soll gegen 0x0 ersetzt werden. Mit neue AS7 oder höher drauf achten
atprogram -t atmelice -i jtag -d at32uc3a1512 write -fs -o 0x0 --values F675FFFF 
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)
echo.  
echo Setze die Security Bit
:atprogram -t atmelice -i jtag -d at32uc3a1512 secure
if ERRORLEVEL 1 (
	color 47
	pause
	exit
)
echo.  
echo Wait
color 27 
pause