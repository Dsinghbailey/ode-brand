"""
lint_deck.py — renderer-free self-correction for Ode decks.

Checks a .pptx for the problems a visual review would catch, without needing a
renderer: shapes that fall off the 16:9 canvas, off-brand colors, and non-brand
fonts. It cannot see text that overflows its own box (that needs the LibreOffice
render in review.sh), so it reports geometry and brand conformance only — and says
so, rather than implying full visual coverage.

Usage:  python lint_deck.py [deck.pptx] [brand/tokens.json]
Exit code 0 = clean, 1 = findings. Designed to run automatically after a build.
"""
import json
import os
import sys

from pptx import Presentation
from pptx.util import Emu

TOL = Emu(int(0.02 * 914400))  # 0.02in tolerance on canvas bounds

# Fallback palette if tokens.json isn't found (matches ode-brand tokens).
FALLBACK = {
    "bistre": "#201D1C", "bone": "#FBFBF8", "bone_warm": "#F4F3EE",
    "white": "#FFFFFF", "cola": "#3C2E2A", "dove": "#625855", "slate": "#D9D9D9",
    "tomato": "#CD3E1D", "blue_gray": "#728FA8", "teal": "#5EA6B1",
    "tea": "#E8EBD7", "lilac": "#F4DCEA",
}


def load_brand(tokens_path):
    """Returns (palette, fonts, loaded_from_file)."""
    if tokens_path and os.path.exists(tokens_path):
        with open(tokens_path) as f:
            t = json.load(f)
        colors = {k: v.upper() for k, v in t["colors"].items()}
        ty = t["type"]
        # Allow every declared family (display/body/mono/secondary) so the linter
        # doesn't flag on-brand accent or mono type.
        fonts = {ty[k] for k in ("display_family", "body_family", "mono_family",
                                 "secondary_family") if ty.get(k)}
        return set(colors.values()), fonts, True
    return {v.upper() for v in FALLBACK.values()}, {"ABC Diatype"}, False


def lint(pptx_path, tokens_path):
    palette, brand_fonts, from_file = load_brand(tokens_path)
    prs = Presentation(pptx_path)
    W, H = prs.slide_width, prs.slide_height
    slides = list(prs.slides)
    errors, warnings = [], []
    if not from_file:
        warnings.append("tokens.json not found at %r; linting against the built-in "
                        "fallback palette, which may be stale." % tokens_path)

    for i, slide in enumerate(slides, 1):
        for sh in slide.shapes:
            tag = "slide %d / %s" % (i, sh.shape_type)
            # Geometry: is the shape within the canvas?
            try:
                l, t, w, h = sh.left, sh.top, sh.width, sh.height
            except Exception:
                l = t = w = h = None
            if None not in (l, t, w, h):
                if l < -TOL or t < -TOL or (l + w) > (W + TOL) or (t + h) > (H + TOL):
                    errors.append("%s: shape extends off the canvas "
                                  "(l=%.2f t=%.2f r=%.2f b=%.2f in; canvas %.2fx%.2f)" % (
                                      tag, l / 914400, t / 914400, (l + w) / 914400,
                                      (t + h) / 914400, W / 914400, H / 914400))
            # Text: brand font + palette conformance
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        name = r.font.name
                        if name and name not in brand_fonts:
                            errors.append("%s: non-brand font %r (use %s)" % (
                                tag, name, " or ".join(sorted(brand_fonts))))
                        try:
                            if r.font.color and r.font.color.type is not None:
                                hexv = "#%s" % str(r.font.color.rgb)
                                if hexv.upper() not in palette:
                                    errors.append("%s: off-palette color %s" % (tag, hexv))
                        except Exception:
                            pass
    return errors, warnings, len(slides)


def main():
    pptx_path = sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"
    tokens_path = sys.argv[2] if len(sys.argv) > 2 else "brand/tokens.json"
    if not os.path.exists(pptx_path):
        print("lint_deck: file not found: %s" % pptx_path)
        sys.exit(2)
    errors, warnings, n = lint(pptx_path, tokens_path)
    print("Linted %s — %d slides, %d findings." % (pptx_path, n, len(errors) + len(warnings)))
    for e in errors:
        print("  ERROR  %s" % e)
    for w in warnings:
        print("  WARN   %s" % w)
    if not errors and not warnings:
        print("  PASS   geometry + brand conformance OK.")
    print("  NOTE   geometry/brand only; for visual overflow run review.sh "
          "(LibreOffice render).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
