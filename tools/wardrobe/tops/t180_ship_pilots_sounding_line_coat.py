"""Ship's Pilot's Sounding-Line Coat: a short buttoned wool coat with a broad linen collar, a neat flat coil of
sounding line marked at the fathoms hung at the hip with its lead swinging below, and a rolled chart in the belt."""
from kit import belt, body, flaps, sleeves
from kit_male import blk
from paint import solid

META = {
    "name": "Ship's Pilot's Sounding-Line Coat",
    "gender": "male",
    "description": "A short buttoned wool coat with a broad linen collar, a flat coil of sounding line marked at the "
                   "fathoms hung at the hip with its lead below, and a rolled chart tucked into the belt.",
    "tags": ["sea", "casual", "scholarly"],
    "covers_waist": True,
}

COIL = (2.0, 9.8, -3.4)      # the coil's hook on the belt; coil, lead line and lead share the hinge


def coil_face(face):
    """Concentric turns of laid line: alternating lit and shaded rings, a dark eye in the middle."""
    for y in range(face.h):
        for x in range(face.w):
            ring = min(x, y, face.w - 1 - x, face.h - 1 - y)
            face.set(x, y, "S3" if ring % 2 == 0 else "S1")
    face.set(face.w // 2, face.h // 2, "K1")


def build(g):
    b = body(g, "P", "twill", 33360)
    f = b.front
    f.vline(4, 1, 11, "P1"), f.vline(3, 1, 11, "P3")
    for y in range(3, 11, 2):
        f.set(4, y, "M3")
    sleeves(g, "P", "twill", 33361, rows=(0, 10), cuff="S3")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "S2")
    # The broad collar: linen lying flat over the shoulders, square at the back.
    coll = g.piece("linen_collar", "TORSO", (-4.5, -.4, -2.6), (9, 1, 5), inflate=.08)
    solid(coll, "S", "weave", 33362, 3, edge=False)
    coll.front.hline(0, 8, 0, "S4"), coll.front.clear(4, 0), coll.front.set(4, 0, "S1")
    back = blk(g, "linen_collar_back", (0, .5, 2.55), (6, 2, 1), "S", 3, "weave", 33363)
    back.back.hline(0, 5, 1, "S2")
    belt(g, "belt", 9.4, height=1)
    # The sounding line: a flat coil on a hook, the leg of line running down to the lead.
    coil = blk(g, "sounding_coil", COIL, (4, 4, 1), "S", 2, "plain", 33364, origin=(-2, .4, -.5), motion="flap_front")
    coil_face(coil.front), coil_face(coil.back)
    for face in (coil.top, coil.bottom, coil.right, coil.left):
        for i in range(face.w * face.h):
            face.set(i % face.w, i // face.w, "S3" if i % 2 else "S1")
    coil.front.set(0, 1, "A2"), coil.front.set(3, 2, "A3")               # fathom marks of red and white rag
    line_leg = blk(g, "sounding_line", COIL, (1, 2, 1), "S", 3, "plain", 33365, origin=(1.0, 4.4, -.5),
                   motion="flap_front", edge=False)
    line_leg.front.set(0, 1, "A2")
    lead = blk(g, "sounding_lead", COIL, (1, 2, 1), "M", 1, "smooth", 33366, origin=(1.0, 6.4, -.5),
               motion="flap_front")
    lead.bottom.fill("K1")
    # A rolled chart tucked slantwise through the belt at the back.
    chart = blk(g, "rolled_chart", (-1.6, 9.2, 3.4), (1, 6, 1), "S", 4, "plain", 33367, origin=(-.5, -3.0, -.5),
                rotation=(0, 0, 28))
    chart.strip.hline(0, chart.strip.w - 1, 1, "A2")
    chart.top.fill("S2"), chart.bottom.fill("S2")
    for face in flaps(g, "coat_hem", 3, "P", "twill", 33368, top=11.0, slit=True):
        face.hline(0, 8, 2, "P1")
