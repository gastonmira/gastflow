#!/bin/bash
# gastflow installer
# Installs all gastflow skills into Claude Code

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(dirname "$0")"

install_skill() {
  local name=$1
  local source_file="$REPO_DIR/skills/${name}.md"
  local target_dir="$SKILLS_DIR/$name"

  mkdir -p "$target_dir"
  cp "$source_file" "$target_dir/SKILL.md"
  echo "  ✓ /$name"
}

echo "Installing gastflow skills..."
echo ""

install_skill "gastflow"
install_skill "gastflow-se"
install_skill "gastflow-qa"
install_skill "gastflow-automation"

echo ""
echo "All skills installed! Start a session with /gastflow in any project."
echo ""
echo "To uninstall: rm -rf $SKILLS_DIR/gastflow $SKILLS_DIR/gastflow-se $SKILLS_DIR/gastflow-qa $SKILLS_DIR/gastflow-automation"
