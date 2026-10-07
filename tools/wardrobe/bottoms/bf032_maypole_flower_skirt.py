"""Maypole Flower Skirt: a festival skirt sewn with flowers, three ribbon bands at the hem and dancing slippers."""
from kit_female import scatter, shoes, skirt

META = {
    "name": "Maypole Flower Skirt",
    "gender": "female",
    "description": "A full festival skirt sewn all over with little flowers, three ribbon bands at the hem and dancing slippers.",
    "tags": ["whimsical", "fancy", "skirt"],
    "locked_to": "tf032_maypole_ribbon_bodice",
}


def build(g):
    s = skirt(g, "P", "weave", 13211, top=9.8, length=10, flare=7)
    for face in s.wide_faces:
        scatter(face, "flower", "A2", "M3", step=(4, 4), y0=2, y1=6)
    s.band(4, "line", "A2", from_bottom=True)
    s.band(2, "line", "S4", from_bottom=True)
    s.band(0, "line", "M3", from_bottom=True)
    shoes(g, "slipper", "A", 2)
    for side in ("right", "left"):
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, 15, 8, "S4"), leg.strip.hline(0, 15, 9, "S4"), leg.strip.hline(0, 15, 10, "S3")
        leg.strip.set(5, 10, "A2"), leg.strip.set(13, 10, "A2")
