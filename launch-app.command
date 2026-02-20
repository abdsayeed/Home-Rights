#!/bin/bash

# HomeRights AI - Double-click launcher for macOS
# This file can be double-clicked from Finder

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Run the start script
./start.sh

# Keep terminal open
echo ""
echo "Press any key to close this window..."
read -n 1
