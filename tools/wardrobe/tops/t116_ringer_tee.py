"""Ringer Tee: a pale tee with contrast bands at the neck and sleeve hems."""
from kit_casual import crew_neck, shirt_body, short_sleeves

META = {
    "name": "Ringer Tee",
    "gender": "male",
    "description": "A pale crew-neck tee with a contrast ring at the neck and around both sleeve hems.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "S", 3, "plain", 11601)
    crew_neck(body, "S", 3, rib="A2")
    body.front.set(3, 1, "A1"), body.front.set(4, 1, "A1")
    short_sleeves(g, "S", 3, "plain", 11602, length=4, band="A2")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 3, "A1")
