"""Pocket Tee: a heavyweight crew-neck tee with a single patch pocket on the chest."""
from kit_casual import chest_pocket, plain_tee

META = {
    "name": "Pocket Tee",
    "gender": "male",
    "description": "A heavyweight crew-neck tee with one patch pocket over the heart.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = plain_tee(g, "P", 1, seed=11801, texture="twill")
    chest_pocket(body.front, "P", 1, x0=5, y0=3)
