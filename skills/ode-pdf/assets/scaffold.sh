#!/usr/bin/env bash
#
# scaffold.sh — assemble an Ode designed-document build workspace.
#
# Usage:  ./scaffold.sh <target-dir> [doc-name]
#   <target-dir>  where the build workspace is created (created if missing)
#   [doc-name]    base name for the source HTML (default: doc) -> <doc-name>.html
#
# Pulls the render engine from this skill and the brand assets (tokens, fonts,
# logos) from the sibling ode-brand skill, so the workspace is self
# contained and on-brand. After scaffolding:
#   cd <target-dir> && npm install && node build.mjs <doc-name>.html
#
set -euo pipefail

TARGET="${1:?usage: scaffold.sh <target-dir> [doc-name]}"
DOCNAME="${2:-doc}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # ode-pdf/assets
BRAND_DIR="$(cd "$SCRIPT_DIR/../../ode-brand/assets" && pwd)" # ode-brand/assets

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

# Engine
cp "$SCRIPT_DIR/build.mjs"      "$TARGET/"
cp "$SCRIPT_DIR/watch.mjs"      "$TARGET/"
cp "$SCRIPT_DIR/paginate.js"    "$TARGET/"
cp "$SCRIPT_DIR/package.json"   "$TARGET/"
cp "$SCRIPT_DIR/components.css" "$TARGET/"

# Brand foundation (tokens.css is required; fonts/logos are guarded so a missing
# glob doesn't abort the scaffold under `set -e`).
cp "$BRAND_DIR/tokens.css" "$TARGET/"
mkdir -p "$TARGET/fonts" "$TARGET/logos"
cp "$BRAND_DIR/fonts/"*.woff2 "$BRAND_DIR/fonts/"*.otf "$TARGET/fonts/" 2>/dev/null || echo "scaffold: no fonts in $BRAND_DIR/fonts (PDF will fall back to Helvetica Neue — see ode-brand/assets/fonts/README.md)"
cp "$BRAND_DIR/logos/"*.svg "$TARGET/logos/" 2>/dev/null || echo "scaffold: no SVG logos in $BRAND_DIR/logos"

# Starter document (only if not already present — never clobber)
if [ ! -e "$TARGET/$DOCNAME.html" ]; then
  sed "s/__DOCNAME__/$DOCNAME/g" "$SCRIPT_DIR/template.html" > "$TARGET/$DOCNAME.html"
fi

# Project asset dir for diagrams/images authored per-document
mkdir -p "$TARGET/assets"

echo "Scaffolded Ode doc workspace at: $TARGET"
echo "Source: $DOCNAME.html"
echo "Next:   cd \"$TARGET\" && npm install && node build.mjs $DOCNAME.html"
