"""Wavy Layers: soft waves to the shoulders, wispy bangs and pointed wave tips."""
from anime import bangs, lock, ring_shell
from paint import k

META = {"name": "Wavy Layers", "gender": "male", "description": "Shoulder-length waves with wispy bangs and pointed tips."}


def waves(face, seed, base=2):
    for y in range(face.h):
        for x in range(face.w):
            d = (x + y * 2 + seed) % 6
            face.set(x, y, k("H", base + 1 if d in (0, 1) else base - 1 if d == 4 else base))


def build(g):
    from paint import scalp
    scalp(g, 2701, side_rows=7, back_rows=8, sideburn=1, part=2)
    hat = ring_shell(g, 2702, side_rows=6, back_rows=8)
    waves(hat.top, 2, 3)
    bangs(g, "bang", [(-4.1, ((2, 4), (1, 2)), 10), (-1.6, ((3, 2), (2, 1)), 16), (1.0, ((3, 2), (2, 1)), 4), (3.4, ((2, 3), (1, 1)), -10)], 2710)
    for side, sign in (("right", -1), ("left", 1)):
        for j, (z, length, tilt) in enumerate(((-2.4, 8, 3), (-.2, 9, 6), (2.0, 8, 4))):
            boxes = lock(g, f"{side}_wave_{j}", (4.3 * sign, -7.6, z), (0, 0, -tilt * sign), ((1, length - 2), (1, 2)), 2, 2720 + j * 5 + (sign > 0))
            for f in boxes[0].sides:
                waves(f, j + (sign > 0), 2)
    for i, (x, rz) in enumerate(((-3.0, 6), (0, 0), (3.0, -6))):
        boxes = lock(g, f"back_wave_{i}", (x, -7.6, 4.25), (5, 0, rz), ((3, 8), (2, 1), (1, 1)), 1, 2750 + i)
        for f in boxes[0].sides:
            waves(f, i, 2)
