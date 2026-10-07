"""Highland Tartan Skirt: a long pleated tartan skirt over laced ghillie shoes."""
from kit import SIDES
from kit_female import shoes, skirt, tartan

META = {
    "name": "Highland Tartan Skirt",
    "gender": "female",
    "description": "A long tartan skirt laid in pleats, with soft ghillie shoes laced high round the ankle.",
    "tags": ["casual", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 13511, top=9.8, length=11, folds=False, gather=False)
    s.paint(lambda f: tartan(f, "P", "A2", offset=f.x0))
    for face in s.wide_faces:
        for x in range(0, face.w, 2):
            face.vline(x, 1, face.h - 1, "P0")
    s.hem("P0")
    shoes(g, "turnshoe", "L", 2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, 15, 9, "S3")
        for face in pants.sides:
            for y in (8, 9):
                face.set(1 if y % 2 else 2, y, "L2")                  # ghillie laces up the ankle
