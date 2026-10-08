"""Wood Gatherer's Faggot Bundle: a rough wool kirtle with turned-back cuffs, a carrying rope over the
shoulder, a billhook at the hip and a tied bundle of sticks slung slantwise across her back."""
from kit import body, sleeves
from kit_f07 import prop, rope
from kit_female import OVER_BACK, neck

META = {
    "name": "Wood Gatherer's Faggot Bundle",
    "gender": "female",
    "description": "A rough wool kirtle with turned-back cuffs, a carrying rope across the breast, a billhook at the "
                   "hip and a rope-tied faggot of sticks slung slantwise on her back.",
    "tags": ["work", "rugged"],
}


def build(g):
    b = body(g, "P", "plain", 57601)
    neck(b.front, "round", "P", 2, edge="P3")
    for face in (b.right, b.left):
        face.vline(2, 0, 11, "P1")                                   # side seams
    b.back.vline(4, 1, 11, "P1")
    for face in b.sides:
        face.hline(0, face.w - 1, 8, "L1")                          # a plain rope girdle
    b.front.set(2, 9, "L2"), b.front.set(2, 10, "L1")
    sleeves(g, "P", "plain", 57602, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 8, "S3"), arm.strip.hline(0, 15, 9, "S2")   # turned-back cuffs
    # The carrying rope, from the left shoulder down across the breast, and round the back.
    j = g.part("jacket")
    rope(j.front, 6, 0, 0, 7, "S", 2)
    rope(j.back, 1, 0, 7, 7, "S", 2)
    j.top.vline(6, 0, 3, "S3")
    j.right.set(3, 7, "S1"), j.right.set(2, 8, "S2")
    # The faggot: a bundle of sticks, rope-tied in two places, slanting from the left shoulder to the right hip.
    bundle = prop(g, "faggot", "TORSO", (-2, -5, 0), (4, 10, 3), pivot=(.2, 5.2, 2.4), rotation=(0, 0, 30),
                  role="L", texture="smooth", seed=57603, base=2)
    for face in bundle.sides:
        for x in range(face.w):
            face.vline(x, 0, face.h - 1, "L1" if (x + face.x0) % 2 else "L3")
        for y in (2, 7):
            face.hline(0, face.w - 1, y, "S2")
            face.set((y // 2) % face.w, y, "S4")
    for face in (bundle.top, bundle.bottom):
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "L4" if (x + y) % 2 == 0 else "L2")   # cut ends
    # A few longer twigs straggling out of the back of the bundle and its lower end.
    for i, (dx, oy, oz, h) in enumerate(((-1.4, -7.0, 2.2, 3), (.6, -6.0, 2.2, 2), (-.5, 4.5, 1.0, 2))):
        twig = prop(g, f"faggot_twig_{i}", "TORSO", (dx - .5, oy, oz), (1, h, 1), pivot=(.2, 5.2, 2.4),
                    rotation=(0, 0, 30), role="L", base=3, seed=57604 + i, edge=False)
        twig.top.fill("L4")
    # A billhook hung from the girdle at the back of the left hip.
    z = OVER_BACK + .1
    handle = prop(g, "billhook", "TORSO", (-.5, 0, 0), (1, 3, 1), pivot=(3.0, 8.8, z), role="L", base=2,
                  seed=57607, motion="flap_back")
    handle.back.set(0, 0, "L3")
    blade = prop(g, "billhook_blade", "TORSO", (-.5, 3, 0), (1, 3, 1), pivot=(3.0, 8.8, z), role="M", base=2,
                 seed=57608, motion="flap_back")
    blade.back.set(0, 0, "M3"), blade.back.set(0, 2, "M1")
    hook = prop(g, "billhook_hook", "TORSO", (.5, 5, 0), (1, 1, 1), pivot=(3.0, 8.8, z), role="M", base=3,
                seed=57609, edge=False, motion="flap_back")
    hook.back.fill("M4")
