#!/bin/bash

# Setup easy command aliases
# Run once: ./setup-alias.sh

echo "Setting up easy commands..."

# Get current directory
DIR="$(pwd)"

# Detect shell
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC="$HOME/.bash_profile"
fi

# Add aliases
echo "" >> "$SHELL_RC"
echo "# HomeRights AI shortcuts" >> "$SHELL_RC"
echo "alias homerights='cd $DIR && ./start.sh'" >> "$SHELL_RC"
echo "alias homerights-stop='cd $DIR && ./stop.sh'" >> "$SHELL_RC"

echo "✓ Aliases added to $SHELL_RC"
echo ""
echo "Restart your terminal or run: source $SHELL_RC"
echo ""
echo "Then you can use:"
echo "  homerights       - Start the app from anywhere"
echo "  homerights-stop  - Stop the app from anywhere"
echo ""
