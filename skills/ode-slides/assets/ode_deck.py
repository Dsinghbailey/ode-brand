"""
ode_deck.py — build on-brand Ode with Anthropic slide decks (.pptx).

A thin, brand-aware wrapper over python-pptx. Produces 16:9 .pptx files that open
in both PowerPoint and Google Slides. Color and type come from the Ode
brand tokens (tokens.json); full-bleed gradient covers/dividers use the brand
background PNGs when present, falling back to a solid Bistre ground.

Usage:
    from ode_deck import Deck
    d = Deck(brand_dir="brand")            # folder with tokens.json, logos/, backgrounds/
    d.add_cover("Title", subtitle="...", eyebrow="Prepared for X", date="June 2026")
    d.add_section("01", "First Section", synopsis="What this section argues.")
    d.add_cards("Three levers", eyebrow="Where value comes from", cards=[
        {"num": "EUR 200M", "title": "New sectors", "body": "..."},
        {"num": "EUR 100M", "title": "Financing", "body": "..."},
        {"num": "EUR 50M", "title": "Data", "body": "..."}])
    d.add_bars("Value breakdown", items=[("New sectors", 200, "EUR 200M"),
                                         ("Financing", 100, "EUR 100M")])
    d.add_roadmap("How we deliver", phases=[
        {"name": "Discover", "when": "Weeks 1-4", "body": "..."},
        {"name": "Build", "when": "Months 2-6", "body": "..."}])
    d.add_stats([("40%", "A metric"), ("3x", "A multiplier"), ("12", "A count")])
    d.add_statement("The one thing this deck exists to say.", label="Central thesis")
    d.add_closing("Thank you.", subtitle="yourdomain.com")
    d.save("deck.pptx")

Prefer the visual slide types (add_cards / add_bars / add_roadmap / add_stats) over
plain bullet lists; add_content is the text fallback.

Fonts: the deck sets font names (ABC Diatype / ABC Diatype). For exact rendering, install
those fonts on the machine that opens the file, or embed them via PowerPoint
(File > Options > Save > Embed fonts). Otherwise the app substitutes a sans-serif.
"""

import json
import math
import os

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# 16:9 canvas
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def _hex(s):
    return RGBColor.from_string(s.lstrip("#"))


class Deck:
    def __init__(self, brand_dir="brand", tokens=None):
        """brand_dir: folder containing tokens.json, logos/, backgrounds/.
        Pass tokens=dict to override loading from disk."""
        self.brand_dir = brand_dir
        if tokens is None:
            with open(os.path.join(brand_dir, "tokens.json")) as f:
                tokens = json.load(f)
        c = tokens["colors"]
        self.BISTRE = _hex(c["bistre"])
        self.BONE = _hex(c["bone_warm"])
        self.WHITE = _hex(c["white"])
        self.TOMATO = _hex(c["tomato"])
        self.BLUEGRAY = _hex(c["blue_gray"])
        self.TEAL = _hex(c["teal"])
        self.DISPLAY = tokens["type"]["display_family"]   # ABC Diatype
        self.BODY = tokens["type"]["body_family"]          # ABC Diatype
        # Hairline/border color for panels and cards. This is a LINE color only
        # (never used for text), so it sits outside the brand text palette by
        # design; the linter checks run colors, not shape borders.
        self.RULE = RGBColor.from_string("D9D9D9")
        # Colors and font families come from tokens; the point sizes and tracking
        # in the slide methods below are a deliberate pptx/slide scale, not
        # tokens.json's scale_marketing (which is sized for marketing layouts).

        self.prs = Presentation()
        self.prs.slide_width = SLIDE_W
        self.prs.slide_height = SLIDE_H
        self._blank = self.prs.slide_layouts[6]  # truly blank layout

    # -- low-level helpers ------------------------------------------------

    def _slide(self):
        return self.prs.slides.add_slide(self._blank)

    def _bg_solid(self, slide, color):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def _bg_image(self, slide, name, fallback):
        """Full-bleed background PNG from brand_dir/backgrounds/<name>.png, or a
        solid fallback color if the image is missing."""
        path = os.path.join(self.brand_dir, "backgrounds", name + ".png")
        if os.path.exists(path):
            slide.shapes.add_picture(path, 0, 0, width=SLIDE_W, height=SLIDE_H)
        else:
            self._bg_solid(slide, fallback)

    def _logo(self, slide, variant, left, top, height):
        path = os.path.join(self.brand_dir, "logos", "logo-%s.png" % variant)
        if os.path.exists(path):
            slide.shapes.add_picture(path, left, top, height=height)

    def _text(self, slide, left, top, width, height, runs,
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
        """runs: list of paragraphs; each paragraph is a list of (text, opts) runs.
        opts keys: font, size, color, bold, italic, caps, tracking, space_after,
        line_spacing."""
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        for i, para in enumerate(runs):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            first_opts = para[0][1] if para else {}
            if "space_after" in first_opts:
                p.space_after = Pt(first_opts["space_after"])
            p.line_spacing = first_opts.get("line_spacing", 1.05)
            for text, opts in para:
                r = p.add_run()
                r.text = text.upper() if opts.get("caps") else text
                f = r.font
                f.name = opts.get("font", self.BODY)
                f.size = Pt(opts.get("size", 16))
                f.bold = opts.get("bold", False)
                f.italic = opts.get("italic", False)
                f.color.rgb = opts.get("color", self.BISTRE)
                if opts.get("caps"):
                    self._set_tracking(r, opts.get("tracking", 200))
        return box

    def _set_tracking(self, run, hundredths_pt):
        """Letter-spacing in 1/100 pt (python-pptx has no API; set via XML)."""
        rPr = run._r.get_or_add_rPr()
        rPr.set("spc", str(int(hundredths_pt)))

    def _rule(self, slide, left, top, width, color, weight=Pt(1)):
        ln = slide.shapes.add_connector(1, left, top, left + width, top)
        ln.line.color.rgb = color
        ln.line.width = weight
        return ln

    def _accent_bar(self, slide, left, top, width, color, height=Pt(3)):
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        return bar

    def _panel(self, slide, left, top, width, height, fill, line=None, radius=True):
        """A filled rectangle/rounded-rectangle with no drop shadow. radius:
        False = square; True = subtle (0.045); a float = that corner fraction
        (0.5 = pill)."""
        shp = MSO_SHAPE.RECTANGLE if radius is False else MSO_SHAPE.ROUNDED_RECTANGLE
        p = slide.shapes.add_shape(shp, int(left), int(top), int(width), int(height))
        if radius is True:
            try:
                p.adjustments[0] = 0.045
            except Exception:
                pass
        elif radius is not False:
            try:
                p.adjustments[0] = float(radius)
            except Exception:
                pass
        p.fill.solid()
        p.fill.fore_color.rgb = fill
        if line is None:
            p.line.fill.background()
        else:
            p.line.color.rgb = line
            p.line.width = Pt(0.75)
        p.shadow.inherit = False
        return p

    def _content_header(self, slide, title, eyebrow=None):
        """Bone ground + optional tomato eyebrow + title. Returns the y (Emu) where
        the slide body should start."""
        self._bg_solid(slide, self.BONE)
        if eyebrow:
            self._accent_bar(slide, Inches(0.7), Inches(0.78), Inches(0.22), self.TOMATO, Pt(2))
            self._text(slide, Inches(1.05), Inches(0.6), Inches(11), Inches(0.4),
                       [[(eyebrow, {"font": self.DISPLAY, "size": 11, "color": self.TOMATO,
                        "caps": True, "tracking": 300, "bold": True})]])
            ttop = Inches(1.02)
        else:
            ttop = Inches(0.7)
        self._text(slide, Inches(0.7), ttop, Inches(11.93), Inches(1.0),
                   [[(title, {"font": self.DISPLAY, "size": 30, "color": self.BISTRE,
                    "line_spacing": 1.0})]])
        return Inches(2.25) if eyebrow else Inches(1.95)

    # -- slide types ------------------------------------------------------

    def add_cover(self, title, subtitle=None, eyebrow=None, date=None):
        s = self._slide()
        self._bg_image(s, "cover", self.BISTRE)
        self._logo(s, "light", Inches(0.7), Inches(0.6), Inches(0.34))
        body = []
        if eyebrow:
            body.append([(eyebrow, {"font": self.DISPLAY, "size": 12, "color": self.WHITE,
                                    "caps": True, "tracking": 320, "bold": True,
                                    "space_after": 14})])
        body.append([(title, {"font": self.DISPLAY, "size": 54, "color": self.WHITE,
                              "bold": False, "line_spacing": 1.0, "space_after": 10})])
        if subtitle:
            body.append([(subtitle, {"font": self.DISPLAY, "size": 20, "color": self.WHITE,
                                     "line_spacing": 1.2})])
        self._text(s, Inches(0.7), Inches(2.4), Inches(11.0), Inches(3.5), body,
                   anchor=MSO_ANCHOR.TOP)
        meta = []
        meta.append([("Prepared by  Ode with Anthropic", {"font": self.DISPLAY, "size": 11,
                     "color": self.WHITE})])
        if date:
            meta.append([(date, {"font": self.DISPLAY, "size": 11, "color": self.WHITE})])
        self._text(s, Inches(0.7), Inches(6.5), Inches(11.0), Inches(0.7), meta)
        return s

    def add_section(self, number, title, synopsis=None):
        s = self._slide()
        self._bg_image(s, "divider", self.BISTRE)
        self._logo(s, "light", Inches(0.7), Inches(0.6), Inches(0.30))
        self._text(s, Inches(0.7), Inches(1.3), Inches(6),
                   Inches(0.5), [[("Section %s" % number,
                   {"font": self.DISPLAY, "size": 12, "color": self.WHITE, "caps": True,
                    "tracking": 320, "bold": True})]])
        # ghost numeral, large and faint
        self._text(s, Inches(8.6), Inches(0.6), Inches(4.5), Inches(6),
                   [[(str(number), {"font": self.DISPLAY, "size": 300, "color": self.BLUEGRAY,
                     "bold": False})]], align=PP_ALIGN.RIGHT)
        body = [[(title, {"font": self.DISPLAY, "size": 48, "color": self.WHITE,
                          "line_spacing": 1.0, "space_after": 12})]]
        if synopsis:
            body.append([(synopsis, {"font": self.BODY, "size": 16, "color": self.WHITE,
                          "line_spacing": 1.35})])
        self._text(s, Inches(0.7), Inches(4.6), Inches(9.0), Inches(2.2), body)
        return s

    def add_content(self, title, bullets=None, eyebrow=None, body=None):
        """Light content slide: optional lead paragraph + a readable bullet list
        (square markers, generous spacing, measure capped for readability). For
        anything that wants visual structure, prefer add_cards / add_bars."""
        s = self._slide()
        y = self._content_header(s, title, eyebrow)
        if body:
            self._text(s, Inches(0.7), y, Inches(10.8), Inches(1.1),
                       [[(body, {"font": self.BODY, "size": 15.5, "color": self.BISTRE,
                        "line_spacing": 1.4})]])
            y = y + Inches(1.05)
        if bullets:
            paras = []
            for b in bullets:
                # Paragraph spacing/leading is read from the first run's opts, so
                # the marker run carries space_after/line_spacing for the row.
                paras.append([("▪  ", {"font": self.DISPLAY, "size": 12, "color": self.TOMATO,
                               "bold": True, "space_after": 11, "line_spacing": 1.3}),
                              (b, {"font": self.BODY, "size": 14.5, "color": self.BISTRE})])
            box_top = y + Inches(0.1)
            box_h = max(int(Inches(1.0)), int(Inches(6.95) - box_top))
            self._text(s, Inches(0.7), box_top, Inches(10.6), box_h, paras)
        return s

    def add_cards(self, title, cards, eyebrow=None):
        """A grid of accent-topped cards — the scannable, visual alternative to a
        bullet list. cards: list of dicts with optional 'num' and 'title'/'body'.
        Lays out 1 row for <=3, 2x2 for 4, three columns for 5-6."""
        s = self._slide()
        y0 = self._content_header(s, title, eyebrow)
        n = len(cards)
        cols = n if n <= 3 else (2 if n == 4 else 3)
        rows = math.ceil(n / cols)
        gut = Inches(0.28)
        cw = int((Inches(11.93) - gut * (cols - 1)) / cols)
        bottom = Inches(6.95)
        ch = int((bottom - y0 - gut * (rows - 1)) / rows)
        accents = [self.TOMATO, self.BLUEGRAY, self.TEAL]
        pad = Inches(0.26)
        for i, c in enumerate(cards):
            r, col = divmod(i, cols)
            left = int(Inches(0.7) + (cw + gut) * col)
            top = int(y0 + (ch + gut) * r)
            accent = accents[i % 3]
            self._panel(s, left, top, cw, ch, self.WHITE, line=self.RULE)
            self._panel(s, left, top, cw, Pt(3.5), accent, radius=False)
            runs = []
            if c.get("num"):
                runs.append([(c["num"], {"font": self.DISPLAY, "size": 26, "color": accent,
                             "space_after": 5})])
            runs.append([(c["title"], {"font": self.DISPLAY, "size": 14.5, "color": self.BISTRE,
                         "bold": True, "space_after": 6, "line_spacing": 1.05})])
            if c.get("body"):
                runs.append([(c["body"], {"font": self.BODY, "size": 11, "color": self.BISTRE,
                             "line_spacing": 1.3})])
            self._text(s, left + pad, top + Inches(0.24), cw - 2 * pad, ch - Inches(0.42), runs)
        return s

    def add_bars(self, title, items, eyebrow=None, note=None):
        """Horizontal bar chart, bars scaled to the largest value. Ideal for a
        value/EV breakdown. items: list of (label, number, value_text), e.g.
        ("New sectors", 200, "EUR 200M"). Pass them pre-sorted if you want a ranking."""
        s = self._slide()
        y0 = self._content_header(s, title, eyebrow)
        maxv = max((v for _, v, _ in items), default=1) or 1
        label_w = Inches(3.4)
        bar_x = int(Inches(0.7) + label_w + Inches(0.2))
        value_w = Inches(1.5)
        bar_max = int(Inches(12.633) - bar_x - value_w)
        n = len(items)
        slot = int((Inches(6.75) - y0) / n)
        bar_h = min(int(Inches(0.44)), slot - int(Inches(0.2)))
        accents = [self.TOMATO, self.BLUEGRAY, self.TEAL]
        for i, (label, v, vtext) in enumerate(items):
            rowtop = int(y0 + slot * i)
            cy = rowtop + int((slot - bar_h) / 2)
            self._text(s, Inches(0.7), rowtop, label_w, slot,
                       [[(label, {"font": self.DISPLAY, "size": 13.5, "color": self.BISTRE})]],
                       anchor=MSO_ANCHOR.MIDDLE)
            w = max(int(Inches(0.12)), int(bar_max * (float(v) / maxv)))
            self._panel(s, bar_x, cy, w, bar_h, accents[i % 3], radius=0.5)
            self._text(s, bar_x + w + Inches(0.14), rowtop, value_w, slot,
                       [[(vtext, {"font": self.DISPLAY, "size": 15, "color": self.BISTRE,
                         "bold": True})]], anchor=MSO_ANCHOR.MIDDLE)
        if note:
            self._text(s, Inches(0.7), Inches(6.95), Inches(11.93), Inches(0.4),
                       [[(note, {"font": self.BODY, "size": 10.5, "color": self.BISTRE})]])
        return s

    def add_roadmap(self, title, phases, eyebrow=None):
        """Horizontal phased timeline: a track with nodes and a column per phase.
        phases: list of dicts {'name','when','body'}. Best with 3-5 phases; keep
        names to one or two words."""
        s = self._slide()
        y0 = self._content_header(s, title, eyebrow)
        n = len(phases)
        x0 = Inches(0.7)
        x1 = Inches(12.633)
        track_y = int(y0 + Inches(0.5))
        self._panel(s, x0, track_y, int(x1 - x0), Pt(2), self.BLUEGRAY, radius=False)
        colw = int((x1 - x0) / n)
        for i, p in enumerate(phases):
            colx = int(x0 + colw * i)
            cx = colx + int(colw / 2)
            node = s.shapes.add_shape(MSO_SHAPE.OVAL, int(cx - Inches(0.09)),
                                      int(track_y - Inches(0.07)), Inches(0.18), Inches(0.18))
            node.fill.solid()
            node.fill.fore_color.rgb = self.WHITE
            node.line.color.rgb = self.BLUEGRAY
            node.line.width = Pt(1.75)
            node.shadow.inherit = False
            runs = [
                [("PHASE %02d" % (i + 1), {"font": self.DISPLAY, "size": 8.5,
                  "color": self.BISTRE, "caps": True, "tracking": 160, "space_after": 4})],
                [(p["name"], {"font": self.DISPLAY, "size": 17, "color": self.BISTRE,
                  "bold": True, "space_after": 3})],
                [(p["when"], {"font": self.DISPLAY, "size": 9.5, "color": self.TOMATO,
                  "caps": True, "tracking": 130, "space_after": 9})],
                [(p["body"], {"font": self.BODY, "size": 10.5, "color": self.BISTRE,
                  "line_spacing": 1.3})],
            ]
            self._text(s, colx + Inches(0.08), track_y + Inches(0.32), colw - Inches(0.3),
                       Inches(3.6), runs)
        return s

    def add_stats(self, stats, title=None, eyebrow=None):
        """stats: list of (value, label) tuples, up to 4."""
        s = self._slide()
        self._bg_solid(s, self.BONE)
        if title:
            self._text(s, Inches(0.7), Inches(0.7), Inches(11.9), Inches(1),
                       [[(title, {"font": self.DISPLAY, "size": 30, "color": self.BISTRE})]])
        n = max(1, min(len(stats), 4))
        colw = Inches(12.0 / n)
        self._rule(s, Inches(0.7), Inches(3.0), Inches(12.0), self.BISTRE, Pt(1.5))
        self._rule(s, Inches(0.7), Inches(5.2), Inches(12.0), self.BISTRE, Pt(1.5))
        for i, (value, label) in enumerate(stats[:4]):
            left = Inches(0.7) + colw * i
            self._text(s, left + Inches(0.1), Inches(3.25), colw, Inches(1.3),
                       [[(value, {"font": self.DISPLAY, "size": 56, "color": self.BISTRE})]])
            self._text(s, left + Inches(0.1), Inches(4.55), colw, Inches(0.6),
                       [[(label, {"font": self.DISPLAY, "size": 11, "color": self.TOMATO,
                        "caps": True, "tracking": 180, "bold": True})]])
        return s

    def add_two_column(self, title, left_title, left_body, right_title, right_body):
        s = self._slide()
        self._bg_solid(s, self.BONE)
        self._text(s, Inches(0.7), Inches(0.7), Inches(11.9), Inches(1),
                   [[(title, {"font": self.DISPLAY, "size": 30, "color": self.BISTRE})]])
        for i, (ct, cb, color) in enumerate([
                (left_title, left_body, self.TOMATO), (right_title, right_body, self.TEAL)]):
            left = Inches(0.7) + Inches(6.1) * i
            self._accent_bar(s, left, Inches(2.3), Inches(5.4), color, Pt(2))
            self._text(s, left, Inches(2.5), Inches(5.4), Inches(0.7),
                       [[(ct, {"font": self.DISPLAY, "size": 18, "color": self.BISTRE, "bold": True})]])
            self._text(s, left, Inches(3.2), Inches(5.4), Inches(3.5),
                       [[(cb, {"font": self.BODY, "size": 15, "color": self.BISTRE, "line_spacing": 1.4})]])
        return s

    def add_statement(self, text, label=None):
        s = self._slide()
        self._bg_solid(s, self.BONE)
        self._rule(s, Inches(0.7), Inches(2.3), Inches(12.0), self.BISTRE, Pt(1.5))
        self._rule(s, Inches(0.7), Inches(5.2), Inches(12.0), self.BISTRE, Pt(1.5))
        body = []
        if label:
            body.append([(label, {"font": self.DISPLAY, "size": 12, "color": self.TOMATO,
                          "caps": True, "tracking": 260, "bold": True, "space_after": 16})])
        body.append([(text, {"font": self.DISPLAY, "size": 30, "color": self.BISTRE,
                      "line_spacing": 1.2})])
        self._text(s, Inches(0.7), Inches(2.6), Inches(11.9), Inches(2.5), body,
                   anchor=MSO_ANCHOR.MIDDLE)
        return s

    def add_closing(self, title, subtitle=None):
        s = self._slide()
        self._bg_image(s, "brand", self.BISTRE)
        self._logo(s, "light", Inches(0.7), Inches(0.6), Inches(0.34))
        body = [[(title, {"font": self.DISPLAY, "size": 48, "color": self.WHITE,
                          "space_after": 10})]]
        if subtitle:
            body.append([(subtitle, {"font": self.BODY, "size": 16, "color": self.WHITE,
                          "line_spacing": 1.35})])
        self._text(s, Inches(0.7), Inches(4.6), Inches(10), Inches(2), body)
        return s

    def save(self, path):
        self.prs.save(path)
        self._retheme_fonts(path)
        return path

    def _retheme_fonts(self, path):
        """Set the deck theme's major/minor Latin font to the brand family.

        python-pptx builds every deck on Office's default theme, whose minor/major
        font is Calibri. Our own runs set the font explicitly, but any text a user
        later TYPES into the template inherits the theme font. Rewriting the theme
        to ABC Diatype makes the whole template on-brand for editing, so nothing
        falls back to Calibri. (Rendering the real face still requires the font to
        be installed/embedded per the opener — see the SKILL "Fonts and fidelity".)
        """
        import re
        import shutil
        import zipfile

        theme = "ppt/theme/theme1.xml"
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if theme not in names:
                return
            blobs = {n: z.read(n) for n in names}
        xml = blobs[theme].decode("utf-8")
        xml = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*',
                     lambda m: m.group(1) + self.DISPLAY, xml, count=1)
        xml = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*',
                     lambda m: m.group(1) + self.BODY, xml, count=1)
        blobs[theme] = xml.encode("utf-8")
        tmp = path + ".tmp"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for n in names:
                z.writestr(n, blobs[n])
        shutil.move(tmp, path)
