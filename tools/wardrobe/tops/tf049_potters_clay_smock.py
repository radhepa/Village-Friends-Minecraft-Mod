"""Potter's Clay Smock: a smock smeared with clay from the wheel, forearms grey to the elbow and a towel at the waist."""
from kit import roll
from kit_female import chemise, girdle, hanging, splotch
from paint import line, rnd

META = {
    "name": "Potter's Clay Smock",
    "gender": "female",
    "description": "A smock smeared with wet clay from the wheel, sleeves pushed up over clay-grey forearms and a towel at the waist.",
    "tags": ["work", "casual"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 14901, neckline="keyhole", sleeve_rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in range(6, 12):
            for x in range(16):
                if y > 8 or rnd(x, y, 14902) < .55:
                    arm.strip.set(x, y, "L3" if (x + y) % 4 else "L2")   # clay to the elbow
    for face in (body.front, body.back):
        line(face, 1, 5, 3, 9, "L3"), line(face, 2, 5, 4, 9, "L2")    # wiped-hand streaks
        splotch(face, "L3", 14903 + face.x0, count=2, y0=6, y1=11)
    line(body.front, 6, 6, 5, 10, "L3")
    girdle(g, "girdle", 8.2, role="L", height=1, buckle=None)
    towel = hanging(g, "towel", 2.8, 5, role="S", base=4, width=2, top=9.0, texture="weave")
    towel.front.set(0, 3, "L3"), towel.front.set(1, 4, "L2")
