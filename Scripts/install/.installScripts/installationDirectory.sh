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

rm -rf $PROGRAM_DIRECTORY/RemoteControl/static
rm -rf $PROGRAM_DIRECTORY/RemoteControl/templates
rm -rf $PROGRAM_DIRECTORY/RemoteControl/app.py
rm -rf $PROGRAM_DIRECTORY/RemoteControl/requirements.txt
rm -rf $PROGRAM_DIRECTORY/RemoteControl/docker/docker-compose.dev.yml
rm -rf $PROGRAM_DIRECTORY/RemoteControl/docker/Dockerfile

rm -rf $PROGRAM_DIRECTORY/Scripts/dev

echo "--> Moving $PROGRAM_DIRECTORY to $INSTALLATION_DIRECTORY..."
mkdir -p "$INSTALLATION_DIRECTORY"
mv $PROGRAM_DIRECTORY $INSTALLATION_DIRECTORY



