"""Charcoal Burner's Sooty Trousers: trousers blackened from the boots up, sacking bound round the shins, and wooden-soled boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import flecks, wraps

META = {
    "name": "Charcoal Burner's Sooty Trousers",
    "gender": "male",
    "description": "Work trousers blackened with soot from the boots up, sacking bound round the shins against embers, and wooden-soled boots.",
    "tags": ["work", "rugged"],
    "locked_to": "t96_charcoal_burners_sooty_smock",
}


def build(g):
    legs(g, "P", "weave", 9611, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 9612)
    footwear(g, "boot", top=10, base=1, sole="L3")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for y in range(10):
            flecks(leg.strip, "K3", 9613, max(0.0, (y - 2) / 24), rows=range(y, y + 1))
        wraps(pants.strip, "S", range(5, 9), base=1, period=4)            # sacking round the shins
        flecks(pants.strip, "K3", 9614, .08, rows=range(5, 9))
