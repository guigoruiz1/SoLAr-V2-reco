#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Get the name of the parent directory
PARENT_DIR=$(basename "$SCRIPT_DIR")

# Check if the parent directory is named "Examples"
if [ "$PARENT_DIR" == "Examples" ]; then
  # Save the current directory and change to the parent directory
  pushd "$SCRIPT_DIR/.."
fi

# Only event displays and analysis after reconstruction has been run
for folder in 202307*
do
  # Print the current file name
  echo Folder: "$folder"

  ./display_events.py "$folder" -s -n
  
  # Run the analysis script again on the output folder
  ./analysis.py "$folder"
  ./analysis.py "$folder" -p min_track_length=160
done

# If pushd was executed, return to the original directory
if [ "$PARENT_DIR" == "Examples" ]; then
  popd
fi