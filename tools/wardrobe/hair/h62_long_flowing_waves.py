"""Long Flowing Waves: side-parted hair falling in loose S-waves past the shoulders, a deep wave swept
across the brow and long waves framing the face from outside the cheeks."""
from anime import ring_shell
from anime_male import SIDES, chain, taper, wave_face
from paint import scalp

META = {"name": "Long Flowing Waves", "gender": "male",
        "description": "Side-parted hair in loose S-waves past the shoulders, a deep wave across the brow."}


def wave(g, pid, start, swing, length, seed, axis="z"):
    """A long lock bending side to side (axis z) or back and forth (axis x) as it falls."""
    rot = (lambda a: (0, 0, a)) if axis == "z" else (lambda a: (a, 0, 0))
    return chain(g, pid, start, [(2, length, 2, rot(swing)), (2, length, 1, rot(-swing)), (2, length - 1, 1, rot(swing)),
                                 (1, 2, 1, rot(-swing * .5))], seed=seed, painter=wave_face, overlap=.3)


def build(g):
    scalp(g, 6201, side_rows=7, back_rows=8, sideburn=0, part=5)
    hat = ring_shell(g, 6202, side_rows=6, back_rows=8)
    wave_face(hat.top, 6203, 3)
    hat.top.vline(5, 0, 7, "H1")
    # The deep wave swept across the brow from the part.
    taper(g, "brow_wave", (1.4, -8.8, -4.3), (-8, 0, 58), ((3, 4, 1), (1, 2, 1)), seed=6210, painter=wave_face)
    for side, sign in SIDES:
        wave(g, f"{side}_front", (4.5 * sign, -7.6, -3.3), 9 * sign, 3, 6220 + (sign > 0) * 9, axis="x")
        wave(g, f"{side}_back", (4.5 * sign, -7.4, 3.2), 10 * sign, 3, 6240 + (sign > 0) * 9)
    for i, x in enumerate((-2.8, -.9, 1.0, 2.9)):
        wave(g, f"back_{i}", (x, -7.6, 4.55), 10 if i % 2 else -10, 4, 6260 + i * 9)
