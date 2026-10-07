"""Light-Wash Jeans: sun-faded jeans with whiskered thighs, worn with canvas shoes."""
from kit_casual import jeans, shoes

META = {
    "name": "Light-Wash Jeans",
    "gender": "male",
    "description": "Sun-faded light-wash jeans with whiskered thighs and paler knees, over canvas shoes.",
    "tags": ["casual", "modern", "denim"],
}


def build(g):
    jeans(g, "D", 3, seed=10301, fade=1)
    shoes(g, "canvas")
