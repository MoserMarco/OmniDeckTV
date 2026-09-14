#!/bin/bash
set -e

# Check if the number of arguments ($#) is less than 2
if [ "$#" -lt 2 ]; then
  echo "Error: At least 2 parameters are required." >&2
  echo "Usage: $0 <INSTALLATION_DIRECTORY> <SECOND_PARAMETER>" >&2
  exit 1
fi


echo "=== Starting TVControlHub Setup, Target Directory: $1 ==="

PROGRAM_DIRECTORY=$1
INSTALLATION_DIRECTORY=$2


echo "--> Removing unused files from RemoteControl..."
find $PROGRAM_DIRECTORY/RemoteControl -mindepth 1 ! -name "docker-compose.yml" -delete
rm -ri $PROGRAM_DIRECTORY/Scripts/dev

echo "--> Moving $PROGRAM_DIRECTORY to $INSTALLATION_DIRECTORY..."
mkdir -p "$INSTALLATION_DIRECTORY"
mv $PROGRAM_DIRECTORY $INSTALLATION_DIRECTORY

sudo ln -sf "$INSTALLATION_DIRECTORY/Scripts/install/run_all.sh" /usr/local/bin/tvcontrolhub

