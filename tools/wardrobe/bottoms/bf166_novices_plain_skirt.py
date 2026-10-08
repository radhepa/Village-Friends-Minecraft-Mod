"""Novice's Plain Skirt: an ankle-length skirt of undyed wool with two growth tucks sewn above the hem,
ready to be let down, over plain turnshoes."""
from kit_female import shoes, skirt

META = {
    "name": "Novice's Plain Skirt",
    "gender": "female",
    "description": "A plain ankle-length skirt of undyed wool with two growth tucks above the hem, over simple turnshoes.",
    "tags": ["simple", "casual", "skirt", "long_skirt", "holy"],
}


def build(g):
    s = skirt(g, "S", "plain", 55211, base=1, top=9.8, length=11, back_length=11, flare=4, folds=False, gather=False)
    for face in s.wide_faces:
        face.vline(2, 2, 3, "S0"), face.vline(7, 2, 3, "S0")             # soft folds from the waist
    for from_bottom in (2, 5):
        s.band(from_bottom, "line", "S2", from_bottom=True)              # the tuck's lit fold
        s.band(from_bottom - 1, "line", "S0", from_bottom=True)          # and its shadow beneath
    shoes(g, "turnshoe", "L", 1)
