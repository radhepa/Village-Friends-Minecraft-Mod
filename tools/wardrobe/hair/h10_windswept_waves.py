"""Windswept Waves: wavy hair blown to one side, a curling front wave and rippling locks at the nape."""
from paint import hair_box, k, scalp, shell

META = {"name": "Windswept Waves", "description": "Wavy, wind-blown hair swept to one side with a curling forelock."}


def waves(face, seed, base=2):
    """Diagonal wave bands: light crests and shaded troughs."""
    for y in range(face.h):
        for x in range(face.w):
            d = (x + y * 2 + seed) % 6
            face.set(x, y, k("H", base + 1 if d in (0, 1) else base - 1 if d == 4 else base))


def build(g):
    scalp(g, 901, side_rows=5, back_rows=8, sideburn=2)
    shell(g, 902, side_rows=4, back_rows=7, front=[(0, 1), (0, 2), (0, 3), (7, 1), (7, 2), (6, 1), (5, 1)])
    hat = g.part("hat")
    waves(hat.top, 3, 3)
    # Wavy locks blown toward the wearer's right.
    for i, (x, z, w, rz) in enumerate(((-2.4, -2.0, 4, -18), (1.4, -2.4, 4, -12), (-1.8, 1.2, 4, -16), (2.2, 1.0, 3, -8))):
        lock = g.piece(f"blown_lock_{i}", "HEAD", (-w / 2, -2, -1.5), (w, 2, 3), pivot=(x, -7.9, z), rotation=(0, 0, rz))
        hair_box(lock, 910 + i, 2, top_delta=1)
        waves(lock.top, i, 3)
        for f in lock.sides:
            waves(f, f.x0 + i, 2)
    # A forelock flicked across the brow.
    fore = g.piece("forelock", "HEAD", (-4, -1, -1), (4, 2, 1), pivot=(1.6, -8.4, -4.2), rotation=(-16, 0, -14))
    hair_box(fore, 920, 2, sheen_row=0, top_delta=2)
    lift = g.piece("wind_lift", "HEAD", (0, -1, -2.5), (1, 3, 5), pivot=(4.1, -7.8, .3), rotation=(0, 0, -30))
    hair_box(lift, 930, 2, sheen_row=0)
    side = g.piece("right_side", "HEAD", (-.5, 0, -3), (1, 5, 6), pivot=(-4.35, -7.8, .6), rotation=(0, 0, 4))
    hair_box(side, 931, 2, sheen_row=1)
    for i, (x, rz, length) in enumerate(((-3.0, 14, 5), (0, -6, 6), (3.0, 18, 5))):
        lock = g.piece(f"wave_lock_{i}", "HEAD", (-1.5, 0, 0), (3, length, 1), pivot=(x, -7.2, 4.2), rotation=(14, 0, rz))
        hair_box(lock, 940 + i, 2, sheen_row=1)
        waves(lock.back, i, 2)
