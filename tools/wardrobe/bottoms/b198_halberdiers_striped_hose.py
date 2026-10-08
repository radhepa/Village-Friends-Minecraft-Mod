"""Halberdier's Striped Hose: hose striped top to toe in the two house colours, bowed knee garters and broad square-toed shoes."""
from kit import SIDES, footwear, waistband
from kit_male import leg_blk, toe_pieces
from kit_m04 import sides_of

META = {
    "name": "Halberdier's Striped Hose",
    "gender": "male",
    "description": "Close hose striped from hip to ankle in the two house colours, tied below the knee with bowed garters, "
                   "over broad square-toed 'cow-mouth' shoes slashed across the vamp.",
    "tags": ["martial", "fancy", "slim"],
}

S = 34100


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        st = leg.strip
        for y in range(0, 10):
            for x in range(st.w):
                stripe = (x // 2) % 2
                st.set(x, y, ("A2" if x % 2 == 0 else "A1") if stripe else ("P2" if x % 2 == 0 else "P3"))
        leg.top.fill("P2")
        st.hline(0, st.w - 1, 5, "S3"), st.hline(0, st.w - 1, 6, "S1")        # garter
    body = waistband(g, "P", "velvet", S)
    for face in body.sides:
        for x in range(face.w):
            if (x // 2) % 2:
                face.vline(x, 10, 11, "A2")
    footwear(g, "shoe", top=10, role="L", base=1)
    for i, side in enumerate(SIDES):
        bow = leg_blk(g, f"{side}_garter_bow", side, 5.0, (1, 2, 1), "S", 3, "plain", S + 2 + i,
                      dx=-2.3 if side == "right" else 2.3)
        getattr(bow, sides_of(side)[0]).set(0, 1, "S1")
    for toe in toe_pieces(g, "cow_mouth_toe", (4, 2, 2), "L", base=1, texture="smooth", seed=S + 4, y=10.0, z=-1.9):
        toe.top.hline(0, 3, 0, "A2"), toe.top.set(0, 1, "L2"), toe.top.set(3, 1, "L2")   # slashed vamp
        toe.front.hline(0, 3, 1, "K1")
        toe.front.set(0, 0, "L2"), toe.front.set(3, 0, "L2")
