#!/bin/bash
# gastflow installer
# Installs gastflow for Claude Code, Codex, or both.
# Works both locally (from cloned repo) and remotely (via curl).

set -e

REPO_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
REPO="gastonmira/gastflow"
BRANCH="main"
BASE_SKILLS_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/skills"
BASE_CODEX_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/codex/gastflow"

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

CLAUDE_SKILLS=("gastflow" "gastflow-product" "gastflow-se" "gastflow-bugfix" "gastflow-qa" "gastflow-automation")
CODEX_FILES=(
  "SKILL.md"
  "assets/template.html"
  "references/artifacts.md"
  "references/agents.md"
  "agents/openai.yaml"
)

TARGET="all"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--all|--claude|--codex]

  --all      Install gastflow for Claude Code and Codex (default)
  --claude   Install Claude Code skills only
  --codex    Install Codex skill only
EOF
}

case "${1:-}" in
  ""|--all)
    TARGET="all"
    ;;
  --claude)
    TARGET="claude"
    ;;
  --codex)
    TARGET="codex"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown option: $1" >&2
    usage >&2
    exit 1
    ;;
esac

install_claude_skill() {
  local name=$1
  local target_dir="$CLAUDE_SKILLS_DIR/$name"
  mkdir -p "$target_dir"

  if [ -f "$REPO_DIR/skills/${name}.md" ]; then
    cp "$REPO_DIR/skills/${name}.md" "$target_dir/SKILL.md"
  else
    curl -fsSL "$BASE_SKILLS_URL/${name}.md" -o "$target_dir/SKILL.md"
  fi
  echo "  ✓ /$name"
}

install_claude_template() {
  # Shared HTML design system used by every skill to render artifacts.
  # Lives next to the orchestrator skill so all sub-agents can Read it.
  local target="$CLAUDE_SKILLS_DIR/gastflow/template.html"

  if [ -f "$REPO_DIR/skills/gastflow-html-template.html" ]; then
    cp "$REPO_DIR/skills/gastflow-html-template.html" "$target"
  else
    curl -fsSL "$BASE_SKILLS_URL/gastflow-html-template.html" -o "$target"
  fi
  echo "  ✓ template.html (HTML design system)"
}

install_claude() {
  echo "Installing gastflow for Claude Code..."
  echo ""

  for skill in "${CLAUDE_SKILLS[@]}"; do
    install_claude_skill "$skill"
  done

  install_claude_template
}

install_codex_file() {
  local relative_path=$1
  local target="$CODEX_SKILLS_DIR/gastflow/$relative_path"
  mkdir -p "$(dirname "$target")"

  if [ -f "$REPO_DIR/codex/gastflow/$relative_path" ]; then
    cp "$REPO_DIR/codex/gastflow/$relative_path" "$target"
  else
    curl -fsSL "$BASE_CODEX_URL/$relative_path" -o "$target"
  fi
  echo "  ✓ $relative_path"
}

install_codex() {
  echo "Installing gastflow for Codex..."
  echo ""

  for file in "${CODEX_FILES[@]}"; do
    install_codex_file "$file"
  done
}

case "$TARGET" in
  all)
    install_claude
    echo ""
    install_codex
    ;;
  claude)
    install_claude
    ;;
  codex)
    install_codex
    ;;
esac

echo ""
echo "gastflow installed for $TARGET."
echo ""
echo "Claude Code usage: open any project and run /gastflow"
echo "Codex usage: ask Codex to use gastflow for your feature or bug fix"
echo ""
echo "Claude uninstall: rm -rf ${CLAUDE_SKILLS[*]/#/$CLAUDE_SKILLS_DIR/}"
echo "Codex uninstall: rm -rf $CODEX_SKILLS_DIR/gastflow"
