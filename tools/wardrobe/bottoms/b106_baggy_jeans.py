"""Baggy Jeans: roomy wide-leg jeans that stack over the shoes, cinched with a long belt."""
from kit_casual import jeans, leather_belt, shoes, stacked_hems
from paint import solid

META = {
    "name": "Baggy Jeans",
    "gender": "male",
    "description": "Roomy wide-leg jeans that stack over the shoes, cinched by a belt with a long tail.",
    "tags": ["casual", "modern", "denim", "relaxed"],
}


def build(g):
    jeans(g, "D", 2, seed=10601, end=9, overlay=True)
    stacked_hems(g, "D", 2)
    leather_belt(g)
    tail = g.piece("waist_belt_tail", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-2.1, 10.2, -2.75))
    solid(tail, "L", "leather", 10602, 2)
    tail.front.set(0, 2, "M3")
    shoes(g, "canvas")
