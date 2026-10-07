"""Charcoal Slacks: pressed charcoal dress slacks with sharp creases and dark shoes."""
from kit_casual import leather_belt, shoes, trousers

META = {
    "name": "Charcoal Slacks",
    "gender": "male",
    "description": "Pressed charcoal dress slacks with sharp creases, a slim belt and dark shoes.",
    "tags": ["casual", "modern", "tailored", "slim"],
}


def build(g):
    trousers(g, "K", 3, "weave", 11001, crease=True)
    leather_belt(g, "K", 1, "M")
    shoes(g, "dark")
