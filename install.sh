#!/bin/bash
# gastflow installer
# Installs the gastflow skill into Claude Code

set -e

SKILLS_DIR="$HOME/.claude/skills"
SKILL_FILE="$SKILLS_DIR/gastflow"

echo "Installing gastflow..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Copy skill file (no .md extension — Claude Code requires this)
cp "$(dirname "$0")/skills/gastflow.md" "$SKILL_FILE"

echo ""
echo "✓ gastflow installed!"
echo ""
echo "Usage: open any project in Claude Code and run /gastflow"
echo ""
echo "To uninstall: rm $SKILL_FILE"
