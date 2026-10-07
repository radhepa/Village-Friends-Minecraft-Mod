"""Pleated Trousers: double-pleated trousers with turn-ups and a slim belt."""
from kit_casual import leather_belt, rolled_hems, shoes, trousers

META = {
    "name": "Pleated Trousers",
    "gender": "male",
    "description": "Double-pleated trousers with a high waist, deep turn-ups and a slim belt.",
    "tags": ["casual", "modern", "tailored"],
}


def build(g):
    legs, body = trousers(g, "P", 1, "weave", 11701, crease=True)
    for leg in legs:
        leg.front.vline(1, 0, 2, "P0"), leg.front.vline(2, 0, 1, "P0")   # pleats folding into the crease
    rolled_hems(g, "P", 2, y=8.4, texture="weave")
    leather_belt(g)
    shoes(g, "leather")
