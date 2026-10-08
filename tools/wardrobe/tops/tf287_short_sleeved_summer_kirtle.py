"""Short-Sleeved Summer Kirtle: a light kirtle with elbow sleeves and turned-up cuffs, tied shut with ribbon bows."""
from kit import SIDES, body
from kit_female import arm_rings, neck
from paint import fabric, grid, solid, strip_fabric

META = {
    "name": "Short-Sleeved Summer Kirtle",
    "gender": "female",
    "description": "A light summer kirtle with a bound scoop neck, elbow sleeves with turned-up cuffs and two ribbon bows tying the front shut.",
    "tags": ["casual", "relaxed", "simple"],
}

BOW = ["a..a", ".bb.", "a..a"]


def build(g):
    b = body(g, "P", "plain", 60040, base=3)
    neck(b.front, "scoop", "P", 3, edge="A2")
    b.front.vline(3, 10, 11, "P2")                                     # the edge-to-edge closing below the bows
    for face in (b.front, b.back):
        face.vline(0, 4, 11, "P2"), face.vline(7, 4, 11, "P2")
    b.back.hline(1, 6, 0, "A2")                                          # the binding runs round the back neck
    for face in (b.right, b.left):
        face.hline(0, 3, 0, "A2")
        face.vline(1, 2, 11, "P2")
    j = g.part("jacket")
    for y in (3, 7):
        grid(j.front, 2, y, BOW, {"a": "A3", "b": "A1"})                  # ribbon bows, raised on the overlay
    # Sleeves stop at the elbow; the turned-up cuff shows the binding along its top.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "plain", 60041 + (side == "left"), 3, 0, 3)
        fabric(arm.top, "P", "plain", 60043, 4)
        outer = arm.right if side == "right" else arm.left
        outer.vline(1, 0, 3, "P2")
    for ring in arm_rings(g, "turned_cuff", 1.6, 2, 5, inflate=.06):
        solid(ring, "P", "plain", 60044, 3, edge=False)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "A2")
            face.hline(0, face.w - 1, 1, "P2")
        ring.top.fill("A2"), ring.bottom.fill("P1")
