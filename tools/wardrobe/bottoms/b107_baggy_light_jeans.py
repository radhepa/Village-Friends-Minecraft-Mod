"""Baggy Light Jeans: wide light-wash jeans with a carpenter loop and deep turn-ups."""
from kit_casual import jeans, rolled_hems, shoes
from paint import solid

META = {
    "name": "Baggy Light Jeans",
    "gender": "male",
    "description": "Wide light-wash jeans with a carpenter's loop on the thigh and deep turned-up cuffs.",
    "tags": ["casual", "modern", "denim", "relaxed"],
}


def build(g):
    jeans(g, "D", 3, seed=10701, fade=1, overlay=True)
    rolled_hems(g, "D", 3, y=7.8, inflate=.3)
    loop = g.piece("left_hammer_loop", "LEFT_LEG", (0, 0, -.5), (1, 3, 1), pivot=(2.2, 3.0, 0))
    solid(loop, "D", "twill", 10702, 3)
    loop.left.set(0, 0, "M3")
    shoes(g, "dark")
