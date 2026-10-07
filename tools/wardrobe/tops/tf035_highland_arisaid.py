"""Highland Arisaid: a great tartan plaid draped over the shoulders, belted at the waist and pinned with a round brooch."""
from kit_female import chemise, girdle, mantle, over_flaps, tartan
from paint import solid

META = {
    "name": "Highland Arisaid",
    "gender": "female",
    "description": "A great tartan plaid wrapped over the shoulders, belted at the waist and pinned with a big round brooch.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 3, "weave", 13501, neckline="round", sleeve_rows=(0, 11))
    j = g.part("jacket")
    for face in j.sides:
        tartan(face, "P", "A2", offset=face.x0)
    tartan(j.top, "P", "A2")
    for x, y in [(3, 0), (4, 0), (3, 1), (4, 1), (2, 0), (5, 0)]:
        j.front.clear(x, y)
    drape = mantle(g, "plaid_drape", "P", "plain", 13502, 2, height=3, width=11, depth=6, y=-.8)
    for face in drape.faces:
        tartan(face, "P", "A2", offset=face.x0)
    pin = g.piece("brooch", "TORSO", (-1.5, -1.5, -.5), (3, 3, 1), pivot=(-2.0, 2.8, -3.0), inflate=.05)
    solid(pin, "M", "smooth", 13503, 3, edge=False)
    pin.front.set(1, 1, "A2"), pin.front.set(0, 0, "M4"), pin.front.set(2, 2, "M1")
    girdle(g, "belt", 8.0, role="L", height=1, wide=True)
    f, bk = over_flaps(g, "plaid_skirt", 10, "P", "plain", 13504, width=10, top=9.0)
    for face in (f, bk):
        tartan(face, "P", "A2", offset=3)
        for x in range(0, face.w, 2):
            face.set(x, 0, "P0")
        for x in range(face.w):
            if x % 2:
                face.set(x, face.h - 1, "S3")                        # fringed edge
