"""Great Plaid Kilt & Hose: the belted plaid's pleated lower fold, diced hose with garter flashes, and tongued brogues."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_male import check, skirt_panels, tartan
from paint import solid

META = {
    "name": "Great Plaid Kilt & Hose",
    "gender": "male",
    "description": "The great plaid's pleated lower fold belted at the waist, diced hose with garter flashes, and brogues with long tongues.",
    "tags": ["casual", "kilt", "rugged"],
    "locked_to": "t84_belted_great_plaid",
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        tartan(leg.strip, rows=range(0, 4))
        check(leg.strip, "A2", "S3", size=2, rows=range(5, 10))           # diced hose
        leg.strip.hline(0, leg.strip.w - 1, 5, "S2")
        tartan(leg.top)
    body = waistband(g, "P", "weave", 8411)
    for face in body.sides:
        tartan(face, rows=range(9, 12))
    footwear(g, "turnshoe", top=10, base=1)
    for side in SIDES:
        g.part(f"{side}_pants").front.hline(1, 2, 10, "L3")               # brogue tongue
    front, back, sides = skirt_panels(g, "plaid_kilt", 6, "P", "weave", 8412, top=10.4, side_len=5)
    for face in (front, back):
        tartan(face, ox=face.x0)
        for x in range(0, 9, 2):
            face.vline(x, 1, 5, "P0")
    for box in sides:
        for face in box.faces:
            tartan(face, ox=face.x0 + 2)
    for i, side in enumerate(SIDES):
        flash = g.piece(f"{side}_garter_flash", leg_bone(side), (-.5, 0, -.5), (1, 2, 1),
                        pivot=(-2.25 if side == "right" else 2.25, 5.4, -.6))
        solid(flash, "A", "plain", 8413 + i, 2, edge=False)
