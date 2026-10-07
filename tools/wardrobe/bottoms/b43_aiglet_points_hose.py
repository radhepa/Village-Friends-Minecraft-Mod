"""Aiglet-Points Hose: close footed hose with leather-soled feet, trussed to the doublet by laces tipped with metal aiglets."""
from kit import SIDES, waistband
from kit_male import blk
from paint import fabric, strip_fabric

META = {
    "name": "Aiglet-Points Hose",
    "gender": "male",
    "description": "Close-fitting footed hose with sewn leather soles, trussed up by laces tipped with metal aiglets at the waist.",
    "tags": ["casual", "slim"],
}


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "velvet", 4311, 2, 0, 11)
        fabric(leg.top, "P", "velvet", 4311, 2)
        leg.back.vline(1 if side == "right" else 2, 0, 10, "P1")          # back seam
        leg.bottom.fill("L0")
        pants.strip.hline(0, pants.strip.w - 1, 11, "L2")                 # the sewn sole
        pants.front.hline(0, 3, 10, "L2"), pants.back.hline(0, 3, 10, "L1")
        pants.bottom.fill("L1")
    waistband(g, "P", "velvet", 4312)
    for i, (x, z) in enumerate(((-2.4, -2.75), (2.4, -2.75), (-2.4, 2.35), (2.4, 2.35))):
        point = blk(g, f"waist_point_{i}", (x, 9.0, z), (1, 2, 1), "A", 2, "plain", 4313 + i)
        point.strip.hline(0, point.strip.w - 1, 1, "M3")                  # metal aiglet
