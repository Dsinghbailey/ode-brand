#!/usr/bin/env bash
#
# scaffold.sh — assemble an Ode slide-deck build workspace.
#
# Usage:  ./scaffold.sh <target-dir>
#   Creates a self-contained workspace with the deck helper and a copy of the
#   brand assets (tokens, PNG logos, gradient backgrounds) pulled from the sibling
#   ode-brand skill. After scaffolding:
#     cd <target-dir> && pip install python-pptx && python build_deck.py
#
set -euo pipefail

TARGET="${1:?usage: scaffold.sh <target-dir>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # ode-slides/assets
BRAND_DIR="$(cd "$SCRIPT_DIR/../../ode-brand/assets" && pwd)" # ode-brand/assets

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

cp "$SCRIPT_DIR/ode_deck.py" "$TARGET/"
cp "$SCRIPT_DIR/lint_deck.py" "$TARGET/"
cp "$SCRIPT_DIR/review.sh" "$TARGET/"
[ -e "$TARGET/build_deck.py" ] || cp "$SCRIPT_DIR/build_example.py" "$TARGET/build_deck.py"

# Brand assets the deck reads at build time -> <workspace>/brand/
mkdir -p "$TARGET/brand/logos" "$TARGET/brand/backgrounds" "$TARGET/brand/fonts"
cp "$BRAND_DIR/tokens.json" "$TARGET/brand/"
cp "$BRAND_DIR/logos/"*.png "$TARGET/brand/logos/" 2>/dev/null || true
# Bundle the brand fonts (if present) so the user can install them for fidelity.
# ABC Diatype is commercial and NOT a Google Font, so BOTH Google Slides and
# un-provisioned PowerPoint substitute Helvetica Neue until the fonts are installed
# or embedded. See ode-brand/assets/fonts/README.md.
cp "$BRAND_DIR/fonts/"*.otf "$BRAND_DIR/fonts/"*.woff2 "$TARGET/brand/fonts/" 2>/dev/null || true
if compgen -G "$BRAND_DIR/backgrounds/*.png" > /dev/null; then
  cp "$BRAND_DIR/backgrounds/"*.png "$TARGET/brand/backgrounds/"
else
  echo "NOTE: brand gradient backgrounds not found. Cover/divider/closing slides"
  echo "      will fall back to a solid Bistre ground. To get the gradients,"
  echo "      generate them once in the ode-brand skill:"
  echo "        cd $BRAND_DIR && npm i puppeteer && node gen-backgrounds.mjs"
  echo "      then re-run this scaffold."
fi

echo "Scaffolded Ode deck workspace at: $TARGET"
echo "Next:  cd \"$TARGET\" && pip install python-pptx && python build_deck.py && bash review.sh deck.pptx"
