"""Box Braids: a crown of neatly parted squares and many long thin braids, a few capped with metal cuffs."""
from anime import ring_shell
from anime_female import strand, tie, SIDES
from paint import k, scalp

META = {"name": "Box Braids", "gender": "female",
        "description": "Many long, thin box braids from neatly parted squares, a few finished with metal cuffs."}

# (x, y, z, length, rx, rz, cuffed) for the braids down the back.
BACK = [(-3.6, -7.0, 4.5, 15, -3, 6, False), (-2.4, -7.6, 4.8, 17, -4, 3, True), (-1.2, -7.2, 4.5, 16, -4, 1, False),
        (0.0, -7.6, 4.85, 18, -4, 0, False), (1.2, -7.2, 4.5, 16, -4, -1, True), (2.4, -7.6, 4.8, 17, -4, -3, False),
        (3.6, -7.0, 4.5, 14, -3, -6, False), (-1.8, -5.0, 5.15, 13, -2, 2, False), (1.8, -5.0, 5.15, 14, -2, -2, False)]


def build(g):
    scalp(g, 8001, side_rows=8, back_rows=8, sideburn=0, part=3)
    head = g.part("head")
    for face in (head.top, head.back):   # the square parting grid
        for i in range(8):
            if i in (2, 5):
                face.hline(0, 7, i, k("H", 0)), face.vline(i, 0, 7, k("H", 0))
    hat = ring_shell(g, 8002, side_rows=6, back_rows=7)
    for i in (2, 5):
        hat.top.hline(0, 7, i, k("H", 1))
    hat.top.vline(3, 0, 7, k("H", 0))
    for side, sign in SIDES:
        # Two braids framing the face fall in front of the shoulders; two more behind the ear.
        strand(g, f"{side}_front_braid", (4.3 * sign, -7.6, -3.5), (-4, 0, -3 * sign), ((1, 14, 0, 1),), 1, 8010 + (sign > 0),
               ring=None, texture="braidlet", motion="sway")
        tie(g, f"{side}_front_cuff", (4.3 * sign, -7.6, -3.5), (-4, 0, -3 * sign), (1, 1, 1), y=11.5, role="M", base=3, motion="sway")
        strand(g, f"{side}_cheek_braid", (4.5 * sign, -7.4, -2.2), (-14, 0, -5 * sign), ((1, 12, 0, 1),), 1, 8013 + (sign > 0),
               ring=None, texture="braidlet", motion="sway")
        for j, (z, n) in enumerate(((.4, 8), (2.6, 14))):
            strand(g, f"{side}_side_braid_{j}", (4.55 * sign, -7.4, z), (2 if j else 0, 0, -4 * sign), ((1, n, 0, 1),), 1,
                   8016 + j * 2 + (sign > 0), ring=None, texture="braidlet", motion="sway" if j else "none")
    for i, (x, y, z, n, rx, rz, cuffed) in enumerate(BACK):
        strand(g, f"back_braid_{i}", (x, y, z), (rx, 0, rz), ((1, n, 0, 1),), 1, 8030 + i, ring=None, texture="braidlet",
               motion="sway")
        if cuffed:
            tie(g, f"back_cuff_{i}", (x, y, z), (rx, 0, rz), (1, 1, 1), y=n - 2.5, role="M", base=3, motion="sway")
