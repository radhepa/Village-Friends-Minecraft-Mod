"""Cream Trousers: plain straight-leg trousers in soft cream."""
from kit_casual import shoes, trousers

META = {
    "name": "Cream Trousers",
    "gender": "male",
    "description": "Plain straight-leg trousers in soft cream, worn with dark shoes.",
    "tags": ["casual", "modern", "simple"],
}


def build(g):
    trousers(g, "S", 3, "weave", 12001)
    shoes(g, "dark")
