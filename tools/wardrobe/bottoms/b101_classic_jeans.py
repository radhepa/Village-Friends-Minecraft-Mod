"""Classic Jeans: straight-leg five-pocket jeans with gold stitching and a leather belt."""
from kit_casual import jeans, leather_belt, shoes

META = {
    "name": "Classic Jeans",
    "gender": "male",
    "description": "Straight-leg five-pocket jeans with copper rivets, gold stitching, a leather belt and lace-up shoes.",
    "tags": ["casual", "modern", "denim"],
}


def build(g):
    jeans(g, "D", 2, seed=10101)
    leather_belt(g)
    shoes(g, "leather")
