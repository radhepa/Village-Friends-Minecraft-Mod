"""Oyster Seller's Shell-Basket Bodice: a horn-buttoned work bodice over a rolled chemise, a knotted
neckerchief, and a shallow basket heaped with oysters slung on the right hip with an oyster knife
tucked in its strap."""
from kit import roll
from kit_f03 import basket
from kit_female import bodice, chemise
from paint import line, solid

META = {
    "name": "Oyster Seller's Shell-Basket Bodice",
    "gender": "female",
    "description": "A horn-buttoned work bodice, a knotted neckerchief and a shallow basket heaped with oysters slung on the hip.",
    "tags": ["sea", "work", "casual"],
}

SEED = 53060


def oysters(face, seed):
    """A heap of rough grey shells: ridged ovals with pale lips and the odd open, pearly one."""
    for y in range(face.h):
        for x in range(face.w):
            cell = (x + 2 * (y % 2)) % 3
            face.set(x, y, "M1" if cell == 0 else "M3" if (x + y + seed) % 5 == 0 else "M2")
    face.set(1 % face.w, 0, "S4"), face.set(min(face.w - 1, 3), face.h - 1, "S4")


def build(g):
    chemise(g, "S", 3, "weave", SEED, neckline="scoop", sleeve_rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    b = bodice(g, "P", "twill", SEED + 1, rows=(2, 9), neckline="square", edge="P3")
    b.front.vline(3, 2, 9, "P1")                                    # the front edges meet
    for y in (3, 5, 7):
        b.front.set(4, y, "L3"), b.front.set(4, y + 1, "L1")       # horn buttons
    for face in (b.right, b.left):
        face.vline(1, 2, 9, "P3")
    # The basket strap: over the left shoulder, across the chest to the right hip.
    line(b.front, 7, 0, 2, 8, "L2"), line(b.front, 7, 1, 3, 8, "L1")
    line(b.back, 0, 0, 6, 9, "L2")
    b.top.vline(6, 0, 3, "L2")
    # A neckerchief knotted at the throat, its two tails falling over the bodice.
    ring = g.piece("neckerchief", "TORSO", (-4.5, -.5, -2.5), (9, 1, 5), inflate=.06)
    solid(ring, "A", "weave", SEED + 2, 2, edge=False)
    for f in ring.sides:
        for x in range(0, f.w, 2):
            f.set(x, 0, "A3")
    knot = g.piece("neckerchief_knot", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(-.6, .4, -1.75))
    solid(knot, "A", "plain", SEED + 3, 2, edge=False)
    knot.front.set(0, 0, "A3"), knot.front.set(1, 1, "A1")
    for i, (x, rot) in enumerate(((-1.4, 12), (-.1, -10))):
        tail = g.piece(f"neckerchief_tail_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 2.2, -2.75), rotation=(0, 0, rot))
        solid(tail, "A", "plain", SEED + 4 + i, 2)
        tail.front.set(0, 2, "A1")
    # The oyster knife: a short stout blade tucked through the strap on the chest.
    knife = g.piece("oyster_knife", "TORSO", (-.5, -1.5, -.5), (1, 3, 1), pivot=(1.6, 4.6, -2.75), rotation=(0, 0, 32))
    solid(knife, "L", "smooth", SEED + 6, 2, edge=False)
    knife.front.set(0, 0, "M4"), knife.back.set(0, 0, "M3"), knife.front.set(0, 2, "L1")
    # A shallow round basket on the right hip, heaped with oysters.
    bk = basket(g, "oyster_basket", "TORSO", (-2.5, 0, -1.5), (5, 2, 3), pivot=(-1.5, 9.0, -4.7), role="L", base=2)
    for f in bk.sides:
        f.hline(0, f.w - 1, f.h - 1, "L1")
    heap = g.piece("oyster_heap", "TORSO", (-2, -1, -1), (4, 1, 2), pivot=(-1.5, 9.0, -4.7), inflate=.15)
    for f in heap.faces:
        oysters(f, SEED + 7)
    heap.bottom.fill("M1")
    crown = g.piece("oyster_heap_top", "TORSO", (-1.5, -2, -.5), (3, 1, 1), pivot=(-1.5, 9.0, -4.7), inflate=.1)
    for f in crown.faces:
        oysters(f, SEED + 9)
    shell = g.piece("open_oyster", "TORSO", (-.5, -1.4, -.5), (1, 1, 1), pivot=(-2.9, 8.4, -5.5), inflate=.15)
    solid(shell, "S", "plain", SEED + 8, 4, edge=False)
    shell.front.set(0, 0, "M3")
