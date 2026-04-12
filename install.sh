#!/bin/bash
# gastflow installer
# Installs the gastflow skill into Claude Code

set -e

SKILLS_DIR="$HOME/.claude/skills"
SKILL_DIR="$SKILLS_DIR/gastflow"

echo "Installing gastflow..."

# Claude Code skills must be a directory containing SKILL.md
mkdir -p "$SKILL_DIR"
cp "$(dirname "$0")/skills/gastflow.md" "$SKILL_DIR/SKILL.md"

echo ""
echo "✓ gastflow installed!"
echo ""
echo "Usage: open any project in Claude Code and run /gastflow"
echo ""
echo "To uninstall: rm -rf $SKILL_DIR"
