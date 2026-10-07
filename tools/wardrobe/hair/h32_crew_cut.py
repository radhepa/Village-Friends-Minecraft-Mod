"""Crew Cut: high-and-tight faded sides, the top a little longer at the front and brushed up and
back into a low ridge."""
from anime_male import clipped, clipped_scalp, combed_face, plate, taper

META = {"name": "Crew Cut", "gender": "male",
        "description": "High-and-tight faded sides under a short top, brushed up and back at the front."}


def build(g):
    clipped_scalp(g, 3201, base=1, side_rows=7, back_rows=7, fade_rows=5, sideburn=0)
    hat = g.part("hat")
    combed_face(hat.top, 3202, 2)
    for face in (hat.right, hat.left, hat.back):
        clipped(face, 3203 + face.x0, 1, rows=[0])
    hat.front.hline(0, 7, 0, "H2")
    # The front ridge: short locks brushed up and back, longest at the hairline.
    for i, x in enumerate((-2.5, 0, 2.5)):
        taper(g, f"ridge_{i}", (x, -8.3, -3.2), (-46, 0, -x * 3), ((3, 2, 2), (2, 1, 1)), seed=3210 + i * 3, ring=0, up=True)
    for i, x in enumerate((-1.3, 1.3)):
        taper(g, f"mid_{i}", (x, -8.3, -.8), (-58, 0, -x * 4), ((3, 1, 2), (2, 1, 1)), seed=3230 + i * 3, ring=None, up=True)
    # Shorter at the crown, lying almost flat.
    for i, (x, z) in enumerate(((-1.6, 1.6), (1.6, 1.8), (0, 3.2))):
        plate(g, f"crown_{i}", (x, -8.3, z), (3, 1, 2), rotation=(-6, 0, x * 3), seed=3250 + i, sheen=0)
