"""Seaweed Gatherer's Kelp-Basket Bodice: a spiral-laced wool bodice under the broad straps of a tall wicker
creel, wet kelp heaped in it and trailing over its rim, and a short wrack hook at her belt."""
from kit import roll
from kit_f03 import basket, front_prop
from kit_female import bodice, chemise, girdle, lacing
from paint import fabric, rnd, solid

META = {
    "name": "Seaweed Gatherer's Kelp-Basket Bodice",
    "gender": "female",
    "description": "A spiral-laced bodice under the straps of a tall wicker creel heaped with wet kelp that trails over its rim, a wrack hook at her belt.",
    "tags": ["sea", "work", "rugged"],
}

SEED = 53240


def kelp(face, seed):
    """Wet brown fronds: long glossy blades with a pale midrib and the odd swollen bladder."""
    for y in range(face.h):
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            face.set(x, y, "K1" if (x + face.x0) % 3 == 0 else "K4" if r > .8 else "K3")
    for y in range(1, face.h, 3):
        face.set((y * 2 + seed) % face.w, y, "L3")                    # a swollen bladder


def build(g):
    chemise(g, "S", 3, "weave", SEED, neckline="scoop", sleeve_rows=(0, 4))
    roll(g, "S", 1.8, base=3)
    b = bodice(g, "P", "weave", SEED + 1, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "spiral", lace="S3", under="P0", eyelet="M2")
    # The creel's two broad straps over the shoulders, down the front to the armpits.
    for face, xs in ((b.front, (0, 7)), (b.back, (1, 6))):
        for x in xs:
            face.vline(x, 0, 5 if face is b.front else 3, "L2")
            face.set(x, 0, "L3")
    for x in (0, 7):
        b.top.vline(x, 0, 3, "L2")
    for face in (b.right, b.left):
        face.hline(0, face.w - 1, 5, "L1")                           # the straps run back under the arms
    girdle(g, "belt", 8.0, role="L", base=1, height=1, buckle="M")
    # The creel: tall wicker on the back, heaped with kelp that spills over the rim.
    creel = basket(g, "creel", "TORSO", (-3, 0, 0), (6, 8, 4), pivot=(0, .8, 2.4), role="L", base=2, inside="K1")
    for f in creel.sides:
        f.hline(0, f.w - 1, 4, "L1")                                 # a binding row half way down
    heap = g.piece("kelp_heap", "TORSO", (-2.5, -1, 0), (5, 1, 3), pivot=(0, .8, 3.3), inflate=.1)
    for f in heap.faces:
        kelp(f, SEED + 2)
    for i, (x, n, rot) in enumerate(((-2.2, 5, 6), (-.4, 7, -4), (1.6, 4, 8))):
        frond = g.piece(f"kelp_frond_{i}", "TORSO", (-.5, 0, 0), (1, n, 1), pivot=(x, .3, 6.45), rotation=(6, 0, rot),
                        motion="sway")
        for f in frond.faces:
            kelp(f, SEED + 3 + i)
        frond.back.set(0, n - 1, "K1")
    # A short iron wrack hook hung at the left hip, its point turned forward.
    hook = front_prop(g, "wrack_hook", 3.2, (1, 3, 1), y=0, role="L", base=2, seed=SEED + 7, top=8.6)
    hook.front.set(0, 0, "L3")
    tip = front_prop(g, "wrack_hook_tip", 3.2, (1, 1, 2), y=3, role="M", base=2, seed=SEED + 8, top=8.6, edge=False)
    tip.front.fill("M3")
