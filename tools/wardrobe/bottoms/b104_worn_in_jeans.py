"""Worn-In Jeans: well-loved jeans with faded knees, a frayed knee tear and turned-up cuffs."""
from kit_casual import jeans, leather_belt, rolled_hems, shoes

META = {
    "name": "Worn-In Jeans",
    "gender": "male",
    "description": "Well-loved jeans with faded knees, one frayed knee, turned-up cuffs and a leather belt.",
    "tags": ["casual", "modern", "denim", "rugged"],
}


def build(g):
    legs, body = jeans(g, "D", 2, seed=10401, fade=2)
    right = legs[0].front
    right.hline(0, 2, 5, "S4"), right.set(1, 6, "S3")   # frayed threads across one knee
    rolled_hems(g, "D", 3, y=8.4)
    leather_belt(g)
    shoes(g, "boot")
