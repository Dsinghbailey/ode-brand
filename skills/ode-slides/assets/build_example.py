"""
build_deck.py — author an Ode slide deck.

Edit this file to build your deck, then run:  python build_deck.py
Outputs deck.pptx (opens in PowerPoint and Google Slides). See ode_deck.py
and reference/deck-api.md for every slide type.

Design note: reach for a VISUAL slide (add_cards / add_bars / add_roadmap /
add_stats) before a plain add_content bullet list — a wall of bullets is the most
common reason a deck reads as flat. One idea per slide; let slides breathe.
"""
from ode_deck import Deck

d = Deck(brand_dir="brand")

d.add_cover(
    "Deck Title Here",
    subtitle="A one-line subtitle that frames what this deck is, in plain language.",
    eyebrow="Prepared for [Client]",
    date="Month YYYY",
)

d.add_stats(
    [("200+", "A count"), ("35,000", "Another"), ("$1.5B", "A total"), ("9", "A number")],
    title="The scale in four numbers",
)

d.add_statement(
    "The one statement this deck exists to make.",
    label="Central thesis",
)

# A value breakdown reads far better as bars than as a list of numbers.
d.add_bars(
    "Where the value comes from",
    eyebrow="The opportunity",
    items=[("First lever", 200, "$200M"),
           ("Second lever", 100, "$100M"),
           ("Third lever", 50, "$50M"),
           ("Fourth lever", 40, "$40M")],
    note="Optional caption explaining the figures.",
)

# A set of points reads better as cards than as bullets.
d.add_cards(
    "The levers, side by side",
    eyebrow="What we'd build",
    cards=[
        {"num": "$200M", "title": "First lever", "body": "A short, concrete description that stands on its own."},
        {"num": "$100M", "title": "Second lever", "body": "A short, concrete description that stands on its own."},
        {"num": "$50M", "title": "Third lever", "body": "A short, concrete description that stands on its own."},
        {"num": "$40M", "title": "Fourth lever", "body": "A short, concrete description that stands on its own."},
    ],
)

d.add_roadmap(
    "How we deliver",
    eyebrow="Phased, embedded",
    phases=[
        {"name": "Discover", "when": "Weeks 1-4", "body": "Map the work and pick the first slice."},
        {"name": "Build", "when": "Months 2-6", "body": "Ship the priority workstreams."},
        {"name": "Scale", "when": "Months 6+", "body": "Extend across the rest."},
    ],
)

d.add_closing("Thank you.", subtitle="yourdomain.com")

out = d.save("deck.pptx")
print("Wrote", out)
print("Next: bash review.sh deck.pptx   (lints, and renders to PNGs if LibreOffice is installed)")
print("Fonts: the deck (incl. its theme) is set to ABC Diatype. ABC Diatype is a "
      "commercial font, NOT a Google Font, so the real face shows in PowerPoint / "
      "Keynote once the bundled brand/fonts/ABCDiatype-Regular.otf is installed "
      "(open the .otf). Google Slides substitutes it (platform limitation — it "
      "only renders Google Fonts). For guaranteed ABC Diatype fidelity, use ode-pdf.")
