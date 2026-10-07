"""Morris Dancer's Baldrics: a white shirt crossed by two ribbon baldrics with a rosette, and kerchiefs tied at the wrists."""
from kit import body, neckline, sleeves
from kit_male import arm_x, blk
from paint import line, solid

META = {
    "name": "Morris Dancer's Baldrics",
    "gender": "male",
    "description": "A white dancing shirt crossed front and back by two ribbon baldrics meeting at a rosette, kerchiefs tied at both wrists.",
    "tags": ["whimsical", "casual"],
    "locked_to": "b91_morris_bell_pads",
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 9101, base=4)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 9102, base=4, rows=(0, 10), cuff="S2")
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        line(face, 0, 0, 7, 10, "A2"), line(face, 1, 0, 7, 9, "A3")
        line(face, 7, 0, 0, 10, "P2"), line(face, 6, 0, 0, 9, "P3")
        face.hline(0, 7, 11, "A2")
    for y in range(4):
        jacket.top.set(0, y, "A2"), jacket.top.set(7, y, "P2")
    rosette = blk(g, "rosette", (0, 4.6, -2.75), (2, 2, 1), "A", 3, "plain", 9103, edge=False)
    rosette.front.set(0, 0, "P3"), rosette.front.set(1, 1, "P3")
    for i, (x, rz) in enumerate(((-.6, 8), (.6, -8))):
        tail = blk(g, f"rosette_tail_{i}", (x, 6.4, -2.8), (1, 3, 1), "A" if i else "P", 2, "plain", 9104 + i,
                   rotation=(0, 0, rz), motion="sway")
    for i, side in enumerate(("right", "left")):
        x = arm_x(side) + 2.0
        hanky = g.piece(f"{side}_kerchief", "RIGHT_ARM" if side == "right" else "LEFT_ARM", (-1, 0, -.5), (2, 3, 1),
                        pivot=(x, 8.2, -2.4), motion="sway")
        solid(hanky, "S", "plain", 9106 + i, 4)
        hanky.front.set(0, 2, "S2"), hanky.front.set(1, 0, "A3")
