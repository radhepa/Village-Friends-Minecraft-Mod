"""Wise Woman's Herb-Pocket Skirt: a dark calf-length skirt with a band of patch pockets sewn across the
front, bundles of herbs poking out of each, a ragged hem and striped stockings."""
from kit import SIDES
from kit_f05 import lap_panel
from kit_female import SKIRT_FRONT, dags, shoes, skirt
from paint import solid

META = {
    "name": "Wise Woman's Herb-Pocket Skirt",
    "gender": "female",
    "description": "A dark calf-length skirt with a row of patch pockets across the front, herb bundles poking out of each.",
    "tags": ["casual", "whimsical", "skirt"],
}


def build(g):
    s = skirt(g, "K", "weave", 55061, base=2, top=9.8, length=9, folds=True)
    s.paint(lambda f: dags(f, f.h - 1, "K", 2, step=3))
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(5, 10):
            leg.strip.hline(0, 15, y, "S3" if y % 2 else "A1")      # striped stockings below the hem
    shoes(g, "ankle", "L", 1)
    # The pocket band: three patch pockets in a row, each with a herb bundle tucked in.
    band = lap_panel(g, 9.8, "pocket_band", 2.2, 3, 10, "S", 2, "weave", 55062)
    f = band.front
    for x0 in (0, 3, 7):
        f.vline(x0, 0, 2, "S1")
    f.hline(0, 9, 0, "S3"), f.hline(0, 9, 2, "S1")
    for x in (1, 2, 4, 5, 8):
        f.set(x, 1, "S2")
    band.front.set(9, 1, "S1")
    herbs = [(-3.5, "A", 2), (-0.5, "L", 3), (3.0, "A", 3)]
    for i, (x, role, base) in enumerate(herbs):
        bundle = g.piece(f"herb_bundle_{i}", "TORSO", (-.5 + x, 1.0, -.17), (1, 2, 1), pivot=(0, 9.8, SKIRT_FRONT),
                         motion="flap_front")
        solid(bundle, role, "plain", 55063 + i, base, edge=False)
        for face in bundle.sides:
            face.set(0, 0, f"{role}{base + 1}"), face.set(0, 1, "S1")
        tuft = g.piece(f"herb_tuft_{i}", "TORSO", (-1 + x, .1, -.17), (2, 1, 1), pivot=(0, 9.8, SKIRT_FRONT),
                       motion="flap_front")
        solid(tuft, role, "plain", 55066 + i, base + 1, edge=False)
        tuft.front.set(0, 0, f"{role}{base}")
