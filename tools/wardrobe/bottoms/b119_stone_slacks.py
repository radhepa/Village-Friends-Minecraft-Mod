"""Stone Slacks: pressed slacks in a pale stone shade with leather shoes."""
from kit_casual import leather_belt, shoes, trousers

META = {
    "name": "Stone Slacks",
    "gender": "male",
    "description": "Pressed slacks in a pale stone shade with a leather belt and shoes.",
    "tags": ["casual", "modern", "tailored"],
}


def build(g):
    trousers(g, "S", 2, "weave", 11901, crease=True)
    leather_belt(g)
    shoes(g, "leather")
