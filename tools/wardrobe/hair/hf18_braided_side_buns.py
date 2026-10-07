"""Braided Side Buns: centre-parted, each half plaited and coiled into a bun over the ear."""
from anime import ring_shell
from anime_female import braided_bun, plait_along, strand, SIDES
from paint import scalp

META = {"name": "Braided Side Buns", "gender": "female",
        "description": "A centre part with each side plaited and coiled into a neat bun over the ear."}


def build(g):
    scalp(g, 6801, side_rows=8, back_rows=8, sideburn=0, part=3)
    head = g.part("head")
    head.back.vline(3, 0, 7, "H0"), head.back.vline(4, 0, 7, "H1")
    hat = ring_shell(g, 6802, side_rows=4, back_rows=6)
    hat.top.vline(3, 0, 7, "H1"), hat.back.vline(3, 0, 5, "H1")
    for side, sign in SIDES:
        strand(g, f"{side}_curtain", (.3 * sign, -8.75, -4.35), (-6, 0, 60 * -sign), ((2, 4), (1, 1)), 1, 6810 + (sign > 0), ring=None)
        strand(g, f"{side}_cover", (4.45 * sign, -8.0, .4), (0, 0, -6 * sign), ((1, 4),), 7, 6812 + (sign > 0))
        strand(g, f"{side}_wisp", (4.35 * sign, -6.4, -3.6), (0, 0, -4 * sign), ((1, 4), (1, 2)), 1, 6814 + (sign > 0))
        # The plait runs from the nape up behind the ear and coils into the bun.
        plait_along(g, f"{side}_lead", [(2.0 * sign, -1.6, 4.9), (4.0 * sign, -2.4, 3.9), (5.1 * sign, -3.0, 2.6)], spacing=1.8,
                    seed=6820 + (sign > 0) * 5)
        braided_bun(g, f"{side}_bun", (5.15 * sign, -3.9, .9), (0, 0, 90 * sign), (4, 2, 4), seed=6830 + (sign > 0))
