"""Market Stallholder's Money Apron: a short leather change apron of three bulging coin pockets tied over a
spiral-laced bodice and linen partlet, a notched tally stick thrust through the apron ties."""
from kit_female import OVER_FRONT, bodice, chemise, girdle, lacing, over_panel
from paint import solid

META = {
    "name": "Market Stallholder's Money Apron",
    "gender": "female",
    "description": "A short leather change apron of three bulging coin pockets tied over a laced bodice and linen partlet, a notched tally stick thrust through the ties.",
    "tags": ["work", "apron", "casual"],
    "covers_waist": True,
}

SEED = 53270


def build(g):
    body, arms = chemise(g, "S", 3, "weave", SEED, neckline="high", sleeve_rows=(0, 11), gather=False)
    body.front.hline(1, 6, 0, "S4"), body.front.set(3, 1, "S2"), body.front.set(4, 1, "S2")   # the partlet's collar
    for arm in arms:
        arm.strip.hline(0, 15, 10, "S2")
        arm.front.vline(2, 1, 9, "S2")
    b = bodice(g, "P", "twill", SEED + 1, rows=(2, 9), neckline="square", edge="P1")
    lacing(b.front, 3, 3, 8, "spiral", lace="A3", under="P0", eyelet="M3")
    for face in (b.right, b.left):
        face.vline(1, 2, 9, "P3")
    # The money apron: tied round the waist, three coin pockets across its face.
    girdle(g, "apron_ties", 8.2, role="S", base=2, height=1, buckle=None, texture="weave", wide=True)
    apron = over_panel(g, "money_apron", 5, "L", "leather", SEED + 2, base=2, width=9, top=9.0)
    apron.hline(0, 8, 4, "L1"), apron.vline(0, 0, 4, "L1"), apron.vline(8, 0, 4, "L1")
    for x in (3, 6):
        apron.vline(x, 1, 3, "L1")                                   # pocket seams
    for i, x in enumerate((-3.0, 0.0, 3.0)):
        pocket = g.piece(f"coin_pocket_{i}", "TORSO", (-1, 1.2, -1.0), (2, 2, 1), pivot=(x, 9.0, OVER_FRONT),
                         motion="flap_front", inflate=.06)
        solid(pocket, "L", "leather", SEED + 3 + i, 2, edge=False)
        pocket.front.hline(0, 1, 0, "L3")                            # the stitched pocket mouth
        pocket.front.set(1 if i % 2 else 0, 1, "L1")
        pocket.top.fill("M3")
        pocket.top.set(i % 2, 0, "M4")                               # coin showing at the mouth
    tally = g.piece("tally_stick", "TORSO", (-.5, -2.5, -.5), (1, 4, 1), pivot=(-1.8, 7.8, -3.3), rotation=(0, 0, 18))
    solid(tally, "L", "smooth", SEED + 6, 3, edge=False)
    for y in range(4):
        tally.front.set(0, y, "L1" if y % 2 else "L4")               # notches cut for each debt
