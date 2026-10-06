"""Heavy Work Trousers: reinforced knees, steel-toed lace-up boots, a wide belt and a hip hammer."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Heavy Work Trousers",
    "gender": "male",
    "description": "Heavy twill with stitched knee pads, steel-toed boots, a wide belt and a hammer at the hip.",
    "tags": ["work", "sturdy"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "twill", 151 if side == "right" else 152, 1, 0, 9)
        fabric(leg.top, "P", "twill", 15, 1)
        outer = leg.right if side == "right" else leg.left
        outer.vline(2 if side == "right" else 1, 0, 8, "P0")
        # Stitched knee pads on the overlay.
        for face in (pants.front, pants.right if side == "right" else pants.left):
            fabric(face, "S", "twill", 153, 2, 0, 4, face.w, 3)
            for x in range(face.w):
                face.set(x, 4, "S3" if x % 2 else "S1")
                face.set(x, 6, "S1" if x % 2 else "S2")
        # Lace-up boots with steel toes.
        strip_fabric(leg, "L", "leather", 154, 2, 9, 11)
        for face in pants.sides:
            fabric(face, "L", "leather", 155, 2, 0, 8, face.w, 4)
            face.hline(0, face.w - 1, 8, "L3")
            face.hline(0, face.w - 1, 11, "K1")
        grid(pants.front, 0, 8, ["LSSL", "1SS1", "MMMM", "1111"], {"L": "L3", "S": "S3", "1": "L1", "M": "M2"})
        pants.front.set(1, 10, "M3")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")

    body = g.part("body")
    strip_fabric(body, "P", "twill", 156, 1, 9, 11)
    fabric(body.bottom, "P", "twill", 16, 1)
    belt = g.piece("waist_belt", "TORSO", (-4.65, 9.5, -2.65), (9, 2, 5), inflate=.05)
    solid(belt, "L", "leather", 157, 2)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    grid(belt.front, 3, 0, ["MMM", "M.M"], {"M": "M2"})
    belt.front.set(4, 1, "L0")
    # A hammer hangs from a loop at the back of the right hip.
    handle = g.piece("hip_hammer_handle", "TORSO", (-.5, 0, -.5), (1, 5, 1), pivot=(-2.4, 10.2, 2.75), rotation=(0, 0, 8))
    solid(handle, "L", "leather", 158, 3)
    handle.strip.hline(0, handle.strip.w - 1, 0, "L1")
    head = g.piece("hip_hammer_head", "TORSO", (-1.5, 5, -.75), (3, 2, 1), pivot=(-2.4, 10.2, 2.75), rotation=(0, 0, 8), inflate=.15)
    solid(head, "M", "smooth", 159, 2)
    head.front.set(0, 0, "M4"), head.back.set(0, 0, "M3")
