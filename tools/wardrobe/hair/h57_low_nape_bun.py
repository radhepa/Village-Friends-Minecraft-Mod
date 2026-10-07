"""Low Nape Bun: centre-parted and combed smoothly back over the ears into a round bun low at the
nape, wound with a cord, a couple of short strands loose beneath it."""
from anime_male import SIDES, clump, combed_face, hat_ring, plate, taper, tie
from paint import scalp

META = {"name": "Low Nape Bun", "gender": "male",
        "description": "Centre-parted, combed smoothly back over the ears into a round bun at the nape."}


def build(g):
    scalp(g, 5701, side_rows=6, back_rows=8, sideburn=0, part=3)
    hat = hat_ring(g, 5702, rows={"back": 8, "right": 5, "left": 5})
    combed_face(hat.top, 5703, 3)
    hat.top.vline(3, 0, 7, "H0"), hat.top.vline(4, 0, 7, "H1")
    hat.front.hline(0, 7, 0, "H2")
    # From the part the hair is combed smoothly down each side, then back over the ear.
    for side, sign in SIDES:
        plate(g, f"{side}_sweep", (.25 * sign, -8.35, -.6), (4, 1, 7), origin=(0 if sign > 0 else -4, -1, -3.5),
              rotation=(0, 0, 12 * sign), seed=5710 + (sign > 0), sheen=1, across=True)
        drape = clump(g, f"{side}_drape", (4.45 * sign, -8.2, .2), (1, 4, 7), rotation=(14, 0, -3 * sign), seed=5715 + (sign > 0))
        combed_face(drape.right if sign < 0 else drape.left, 5717 + (sign > 0), 2, sheen=1, across_y=True)
    # Down the back to the bun, converging as it goes.
    for i, x in enumerate((-2.0, 2.0)):
        back = clump(g, f"back_{i}", (x, -8.5, 4.4), (4, 6, 1), rotation=(4, 0, x * 3), seed=5720 + i)
        combed_face(back.back, 5722 + i, 2, sheen=1)
    tie(g, "cord", (0, -2.4, 4.8), (3, 1, 2), role="A", seed=5730)
    clump(g, "bun", (0, -2.2, 5.3), (4, 3, 3), origin=(-2, -1.5, -1), seed=5731, ring=0)
    clump(g, "bun_coil", (0, -3.4, 6.3), (2, 1, 2), origin=(-1, -1, -1), rotation=(-20, 0, 30), seed=5732, top_delta=2)
    for i, (x, rz) in enumerate(((-1.4, 8), (1.4, -8))):
        taper(g, f"loose_{i}", (x, -.6, 4.5), (4, 0, rz), ((1, 2, 1), (1, 1, 1)), seed=5740 + i * 3, ring=None)
