"""Byzantine Embroidered Leg Wraps: close hose bound knee to ankle in spiralling embroidered bands, with low shoes."""
from kit import SIDES, legs, waistband
from kit_male import leg_blk, toe_pieces
from paint import fabric

META = {
    "name": "Byzantine Embroidered Leg Wraps",
    "gender": "male",
    "description": "Close hose bound from knee to ankle in spiralling embroidered bands studded with bright stitches, jewelled garters and low pointed shoes.",
    "tags": ["fancy", "slim"],
}


def lattice(face, rows, ox=0):
    """Spiral bands wound up the shin, each edged dark and studded with an embroidered dot."""
    for y in rows:
        for x in range(face.w):
            p = (y + (x + ox) // 2) % 3                                    # bands climbing one row every two texels
            face.set(x, y, "P1" if p == 0 else "S3" if p == 1 else "S2")
            if p == 1 and (x + ox) % 4 == 1:
                face.set(x, y, "A3")


def build(g):
    legs(g, "P", "twill", 38021, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 38022)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        lattice(leg.strip, range(4, 10), ox=i * 2)
        lattice(pants.strip, range(4, 10), ox=i * 2)
        pants.strip.hline(0, pants.strip.w - 1, 4, "M2")                 # the garter at the knee
        pants.strip.hline(0, pants.strip.w - 1, 9, "S2")
        fabric(leg.strip, "K", "smooth", 38023, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "K", "smooth", 38024, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "A2")                          # embroidered shoe collar
            face.hline(0, face.w - 1, 11, "K0")
        leg.bottom.fill("K0"), pants.bottom.fill("K0")
        jewel = leg_blk(g, f"{side}_garter_jewel", side, 3.7, (1, 1, 1), "A", 3, "plain", 38025 + i,
                        dx=-.5 if side == "right" else .5, dz=-2.35)
        jewel.front.fill("A4")
    for toe in toe_pieces(g, "shoe_point", (2, 1, 2), "K", base=2, y=11.0, z=-2.1, seed=38027):
        toe.top.fill("K3")
