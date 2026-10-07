"""Heather V-Neck: a soft heathered tee with a clean V neckline."""
from kit_casual import shirt_body, short_sleeves, v_neck

META = {
    "name": "Heather V-Neck",
    "gender": "male",
    "description": "A soft heathered tee with a clean V neckline and plain short sleeves.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "S", 2, "weave", 11901)
    v_neck(body, "S", 2)
    short_sleeves(g, "S", 2, "weave", 11902, length=4)
