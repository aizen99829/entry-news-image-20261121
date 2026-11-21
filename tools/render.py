"""Render the Daily Compass front page for Saturday 21 November 2026.

A dense newspaper poster drawn entirely with Pillow primitives:
masthead, three lead panels, ten smaller illustrated panels, a
schematic world map with numbered pins, and a text index covering
the remaining stories of the day. Output is deterministic: the same
code always produces byte-identical PNG bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 241, 227)
INK = (24, 22, 18)
MUTED = (92, 84, 70)
RULE = (24, 22, 18)
PANEL_BG = (255, 253, 246)
PANEL_EDGE = (58, 52, 40)
BADGE_BG = (164, 32, 28)
BADGE_FG = (255, 255, 255)
ACCENT_BLUE = (38, 84, 140)
ACCENT_GREEN = (38, 110, 72)
ACCENT_GOLD = (176, 128, 24)
ACCENT_RED = (178, 44, 36)
SEA = (196, 216, 228)
LAND = (168, 188, 148)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "assets" / "poster.png"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(draw, trial, fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_width, line_gap,
                 max_lines=None):
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    ascent, descent = fnt.getmetrics()
    step = ascent + descent + line_gap
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def draw_badge(draw, x, y, number):
    r = 11
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=BADGE_BG)
    label = str(number)
    fnt = font(SANS_BOLD, 12 if number < 10 else 10)
    w = text_width(draw, label, fnt)
    draw.text((x + r - w / 2, y + r - 7), label, font=fnt, fill=BADGE_FG)


def panel_frame(draw, box):
    draw.rectangle(box, fill=PANEL_BG, outline=PANEL_EDGE, width=2)


def illo_missiles(draw, box):
    """Night sky over south-east Poland: two missile trails arc across,
    a red-and-white flag flies below."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 22, 44))
    for sx, sy in ((x0 + 20, y0 + 12), (x0 + 60, y0 + 6), (x0 + 110, y0 + 16),
                   (x0 + 150, y0 + 8), (x0 + 200, y0 + 14), (x0 + 260, y0 + 10)):
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(250, 250, 240))
    # Dark treeline at the bottom (drawn first so the trails pass over it).
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(10, 14, 26))
    for tx in range(x0 + 6, x1 - 6, 18):
        draw.polygon([(tx, y1 - 16), (tx + 7, y1 - 34), (tx + 14, y1 - 16)],
                     fill=(10, 14, 26))
    # Two diagonal missile trails with bright heads, kept inside the box.
    draw.line([x0 + 8, y0 + 12, x0 + 190, y0 + 44], fill=(250, 180, 60),
              width=4)
    draw.ellipse([x0 + 184, y0 + 38, x0 + 194, y0 + 48], fill=(255, 220, 120))
    draw.line([x0 + 60, y0 + 6, x0 + 260, y0 + 58], fill=(250, 120, 80),
              width=3)
    draw.ellipse([x0 + 254, y0 + 52, x0 + 262, y0 + 60], fill=(255, 200, 100))
    # A small Polish flag on a pole.
    draw.line([x0 + 24, y1 - 34, x0 + 24, y1 - 16], fill=(230, 230, 220),
              width=2)
    draw.rectangle([x0 + 24, y1 - 34, x0 + 52, y1 - 26], fill=(250, 250, 250))
    draw.rectangle([x0 + 24, y1 - 26, x0 + 52, y1 - 18], fill=(198, 38, 32))


def illo_chart_down(draw, box):
    """A red line plunges across the panel while grey bars shrink."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(242, 224, 220))
    pts = [(x0 + 8, y0 + 10), (x0 + 30, y0 + 20), (x0 + 52, y0 + 16),
           (x0 + 74, y0 + 34), (x1 - 10, y1 - 10)]
    draw.line(pts, fill=ACCENT_RED, width=4)
    draw.polygon([(x1 - 24, y1 - 12), (x1 - 8, y1 - 12), (x1 - 10, y1 - 28)],
                 fill=ACCENT_RED)
    for i in range(4):
        bx = x0 + 8 + i * 17
        draw.rectangle([bx, y0 + 12 + i * 5, bx + 11, y0 + 24 + i * 5],
                       fill=(120, 116, 110))


def illo_shield(draw, box):
    """A blue shield with a white check: a plot stopped in time."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 226, 238))
    cx = (x0 + x1) // 2
    top, mid, bot = y0 + 8, y0 + 30, y1 - 8
    draw.polygon([(cx - 34, top), (cx + 34, top), (cx + 34, mid),
                  (cx, bot), (cx - 34, mid)], fill=ACCENT_BLUE,
                 outline=INK, width=2)
    draw.line([(cx - 16, mid - 2), (cx - 4, mid + 12), (cx + 18, mid - 14)],
              fill=(255, 255, 255), width=4)


def illo_tanker(draw, box):
    """A tanker on grey-green water with flames at the bow."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(200, 214, 222))
    # Sky band and sun.
    draw.rectangle([x0, y0, x1, y0 + 22], fill=(232, 226, 200))
    draw.ellipse([x1 - 30, y0 + 4, x1 - 12, y0 + 22], fill=(250, 200, 90))
    # Waves.
    for wy in (y1 - 22, y1 - 14):
        for wx in range(x0 + 2, x1 - 10, 16):
            draw.arc([wx, wy - 4, wx + 14, wy + 6], 180, 360,
                     fill=ACCENT_BLUE, width=2)
    # Hull and deckhouse.
    draw.polygon([(x0 + 12, y1 - 24), (x1 - 12, y1 - 24), (x1 - 26, y1 - 12),
                  (x0 + 26, y1 - 12)], fill=(120, 40, 32), outline=INK,
                 width=1)
    draw.rectangle([x0 + 40, y1 - 38, x0 + 62, y1 - 24], fill=(240, 238, 228),
                   outline=INK, width=1)
    draw.rectangle([x0 + 66, y1 - 38, x0 + 72, y1 - 24], fill=(60, 60, 60))
    # Flames at the bow.
    for fx, fh in ((x1 - 34, 20), (x1 - 26, 28), (x1 - 18, 18)):
        draw.polygon([(fx - 5, y1 - 24), (fx, y1 - 24 - fh), (fx + 5, y1 - 24)],
                     fill=(250, 140, 40))
    draw.ellipse([x1 - 30, y1 - 30, x1 - 16, y1 - 16], fill=(250, 200, 60))


def illo_two_flags(draw, box):
    """UK flag beside the EU ring of stars on a pale ground."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 226, 240))
    ground = y1 - 12
    draw.line([x0 + 6, ground, x1 - 6, ground], fill=MUTED, width=2)
    # United Kingdom on the left pole.
    px = x0 + 6
    draw.line([px, y0 + 14, px, ground], fill=INK, width=2)
    draw.ellipse([px - 2, y0 + 11, px + 2, y0 + 15], fill=ACCENT_GOLD)
    fx0, fy0, fx1, fy1 = px + 2, y0 + 14, x0 + 38, y0 + 40
    draw.rectangle([fx0, fy0, fx1, fy1], fill=(36, 52, 130))
    draw.line([fx0, fy0, fx1, fy1], fill=(255, 255, 255), width=4)
    draw.line([fx0, fy1, fx1, fy0], fill=(255, 255, 255), width=4)
    fcx, fcy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    draw.rectangle([fcx - 4, fy0, fcx + 4, fy1], fill=(255, 255, 255))
    draw.rectangle([fx0, fcy - 4, fx1, fcy + 4], fill=(255, 255, 255))
    draw.rectangle([fcx - 2, fy0, fcx + 2, fy1], fill=(198, 38, 32))
    draw.rectangle([fx0, fcy - 2, fx1, fcy + 2], fill=(198, 38, 32))
    draw.rectangle([fx0, fy0, fx1, fy1], outline=INK, width=1)
    # European Union on the right pole: blue field, gold stars in a ring.
    px = x0 + 44
    draw.line([px, y0 + 14, px, ground], fill=INK, width=2)
    draw.ellipse([px - 2, y0 + 11, px + 2, y0 + 15], fill=ACCENT_GOLD)
    fx0, fy0, fx1, fy1 = px + 2, y0 + 14, x0 + 78, y0 + 40
    draw.rectangle([fx0, fy0, fx1, fy1], fill=(30, 48, 130), outline=INK,
                   width=1)
    scx, scy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    for k in range(12):
        import math
        ang = 2 * math.pi * k / 12 - math.pi / 2
        sx = scx + int(9 * math.cos(ang))
        sy = scy + int(8 * math.sin(ang))
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(250, 205, 60))


def illo_virus(draw, box):
    """A spiky virus sphere on a pale clinical background."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 238, 228))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    import math
    for k in range(12):
        ang = 2 * math.pi * k / 12
        x2 = cx + int(30 * math.cos(ang))
        y2 = cy + int(30 * math.sin(ang))
        draw.line([cx, cy, x2, y2], fill=(150, 60, 60), width=2)
        draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(150, 60, 60))
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(178, 44, 36),
                 outline=(120, 30, 30), width=2)
    for ox, oy in ((-10, -8), (8, -10), (-12, 8), (10, 10), (0, 0)):
        draw.ellipse([cx + ox - 3, cy + oy - 3, cx + ox + 3, cy + oy + 3],
                     fill=(120, 30, 30))


def illo_flame_gavel(draw, box):
    """Flames over a hillside with a judge's gavel below."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(240, 226, 196))
    # Hillside.
    draw.polygon([(x0, y1), (x0, y1 - 22), (x1, y1 - 34), (x1, y1)],
                 fill=(120, 96, 56))
    # Flames.
    for fx, fh in ((x0 + 18, 26), (x0 + 30, 36), (x0 + 42, 24)):
        draw.polygon([(fx - 6, y1 - 22), (fx, y1 - 22 - fh), (fx + 6, y1 - 22)],
                     fill=(250, 140, 40))
    draw.ellipse([x0 + 22, y1 - 40, x0 + 38, y1 - 24], fill=(250, 200, 60))
    # Gavel: handle and head at lower right.
    draw.line([x1 - 34, y1 - 8, x1 - 12, y1 - 26], fill=(90, 60, 30), width=4)
    draw.rectangle([x1 - 30, y1 - 34, x1 - 8, y1 - 24], fill=(120, 84, 44),
                   outline=INK, width=1)


def illo_cyclone(draw, box):
    """A spiral storm over a grey-blue sea."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(186, 208, 224))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for start, rad in ((20, 34), (140, 24), (260, 14)):
        draw.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                 start, start + 200, fill=(255, 255, 255), width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    draw.line([x0 + 6, y1 - 8, x1 - 6, y1 - 8], fill=ACCENT_BLUE, width=3)


def illo_cricket(draw, box):
    """A cricket bat leaning on the pitch, red ball in the air."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(198, 226, 178))
    draw.polygon([(x0 + 26, y1 - 10), (x0 + 40, y0 + 10), (x0 + 52, y0 + 14),
                  (x0 + 38, y1 - 6)], fill=(222, 196, 140), outline=INK,
                 width=2)
    draw.ellipse([x1 - 34, y0 + 22, x1 - 14, y0 + 42], fill=(200, 40, 36),
                 outline=INK, width=2)
    draw.line([x1 - 32, y0 + 26, x1 - 18, y0 + 38], fill=(255, 255, 255),
              width=2)


def illo_chart_up(draw, box):
    """A green line climbs while blue bars grow taller."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(224, 238, 226))
    pts = [(x0 + 8, y1 - 10), (x0 + 30, y1 - 22), (x0 + 52, y1 - 18),
           (x0 + 74, y1 - 36), (x1 - 10, y0 + 10)]
    draw.line(pts, fill=ACCENT_GREEN, width=4)
    draw.polygon([(x1 - 22, y0 + 8), (x1 - 6, y0 + 8), (x1 - 8, y0 + 24)],
                 fill=ACCENT_GREEN)
    for i in range(4):
        bx = x0 + 8 + i * 17
        draw.rectangle([bx, y1 - 16 - i * 5, bx + 11, y1 - 4], fill=ACCENT_BLUE)


def illo_star(draw, box):
    """A gold star on a dark stage curtain: a screen legend remembered."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 32, 64))
    # Curtain folds.
    for cx in range(x0, x1, 14):
        draw.line([cx, y0, cx + 6, y1], fill=(44, 48, 88), width=3)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    import math
    outer, inner = 26, 11
    pts = []
    for k in range(10):
        r = outer if k % 2 == 0 else inner
        ang = -math.pi / 2 + k * math.pi / 5
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(250, 205, 60), outline=(176, 128, 24), width=2)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(176, 128, 24))


def illo_screen(draw, box):
    """A monitor with a warning triangle: the cloud goes dark."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(222, 230, 236))
    # Monitor frame and stand.
    draw.rectangle([x0 + 10, y0 + 8, x1 - 10, y1 - 18], fill=(40, 44, 52),
                   outline=INK, width=2)
    draw.rectangle([x0 + 14, y0 + 12, x1 - 14, y1 - 22], fill=(180, 200, 216))
    draw.rectangle([(x0 + x1) // 2 - 12, y1 - 18, (x0 + x1) // 2 + 12, y1 - 8],
                   fill=(40, 44, 52))
    draw.line([(x0 + x1) // 2 - 20, y1 - 8, (x0 + x1) // 2 + 20, y1 - 8],
              fill=(40, 44, 52), width=3)
    # Warning triangle with an exclamation mark.
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    draw.polygon([(cx, cy - 18), (cx + 18, cy + 12), (cx - 18, cy + 12)],
                 fill=(250, 200, 40), outline=INK, width=2)
    draw.rectangle([cx - 2, cy - 10, cx + 2, cy + 2], fill=INK)
    draw.ellipse([cx - 2, cy + 5, cx + 2, cy + 9], fill=INK)


def illo_detective(draw, box):
    """A fedora and a magnifying glass: the TV detective remembered."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 232, 214))
    cx = (x0 + x1) // 2
    # Fedora: crown and wide brim.
    draw.rectangle([cx - 30, y0 + 26, cx + 30, y0 + 34], fill=(70, 58, 44))
    draw.polygon([(cx - 20, y0 + 26), (cx - 16, y0 + 8), (cx + 16, y0 + 8),
                  (cx + 20, y0 + 26)], fill=(90, 74, 56))
    draw.rectangle([cx - 20, y0 + 20, cx + 20, y0 + 26], fill=(40, 34, 28))
    # Magnifying glass at lower right.
    mx, my = x1 - 26, y1 - 24
    draw.ellipse([mx - 14, my - 14, mx + 14, my + 14], outline=INK, width=3)
    draw.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(200, 220, 235))
    draw.line([mx + 10, my + 10, mx + 22, my + 22], fill=INK, width=3)


ILLUSTRATIONS = {
    1: illo_missiles,
    2: illo_chart_down,
    3: illo_shield,
    4: illo_tanker,
    5: illo_two_flags,
    6: illo_virus,
    7: illo_flame_gavel,
    8: illo_cyclone,
    9: illo_cricket,
    10: illo_chart_up,
    11: illo_star,
    12: illo_screen,
    13: illo_detective,
}

LEADS = [
    (1, "Poland seeks NATO help after missiles land",
     "Two missiles and a drone came down in the south-east. Tusk: a "
     "deliberate provocation; Rutte: a grave violation. No one was hurt."),
    (2, "Wall Street in correction as AI rout deepens",
     "S&P 500 falls 3.7% to 6,910, its seventh straight loss and 10% "
     "below its October record. Nasdaq drops 5.3%."),
    (3, "Denmark expels Russian attache over rapper plot",
     "PET says Russian intelligence planned to kill rapper Kyivstoner at "
     "a Copenhagen concert. Two men are charged."),
]

SMALL = [
    (4, "Tanker hit in the Strait of Hormuz",
     "Struck off Khasab, Oman. Fire on board, no casualties."),
    (5, "UK and EU seal reset deal",
     "Food trade, carbon markets, youth mobility for 100,000."),
    (6, "Virginia's first measles death of 2026",
     "A child aged 0-4 has died. Virginia has 220 cases in 2026."),
    (7, "Palisades Fire arsonist convicted",
     "A jury convicts Jonathan Rinderknecht of starting the fire."),
    (8, "Cyclone Akvan crosses the Odisha coast",
     "Landfall near Gopalpur. Over 72,000 people were evacuated."),
    (9, "India fight back in the Wellington Test",
     "India 159/1 at stumps on day two, trailing by 209."),
    (10, "Sensex rallies; NSE now 5th-largest",
     "Sensex up nearly 898 points. NSE passes HKEX and NASDAQ."),
    (11, "Stewart's cause of death",
     "Cardiopulmonary arrest, Lewy body disorder. He was 86."),
    (12, "Microsoft outage hits Outlook and Teams",
     "Outage affects Outlook, Teams and 365 services worldwide."),
    (13, "Stacy Keach dies at 85",
     "The TV detective Mike Hammer dies after a long heart condition."),
]

INDEX_ITEMS = [
    (14, "World court: Myanmar committed genocide"),
    (15, "Zelenskyy: trilateral summit a 'failure'"),
    (16, "Trump defends calling Putin a friend"),
    (17, "US Senate rejects Iran war-powers resolution"),
    (18, "Iran war nears ninth month; Trump in no rush"),
    (19, "EU adopts 1bn euros in military aid for Ukraine"),
    (20, "UK pledges 1,000+ drones for Ukraine"),
    (21, "Kryvyi Rih: 2 dead, 42 injured in strikes"),
    (22, "Saudi coalition intercepts Houthi missiles over Riyadh"),
    (23, "COP31 climate talks enter final stage in Turkey"),
    (24, "Banks report cyberattacks on third-party vendors"),
    (25, "FAA ground stop snarls US flights into Monday"),
    (26, "Copa 737 clips UPS 767 at Miami taxiway"),
    (27, "YouTube 'preparing $3bn settlement' on addiction claims"),
    (28, "Trump pardons Pete Rose posthumously"),
    (29, "Gold and silver prices fall sharply in India"),
    (30, "Hyundai unveils 2027 Elantra in Los Angeles"),
    (31, "Tesla to wind down Cybertruck by mid-2027"),
    (32, "Wendy's rejects $1.4bn hostile takeover bid"),
    (33, "General strike disrupts Spain's ports and factories"),
    (34, "Pope Leo XIV to vote in US midterms by mail"),
    (35, "Pill hailed as pancreatic cancer breakthrough"),
    (36, "Potatoes grown in simulated lunar soil"),
    (37, "570 set Rocky world record in Philadelphia"),
    (38, "CrowdStrike in talks to buy Zscaler"),
]

PINS = {
    1: (0.568, 0.168),   # south-east Poland
    2: (0.255, 0.295),   # New York, USA (Wall Street)
    3: (0.548, 0.138),   # Copenhagen, Denmark
    4: (0.655, 0.400),   # Strait of Hormuz, off Khasab
    5: (0.498, 0.198),   # Brussels, Belgium
    6: (0.282, 0.332),   # Virginia, USA
    7: (0.145, 0.345),   # Los Angeles, USA
    8: (0.736, 0.429),   # Odisha, India
    9: (0.970, 0.830),   # Wellington, New Zealand
    10: (0.712, 0.415),  # Mumbai, India
    11: (0.482, 0.145),  # London, UK
    12: (0.125, 0.205),  # Seattle area, USA (Microsoft)
    13: (0.200, 0.330),  # US east coast (Stacy Keach)
}


def draw_masthead(draw):
    title_f = font(SERIF_BOLD, 52)
    title = "The Daily Compass"
    w = text_width(draw, title, title_f)
    draw.text(((WIDTH - w) / 2, 6), title, font=title_f, fill=INK)
    sub_f = font(SANS, 15)
    left = "Saturday 21 November 2026"
    right = "38 verified stories - reported Saturday 21 Nov 2026"
    draw.text((14, 66), left, font=sub_f, fill=INK)
    rw = text_width(draw, right, sub_f)
    draw.text((WIDTH - 14 - rw, 66), right, font=sub_f, fill=MUTED)
    draw.line([10, 62, WIDTH - 10, 62], fill=RULE, width=3)
    draw.line([10, 88, WIDTH - 10, 88], fill=RULE, width=1)


def draw_lead(draw, box, number, headline, deck):
    x0, y0, x1, y1 = box
    panel_frame(draw, box)
    illo_box = (x0 + 8, y0 + 8, x1 - 8, y0 + 70)
    ILLUSTRATIONS[number](draw, illo_box)
    draw_badge(draw, x0 + 10, y0 + 10, number)
    head_f = font(SERIF_BOLD, 19)
    y = draw_wrapped(draw, (x0 + 10, y0 + 78), headline, head_f, INK,
                     (x1 - x0) - 20, 2, max_lines=3)
    deck_f = font(SANS, 13)
    draw_wrapped(draw, (x0 + 10, y + 4), deck, deck_f, (40, 38, 32),
                 (x1 - x0) - 20, 3, max_lines=4)


def draw_small(draw, box, number, headline, deck):
    x0, y0, x1, y1 = box
    panel_frame(draw, box)
    illo_box = (x0 + 6, y0 + 6, x0 + 84, y1 - 6)
    ILLUSTRATIONS[number](draw, illo_box)
    draw_badge(draw, x0 + 8, y0 + 8, number)
    head_f = font(SERIF_BOLD, 12)
    y = draw_wrapped(draw, (x0 + 92, y0 + 8), headline, head_f, INK,
                     (x1 - x0) - 100, 1, max_lines=5)
    deck_f = font(SANS, 10)
    draw_wrapped(draw, (x0 + 92, y + 2), deck, deck_f, (40, 38, 32),
                 (x1 - x0) - 100, 1, max_lines=5)


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA, outline=PANEL_EDGE, width=2)

    def poly(points):
        pts = [(x0 + px * (x1 - x0), y0 + py * (y1 - y0)) for px, py in points]
        draw.polygon(pts, fill=LAND, outline=(90, 110, 74))

    # North America: Alaska and Canada across the top, the US east coast
    # down to a distinct Florida peninsula, the Gulf coast, Mexico and a
    # narrow Central America isthmus, then back up the Pacific coast.
    poly([(0.030, 0.200), (0.055, 0.150), (0.100, 0.115), (0.160, 0.100),
          (0.230, 0.110), (0.300, 0.145), (0.345, 0.185), (0.360, 0.250),
          (0.338, 0.295), (0.315, 0.335), (0.300, 0.360), (0.286, 0.420),
          (0.272, 0.405), (0.262, 0.362), (0.225, 0.360), (0.190, 0.375),
          (0.168, 0.430), (0.185, 0.465), (0.205, 0.475), (0.150, 0.450),
          (0.140, 0.390), (0.115, 0.335), (0.085, 0.285), (0.050, 0.245)])
    # Greenland.
    poly([(0.335, 0.055), (0.375, 0.060), (0.380, 0.100), (0.350, 0.115),
          (0.332, 0.090)])
    # South America: wide northern shoulder, Brazil bulging east, then a
    # long taper down to Patagonia.
    poly([(0.280, 0.500), (0.320, 0.480), (0.370, 0.500), (0.400, 0.550),
          (0.382, 0.660), (0.352, 0.780), (0.332, 0.880), (0.302, 0.860),
          (0.282, 0.700), (0.270, 0.580)])
    # Europe mainland: Iberia, Scandinavia across the top, eastern Europe
    # down to the Black Sea, with an Italian boot.
    poly([(0.472, 0.285), (0.470, 0.215), (0.482, 0.175), (0.505, 0.135),
          (0.535, 0.105), (0.570, 0.105), (0.600, 0.135), (0.608, 0.195),
          (0.595, 0.255), (0.565, 0.295), (0.540, 0.280), (0.520, 0.310),
          (0.505, 0.265), (0.490, 0.295)])
    # Britain and Iceland as island shapes.
    poly([(0.476, 0.105), (0.492, 0.090), (0.500, 0.130), (0.494, 0.168),
          (0.482, 0.160)])
    poly([(0.455, 0.085), (0.470, 0.082), (0.472, 0.100), (0.457, 0.102)])
    # Africa: broad northern coast, the Horn in the east, tapering south,
    # plus Madagascar off the south-east coast.
    poly([(0.458, 0.395), (0.470, 0.350), (0.510, 0.335), (0.560, 0.340),
          (0.595, 0.365), (0.612, 0.410), (0.600, 0.475), (0.575, 0.560),
          (0.562, 0.660), (0.548, 0.745), (0.520, 0.765), (0.500, 0.680),
          (0.478, 0.560), (0.462, 0.470)])
    poly([(0.592, 0.615), (0.608, 0.600), (0.610, 0.665), (0.596, 0.690)])
    # Anatolia, bridging Europe and Asia.
    poly([(0.568, 0.255), (0.600, 0.235), (0.618, 0.260), (0.610, 0.300),
          (0.580, 0.295)])
    # Asia mainland: Siberia across the top, the Pacific coast down past
    # Korea and Shanghai to Shenzhen, Vietnam and the Malay peninsula
    # spur, back up through Myanmar to the Himalaya line.
    poly([(0.608, 0.185), (0.650, 0.115), (0.720, 0.080), (0.810, 0.070),
          (0.900, 0.085), (0.955, 0.130), (0.962, 0.200), (0.930, 0.250),
          (0.905, 0.270), (0.878, 0.325), (0.848, 0.385), (0.832, 0.440),
          (0.818, 0.495), (0.802, 0.545), (0.778, 0.505), (0.762, 0.445),
          (0.756, 0.375), (0.720, 0.335), (0.680, 0.330), (0.645, 0.300),
          (0.618, 0.260)])
    # Arabia, with Bahrain on its Gulf coast.
    poly([(0.600, 0.315), (0.622, 0.285), (0.655, 0.295), (0.668, 0.340),
          (0.660, 0.400), (0.638, 0.455), (0.615, 0.430), (0.602, 0.375)])
    # India: a distinct triangular peninsula below the Himalaya line.
    poly([(0.692, 0.345), (0.720, 0.332), (0.748, 0.345), (0.756, 0.380),
          (0.744, 0.425), (0.738, 0.470), (0.726, 0.535), (0.712, 0.470),
          (0.700, 0.405)])
    poly([(0.718, 0.555), (0.728, 0.555), (0.728, 0.575), (0.718, 0.575)])
    # Japan, the Philippines and the Indonesian archipelago.
    poly([(0.902, 0.255), (0.920, 0.205), (0.936, 0.190), (0.934, 0.240),
          (0.918, 0.275)])
    poly([(0.862, 0.425), (0.874, 0.420), (0.876, 0.455), (0.864, 0.460)])
    poly([(0.752, 0.520), (0.766, 0.515), (0.782, 0.565), (0.770, 0.575)])
    poly([(0.800, 0.535), (0.828, 0.530), (0.834, 0.565), (0.806, 0.572)])
    poly([(0.782, 0.600), (0.838, 0.595), (0.840, 0.615), (0.784, 0.618)])
    poly([(0.895, 0.565), (0.950, 0.560), (0.958, 0.585), (0.900, 0.590)])
    # Australia: Cape York in the north-east, a rounded south coast,
    # plus Tasmania below.
    poly([(0.818, 0.650), (0.845, 0.605), (0.878, 0.600), (0.905, 0.630),
          (0.928, 0.675), (0.922, 0.745), (0.895, 0.790), (0.858, 0.795),
          (0.830, 0.745), (0.814, 0.695)])
    poly([(0.908, 0.820), (0.922, 0.818), (0.920, 0.840), (0.906, 0.838)])
    # Fiji: a small Pacific island dot east of Australia.
    poly([(0.951, 0.645), (0.973, 0.643), (0.976, 0.690), (0.960, 0.705),
          (0.950, 0.680)])
    # New Zealand: North and South Islands.
    poly([(0.956, 0.772), (0.972, 0.766), (0.982, 0.800), (0.976, 0.848),
          (0.960, 0.838), (0.954, 0.800)])
    poly([(0.944, 0.852), (0.960, 0.846), (0.968, 0.888), (0.960, 0.928),
          (0.944, 0.892), (0.940, 0.868)])
    label_f = font(SANS_BOLD, 12)
    draw.text((x0 + 10, y0 + 6), "WHERE THE NEWS HAPPENED - PINS 1-13",
              font=label_f, fill=INK)
    pin_f = font(SANS_BOLD, 10)
    for number, (fx, fy) in PINS.items():
        px = x0 + fx * (x1 - x0)
        py = y0 + fy * (y1 - y0)
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=BADGE_BG,
                     outline=(255, 255, 255), width=2)
        label = str(number)
        w = text_width(draw, label, pin_f)
        draw.text((px - w / 2, py - 6), label, font=pin_f, fill=BADGE_FG)


def draw_index(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_BG, outline=PANEL_EDGE, width=2)
    head_f = font(SERIF_BOLD, 15)
    draw.text((x0 + 10, y0 + 6), "ALSO TODAY - INDEX 14-38", font=head_f, fill=INK)
    draw.line([x0 + 8, y0 + 30, x1 - 8, y0 + 30], fill=RULE, width=1)
    item_f = font(SANS, 11)
    col_w = (x1 - x0 - 30) // 2
    col_x = [x0 + 10, x0 + 20 + col_w]
    col_y = [y0 + 36, y0 + 36]
    for idx, (number, headline) in enumerate(INDEX_ITEMS):
        col = 0 if idx < 13 else 1
        prefix = "%d. " % number
        y = draw_wrapped(draw, (col_x[col], col_y[col]), prefix + headline,
                         item_f, INK, col_w, 1, max_lines=2)
        col_y[col] = y + 1


def draw_footer(draw):
    foot_f = font(SANS, 11)
    text = ("Sources on file for every story. Market figures are Friday's "
            "closes, reported Saturday 21 November 2026.")
    w = text_width(draw, text, foot_f)
    draw.text(((WIDTH - w) / 2, HEIGHT - 20), text, font=foot_f, fill=MUTED)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)

    lead_top, lead_h, lead_gap = 96, 208, 8
    lead_w = (WIDTH - 20 - 2 * lead_gap) // 3
    for i, (number, headline, deck) in enumerate(LEADS):
        lx = 10 + i * (lead_w + lead_gap)
        draw_lead(draw, (lx, lead_top, lx + lead_w, lead_top + lead_h),
                  number, headline, deck)

    small_top = lead_top + lead_h + 8
    small_h = 132
    small_w = (WIDTH - 20 - 4 * 6) // 5
    row_items = [SMALL[:5], SMALL[5:]]
    for r, items in enumerate(row_items):
        ry = small_top + r * (small_h + 6)
        for c, (number, headline, deck) in enumerate(items):
            cx = 10 + c * (small_w + 6)
            draw_small(draw, (cx, ry, cx + small_w, ry + small_h),
                       number, headline, deck)

    map_top = small_top + 2 * small_h + 18
    draw_map(draw, (10, map_top, WIDTH - 10, map_top + 148))

    index_top = map_top + 148 + 8
    draw_index(draw, (10, index_top, WIDTH - 10, HEIGHT - 26))
    draw_footer(draw)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)
    return OUT_PATH


if __name__ == "__main__":
    print(render())


