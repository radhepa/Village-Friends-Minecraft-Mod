"""Jester's Bell Hose: chequered motley hose, each leg reversed, in long soft shoes curled up at the toe with a bell."""
from kit import SIDES, waistband
from kit_male import check, toe_pieces
from paint import fabric

META = {
    "name": "Jester's Bell Hose",
    "gender": "male",
    "description": "Chequered motley hose with each leg reversed, in long soft shoes curling up at the toe, a little bell on every tip.",
    "tags": ["whimsical", "fancy"],
    "locked_to": "t67_jesters_motley",
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        a, b = ("P2", "A2") if side == "right" else ("A2", "P2")
        check(leg.strip, a, b, size=2, rows=range(0, 10))
        check(leg.top, a, b, size=2)
        fabric(leg.strip, "A" if side == "right" else "P", "plain", 6711, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "A" if side == "right" else "P", "plain", 6712, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        leg.bottom.fill("K1"), pants.bottom.fill("K1")
    waistband(g, "P", "plain", 6713)
    for i, toe in enumerate(toe_pieces(g, "curl_toe", (2, 1, 3), "A", base=2, texture="plain", y=11.0, z=-2.1)):
        toe.top.fill("A3")
    for tip in toe_pieces(g, "bell_tip", (1, 1, 1), "M", base=3, texture="smooth", y=9.9, z=-4.8):
        tip.bottom.fill("M1")
