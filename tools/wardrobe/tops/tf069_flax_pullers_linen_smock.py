"""Flax Puller's Linen Smock: a loose undyed linen smock with a pin-tucked yoke, a drawstring neck and tied
cuffs, a bundle of pulled flax, roots and blue flowers, slung across her back."""
from kit import body, sleeves
from kit_female import neck
from kit_f01 import bundle
from paint import k, solid

META = {
    "name": "Flax Puller's Linen Smock",
    "gender": "female",
    "description": "A loose undyed linen smock with a pin-tucked yoke, drawstring neck and tied cuffs, a bundle of pulled flax with blue flowers slung across her back.",
    "tags": ["work", "simple", "relaxed"],
}


def build(g):
    b = body(g, "S", "weave", 51320, base=3)
    neck(b.front, "round", "S", 3, edge="S4")
    for face in (b.front, b.back):
        for x in range(face.w):
            face.vline(x, 1, 3, k("S", 4 if x % 2 else 2))            # pin-tucks across the yoke
        face.hline(0, face.w - 1, 4, "S2")
        for x in (2, 5):
            face.vline(x, 6, 11, "S2")                                # the smock's loose falls
    for face in (b.right, b.left):
        face.vline(1, 5, 11, "S2")
    for arm in sleeves(g, "S", "weave", 51321, base=3, rows=(0, 11)):
        arm.strip.hline(0, 15, 1, "S2")
        arm.strip.hline(0, 15, 8, "A2")                               # tapes tying the cuffs back
        arm.strip.hline(0, 15, 9, "S4"), arm.strip.hline(0, 15, 10, "S2"), arm.strip.hline(0, 15, 11, "S3")
    b.front.hline(0, 7, 8, "S1"), b.back.hline(0, 7, 8, "S1")       # a cord tied round the waist
    for face in (b.right, b.left):
        face.hline(0, 3, 8, "S1")
    for i, x in enumerate((-.6, .6)):
        end = g.piece(f"drawstring_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, .9, -2.55), motion="sway")
        solid(end, "A", "plain", 51322 + i, 2, edge=False)
        end.front.set(0, 1, "A3")
    # A bundle of pulled flax across her back: earthy roots below, two ties, blue flowers at the top.
    flax = bundle(g, "flax_bundle", "TORSO", (0, 6.0, 3.3), (2, 12, 2), rotation=(0, 0, 25), role="M", base=2,
                  seed=51324, ties=(4, 8), tie="S1", head_rows=3, head=("A2", "A3"))
    for f in flax.sides:
        f.hline(0, f.w - 1, 11, "L1"), f.set(0, 10, "L2")
    flax.bottom.fill("L0")
