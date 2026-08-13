#!/bin/bash

DVDREADER="/dev/sr0"
TIMEOUT=300
TIMECHECK=2
CHECKTIMES=$(( TIMEOUT / TIMECHECK ))

eject $DVDREADER

for i in $(seq 1 $CHECKTIMES)
do
    char=$(blkid /dev/sr0 | wc -m)

    
    if [[ "$char" != "0" ]]; then
	flatpak run tv.kodi.Kodi dvd://	
	eject $DVDREADER
	
	exit 1
    fi
   

    sleep $TIMECHECK
done

exit 1


