"""Mountain Guide's Crampon Boots: wool breeches and turned-down knitted socks over laced mountain boots with iron crampons strapped beneath."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import ribbing
from kit_m07 import leg_shell
from paint import solid

META = {
    "name": "Mountain Guide's Crampon Boots",
    "gender": "male",
    "description": "Stout wool breeches, thick knitted socks turned down over laced mountain boots, and iron crampons strapped under the soles with two spikes jutting from each toe.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "weave", 37360, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 37361)
    footwear(g, "boot", top=6, base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        ribbing(leg.strip, "S", 3, rows=range(4, 6))                    # sock showing above the boot
        pants.front.vline(1, 7, 10, "L1"), pants.front.vline(2, 7, 10, "L1")   # the lace gap
        for y in (7, 9):
            pants.front.hline(1, 2, y, "L4")                             # crossed laces
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L1")                           # the crampon's ankle strap
        pants.front.set(0, 9, "M3"), pants.front.set(3, 9, "M3")
    for cuff in leg_shell(g, "sock_turn", 4.4, 2, "S", 3, "knit", 37362, inflate=.03):
        for face in cuff.sides:
            ribbing(face, "S", 3)
            face.hline(0, face.w - 1, 1, "S2")
    # The crampon frame round each sole, and its front points.
    for frame in leg_shell(g, "crampon_frame", 11.0, 1, "M", 2, "smooth", 37364, inflate=.05):
        for face in frame.sides:
            for x in range(face.w):
                face.set(x, 0, "M3" if x % 2 else "M1")
    for i, side in enumerate(SIDES):
        for j, x in enumerate((-1.2, 1.2)):
            spike = g.piece(f"{side}_crampon_point_{j}", leg_bone(side), (-.5, -.5, -1), (1, 1, 1),
                            pivot=(x, 11.6, -2.6), rotation=(-20, 0, 0))
            solid(spike, "M", "smooth", 37366 + i * 2 + j, 3, edge=False)
            spike.front.set(0, 0, "M4")
