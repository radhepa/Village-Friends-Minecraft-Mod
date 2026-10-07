"""Black Jeans: five-pocket jeans in washed black with tonal grey stitching."""
from kit_casual import jeans, shoes

META = {
    "name": "Black Jeans",
    "gender": "male",
    "description": "Five-pocket jeans in washed black, tonal stitching and dark shoes.",
    "tags": ["casual", "modern", "denim"],
}


def build(g):
    jeans(g, "K", 2, seed=10501, stitch="K4")
    shoes(g, "dark")
