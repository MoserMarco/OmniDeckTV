#!/bin/bash

# Automatically detect the system DVD drive
DVDREADER=$(lsblk -dno NAME,TYPE | awk '$2=="rom" {print "/dev/"$1; exit}')

# Check if a DVD drive was found
if [ -z "$DVDREADER" ]; then
    echo "Error: No CD/DVD drive detected on the system."
    exit 1
fi

echo "Drive detected at: $DVDREADER"

TIMEOUT=300
TIMECHECK=2
CHECKTIMES=$(( TIMEOUT / TIMECHECK ))

# Open the tray
eject "$DVDREADER"

echo "Please insert the DVD..."

for i in $(seq 1 $CHECKTIMES)
do
    # Check if a valid disc is loaded and ready
    if blkid "$DVDREADER" > /dev/null 2>&1; then
        echo "DVD Detected! Launching Kodi..."

        # Launch Kodi via Flatpak
        flatpak run tv.kodi.Kodi "dvd://"

        # Eject the DVD after closing Kodi
        eject "$DVDREADER"
        exit 0
    fi

    sleep $TIMECHECK
done

echo "Timeout reached: No DVD was inserted."
exit 1