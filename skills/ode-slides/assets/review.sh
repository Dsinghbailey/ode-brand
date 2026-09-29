#!/usr/bin/env bash
#
# review.sh — self-correction loop for an Ode deck.
#
# Usage:  bash review.sh [deck.pptx]
#
# 1. Runs the renderer-free linter (geometry + brand conformance) — always.
# 2. Tries to render the deck to per-slide PNGs so the agent can LOOK at every
#    slide, using whatever renderer is on the machine, in this order:
#       LibreOffice (headless) -> Keynote (osascript) -> PowerPoint (osascript)
#    On a typical Mac, Keynote is preinstalled, so the visual loop works with no
#    install. If none is available, it falls back to LINT-ONLY and says so loudly.
#
# The closing banner states which level of review happened so the caller knows
# whether the slides were actually seen or only structurally checked.
#
set -uo pipefail

DECK="${1:-deck.pptx}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -e "$DECK" ]; then echo "review: $DECK not found"; exit 2; fi

echo "== Lint (always) =="
python3 "$HERE/lint_deck.py" "$DECK" "brand/tokens.json"
LINT=$?

echo
echo "== Visual render =="
mkdir -p review
BASE="$(basename "${DECK%.pptx}")"
ABS_PPTX="$(cd "$(dirname "$DECK")" && pwd)/$(basename "$DECK")"
PDF_DIR="$(cd review && pwd)"
PDF="$PDF_DIR/$BASE.pdf"
rm -f "$PDF"
RENDERER=""

# 1) LibreOffice (headless)
SOFFICE=""
for c in soffice libreoffice "/Applications/LibreOffice.app/Contents/MacOS/soffice"; do
  if command -v "$c" >/dev/null 2>&1; then SOFFICE="$c"; break; fi
done
if [ -n "$SOFFICE" ]; then
  "$SOFFICE" --headless --convert-to pdf --outdir "$PDF_DIR" "$ABS_PPTX" >/dev/null 2>&1 || true
  [ -e "$PDF" ] && RENDERER="LibreOffice"
fi

# 2) Keynote (osascript export). Free/preinstalled on most Macs.
if [ -z "$RENDERER" ] && [ -d "/Applications/Keynote.app" ]; then
  osascript - "$ABS_PPTX" "$PDF" >/dev/null 2>&1 <<'OSA' || true
on run argv
  tell application "Keynote"
    set theDoc to open (POSIX file (item 1 of argv))
    export theDoc to (POSIX file (item 2 of argv)) as PDF
    close theDoc saving no
  end tell
end run
OSA
  [ -e "$PDF" ] && RENDERER="Keynote"
fi

# 3) Microsoft PowerPoint (osascript export).
if [ -z "$RENDERER" ] && [ -d "/Applications/Microsoft PowerPoint.app" ]; then
  osascript - "$ABS_PPTX" "$PDF" >/dev/null 2>&1 <<'OSA' || true
on run argv
  tell application "Microsoft PowerPoint"
    set theDoc to open (item 1 of argv)
    save theDoc in (item 2 of argv) as save as PDF
    close theDoc saving no
  end tell
end run
OSA
  [ -e "$PDF" ] && RENDERER="PowerPoint"
fi

echo
SLIDES=0
if [ -n "$RENDERER" ] && [ -e "$PDF" ] && command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 110 "$PDF" "$PDF_DIR/slide" >/dev/null 2>&1
  SLIDES=$(ls "$PDF_DIR"/slide-*.png 2>/dev/null | wc -l | tr -d ' ')
fi

echo "============================================================"
if [ "$SLIDES" -gt 0 ]; then
  echo "REVIEW LEVEL: VISUAL  (rendered via $RENDERER)"
  echo "Rendered $SLIDES slide image(s) to review/slide-*.png — open and look at"
  echo "every one (overflow, contrast on gradients, wrapping). Note: a local"
  echo "renderer substitutes fonts, so type is approximate; layout is accurate."
else
  echo "REVIEW LEVEL: LINT-ONLY  (no slide renderer found)"
  echo "Structural checks (geometry + brand) ran, but the slides were NOT seen."
  echo "Install a renderer for the full visual loop:"
  echo "    brew install --cask libreoffice      # macOS"
  echo "  (Keynote or Microsoft PowerPoint are used automatically if installed.)"
  echo "Or open $DECK in PowerPoint / Google Slides and review by eye."
fi
[ "$LINT" -ne 0 ] && echo "Lint reported findings above — fix them before shipping."
echo "============================================================"
exit 0
