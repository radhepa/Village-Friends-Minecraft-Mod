"""Low Ponytail: swept back and tied at the nape with a palette ribbon; the tail sways as they walk."""
from paint import hair_box, k, scalp, shell, solid

META = {"name": "Low Ponytail", "gender": "male", "description": "Swept-back hair tied low with a ribbon, loose strands framing the face."}


def build(g):
    scalp(g, 401, side_rows=4, back_rows=8, sideburn=1)
    head = g.part("head")
    for x in range(8):   # combed-back lines on the crown
        if x % 2:
            head.top.vline(x, 0, 7, "H1")
    shell(g, 402, side_rows=2, back_rows=7, front=[(0, 1), (0, 2), (0, 3), (7, 1), (7, 2), (7, 3)])
    hat = g.part("hat")
    for x in range(8):
        hat.top.set(x, 7, "H3" if x % 2 else "H2")
    # A soft swell at the back of the crown where the hair is gathered.
    swell = g.piece("crown_swell", "HEAD", (-3, -1, -1), (6, 2, 3), pivot=(0, -7.9, 2.4), rotation=(-14, 0, 0))
    hair_box(swell, 410, 2, top_delta=1)
    # Face-framing strands at the temples.
    for side, x in (("right", -4.6), ("left", 3.6)):
        strand = g.piece(f"{side}_strand", "HEAD", (0, 0, -.5), (1, 5, 1), pivot=(x, -7.4, -3.9), rotation=(0, 0, 4 if side == "right" else -4))
        hair_box(strand, 420 + (side == "left"), 2, sheen_row=0)
    # Ribbon tie in the outfit's accent color, then the tail.
    tie = g.piece("ribbon", "HEAD", (-1.5, -1, 0), (3, 2, 1), pivot=(0, -2.2, 4.3))
    solid(tie, "A", "plain", 430, 2, edge=False)
    tie.back.set(1, 0, "A3")
    for side, rz in (("right", 30), ("left", -30)):
        bow = g.piece(f"ribbon_{side}", "HEAD", (-1, -.5, 0), (2, 1, 1), pivot=(-1.4 if side == "right" else 1.4, -2.4, 4.45), rotation=(0, 0, rz))
        solid(bow, "A", "plain", 431, 2, edge=False)
    gather = g.piece("tail_root", "HEAD", (-1.5, 0, 0), (3, 2, 2), pivot=(0, -3.0, 4.0))
    hair_box(gather, 440, 2)
    tail = g.piece("tail", "HEAD", (-1.5, 0, -1), (3, 6, 2), pivot=(0, -1.2, 5.3), rotation=(10, 0, 0), motion="sway")
    hair_box(tail, 441, 2, sheen_row=1)
    tip = g.piece("tail_tip", "HEAD", (-1, 0, -1), (2, 2, 2), pivot=(0, 4.6, 6.2), rotation=(16, 0, 0), motion="sway")
    hair_box(tip, 442, 2)
