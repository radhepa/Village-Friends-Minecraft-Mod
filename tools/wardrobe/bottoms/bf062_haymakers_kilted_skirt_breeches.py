"""Haymaker's Kilted Skirt over Breeches: the overskirt rolled up round the hips into a thick kilted roll,
leaving a short skirt over linen breeches tied below the knee, bare shins and low laced shoes."""
from kit import SIDES, legs
from kit_female import leg_rings, shoes, skirt
from paint import k, solid

META = {
    "name": "Haymaker's Kilted Skirt over Breeches",
    "gender": "female",
    "description": "An overskirt rolled up round the hips into a thick kilted roll above a short skirt, linen breeches tied below the knee and low laced shoes.",
    "tags": ["work", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51061, top=10.2, length=6, flare=7, folds=False)
    legs(g, "S", "twill", 51060, base=2, rows=(0, 6), crease=False)
    for face in s.wide_faces:
        for x in range(1, face.w - 1, 3):
            face.vline(x, 2, face.h - 2, "P1")
    s.hem("P1")
    # The rolled-up overskirt: a thick twisted roll of cloth round the hips.
    roll = g.piece("waist_kilted_roll", "TORSO", (-5.5, 0, -3.2), (11, 2, 6), pivot=(0, 9.1, .1), inflate=.12)
    solid(roll, "P", "weave", 51062, 2, edge=False)
    for face in roll.sides:
        for x in range(face.w):
            face.set(x, 0, k("P", 3 if (x // 2) % 2 == 0 else 2))
            face.set(x, 1, k("P", 1 if (x // 2) % 2 == 0 else 2))
    roll.top.fill("P3"), roll.bottom.fill("P1")
    # Breeches gathered under the knee with a tie, then bare shins.
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, leg.strip.w - 1, 6, "S1")
    for box in leg_rings(g, "breech_tie", 5.6, 1, 5, inflate=.04):
        solid(box, "S", "plain", 51063, 3, edge=False)
        box.front.set(1, 0, "A2"), box.front.set(2, 0, "A3")
    shoes(g, "ankle", "L", 2, top=10)
