"""Smith's Apron: a short-sleeved henley under a riveted leather bib apron, with work gloves."""
from paint import cap, fabric, grid, k, line, rivets, solid, strip_fabric

META = {
    "name": "Smith's Apron",
    "description": "Henley work shirt, riveted leather bib apron with a stocked pocket, and heavy gloves.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "P", "twill", 141, 2)
    cap(body, "P", texture="twill", seed=141)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    f.vline(4, 1, 3, "P1")
    f.set(3, 1, "M3"), f.set(3, 3, "M3")
    # Leather bib on the jacket layer with neck strap, pocket and corner rivets.
    jf, jb = jacket.front, jacket.back
    fabric(jf, "L", "leather", 142, 2, 1, 2, 6, 10)
    jf.vline(1, 0, 1, "L2"), jf.vline(6, 0, 1, "L2")
    jf.hline(1, 6, 2, "L3")
    jf.vline(1, 3, 11, "L1"), jf.vline(6, 3, 11, "L3")
    jf.set(1, 2, "M3"), jf.set(6, 2, "M3")
    grid(jf, 2, 5, ["dddd", "dLLd", "dddd"], {"d": "L1", "L": "L2"})
    jf.set(4, 4, "M3"), jf.set(4, 3, "M4")   # a rule tucked in the pocket
    jacket.top.vline(1, 0, 3, "L2"), jacket.top.vline(6, 0, 3, "L2")
    line(jb, 1, 0, 6, 8, "L2")
    line(jb, 6, 0, 1, 8, "L2")
    jb.hline(0, 7, 9, "L2")
    jb.set(3, 9, "L3"), jb.set(4, 9, "L3"), jb.set(3, 10, "L1"), jb.set(4, 10, "L2"), jb.set(4, 11, "L1")
    for face in (jacket.right, jacket.left):
        face.hline(0, face.w - 1, 9, "L2")

    for side in ("right", "left"):
        arm, sleeve = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        strip_fabric(arm, "P", "twill", 143, 2, 0, 3)
        fabric(arm.top, "P", "twill", 143, 3)
        arm.strip.hline(0, arm.strip.w - 1, 3, "P3")
        arm.strip.hline(0, arm.strip.w - 1, 4, "X1")
        # Heavy gauntlet gloves over the hands.
        strip_fabric(sleeve, "L", "leather", 144, 2, 8, 11)
        for face in sleeve.sides:
            face.hline(0, face.w - 1, 8, "L3")
            face.hline(0, face.w - 1, 9, "L1")
        fabric(sleeve.bottom, "L", "leather", 145, 1)

    # Long apron skirt: it rides on the leading leg.
    skirt = g.piece("apron_skirt", "TORSO", (-3.5, 0, 0), (7, 7, 1), pivot=(0, 11.3, -2.95), motion="flap_front")
    solid(skirt, "L", "leather", 146, 2)
    s = skirt.front
    s.vline(0, 0, 6, "L1"), s.vline(6, 0, 6, "L3")
    s.hline(0, 6, 6, "L1")
    grid(s, 1, 1, ["ddddd", "dLLLd", "ddddd"], {"d": "L1", "L": "L2"})
    s.set(1, 1, "M3"), s.set(5, 1, "M3")
