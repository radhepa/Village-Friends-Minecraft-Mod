"""Slim Dark Jeans: slim jeans in a deep rinse, with dark shoes."""
from kit_casual import jeans, shoes

META = {
    "name": "Slim Dark Jeans",
    "gender": "male",
    "description": "Slim five-pocket jeans in a deep, even rinse, worn with dark shoes.",
    "tags": ["casual", "modern", "denim", "slim"],
}


def build(g):
    jeans(g, "D", 1, seed=10201, stitch="D3")
    shoes(g, "dark")
