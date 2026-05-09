#!/bin/bash
# gastflow installer
# Installs all gastflow skills into Claude Code
# Works both locally (from cloned repo) and remotely (via curl)

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
REPO="gastonmira/gastflow"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/skills"

SKILLS=("gastflow" "gastflow-product" "gastflow-se" "gastflow-bugfix" "gastflow-qa" "gastflow-automation")

install_skill() {
  local name=$1
  local target_dir="$SKILLS_DIR/$name"
  mkdir -p "$target_dir"

  if [ -f "$REPO_DIR/skills/${name}.md" ]; then
    cp "$REPO_DIR/skills/${name}.md" "$target_dir/SKILL.md"
  else
    curl -fsSL "$BASE_URL/${name}.md" -o "$target_dir/SKILL.md"
  fi
  echo "  ✓ /$name"
}

install_template() {
  # Shared HTML design system used by every skill to render artifacts.
  # Lives next to the orchestrator skill so all sub-agents can Read it.
  local target="$SKILLS_DIR/gastflow/template.html"

  if [ -f "$REPO_DIR/skills/gastflow-html-template.html" ]; then
    cp "$REPO_DIR/skills/gastflow-html-template.html" "$target"
  else
    curl -fsSL "$BASE_URL/gastflow-html-template.html" -o "$target"
  fi
  echo "  ✓ template.html (HTML design system)"
}

echo "Installing gastflow skills..."
echo ""

for skill in "${SKILLS[@]}"; do
  install_skill "$skill"
done

install_template

echo ""
echo "All skills installed! Start a session with /gastflow in any project."
echo ""
echo "To uninstall: rm -rf ${SKILLS[*]/#/$SKILLS_DIR/}"
