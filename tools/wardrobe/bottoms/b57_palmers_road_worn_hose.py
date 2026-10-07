"""Palmer's Road-Worn Hose: dusty hose darned at knee and shin, in turned-down travel boots badged with a scallop shell."""
from kit import SIDES, footwear, legs, waistband
from kit_male import flecks, leg_rings

META = {
    "name": "Palmer's Road-Worn Hose",
    "gender": "male",
    "description": "Dusty hose darned at the knees and shins from the long road, in turned-down travel boots badged with a scallop shell.",
    "tags": ["holy", "rugged"],
    "locked_to": "t57_palmers_scallop_cloak",
}


def build(g):
    legs(g, "S", "weave", 5711, base=2, rows=(0, 7), crease=False)
    waistband(g, "S", "weave", 5712)
    footwear(g, "boot", top=7, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.rect(1, 3, 2, 2, "S1"), leg.front.set(2, 3, "S3")        # darned knee
        leg.front.set(1, 6, "S1")
        flecks(leg.strip, "S3", 5713, .1, rows=range(0, 7))
        flecks(pants.strip, "L3", 5714, .12, rows=range(8, 11))           # road dust on the boots
    for ring in leg_rings(g, "boot_turn", 6.0, "L", (5, 2, 5), 2, "leather", 5715, inflate=.1):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
        ring.front.set(2, 1, "S4"), ring.front.set(1, 0, "S4"), ring.front.set(3, 0, "S4")   # scallop badge
