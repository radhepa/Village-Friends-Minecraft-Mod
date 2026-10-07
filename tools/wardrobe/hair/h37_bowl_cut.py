"""Bowl Cut: the medieval pudding-basin cut, a rounded cap of hair cut to one blunt line above the
brows and ears, the sides and nape shaved below the line."""
from anime import ring_shell
from anime_male import clump, plate, shave
from paint import scalp

META = {"name": "Bowl Cut", "gender": "male",
        "description": "The medieval pudding-basin cut: a blunt line above the brows and ears, shaved beneath."}


def build(g):
    head = g.part("head")
    scalp(g, 3701, side_rows=4, back_rows=4, sideburn=0)
    for face in (head.right, head.left, head.back):
        shave(face, 3702 + face.x0, range(4, 8 if face is head.back else 7), density=.3)
    ring_shell(g, 3703, side_rows=3, back_rows=3, ring_row=1)
    # The blunt fringe: four clumps cut straight across above the brows.
    for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        clump(g, f"fringe_{i}", (x, -8.55, -4.35 - (i % 2) * .1), (2, 3, 1), rotation=(-6, 0, 0), seed=3710 + i * 3, ring=0)
    # The same line around the sides and back.
    for side, sign in (("right", -1), ("left", 1)):
        for j, z in enumerate((-2.8, 0, 2.8)):
            clump(g, f"{side}_{j}", (4.35 * sign + .08 * sign * (j % 2), -8.5, z), (1, 4, 3), seed=3720 + j + (sign > 0) * 3, ring=1)
    for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        clump(g, f"back_{i}", (x, -8.5, 4.35 + (i % 2) * .08), (2, 4, 1), seed=3730 + i * 3, ring=1)
    # A rounded crown swirling out from the whorl.
    for i, (x, z, ry) in enumerate(((-1.6, -1.4, 20), (1.6, -1.4, -20), (0, 1.8, 0))):
        plate(g, f"crown_{i}", (x, -8.35, z), (3, 1, 4), rotation=(0, ry, 0), seed=3740 + i, sheen=1)
