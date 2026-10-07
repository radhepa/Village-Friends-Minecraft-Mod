"""Town Crier's Bell Coat: a brass-buttoned coat with a short cape, a livery armband, a handbell and a proclamation scroll."""
from kit import belt, body, sleeves
from kit_male import blk, buttons, shoulder_cape

META = {
    "name": "Town Crier's Bell Coat",
    "gender": "male",
    "description": "A town crier's coat with big brass buttons, a short shoulder cape, a badged livery armband, a handbell and a scroll.",
    "tags": ["fancy", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 6801)
    b.front.vline(3, 0, 11, "P0"), b.front.vline(4, 0, 11, "P3")
    buttons(b.front, 2, 1, 9, 3, "M4"), buttons(b.front, 5, 1, 9, 3, "M4")
    sleeves(g, "P", "twill", 6802, rows=(0, 10), cuff="A2")
    band = g.part("left_sleeve")
    for y in (2, 3):
        band.strip.hline(0, band.strip.w - 1, y, "A2")
    band.left.set(1, 2, "M4"), band.left.set(2, 3, "M3")                 # livery badge
    cape = shoulder_cape(g, "crier_cape", "P", "twill", 6803, length=2, width=11)
    for face in cape.sides:
        face.hline(0, face.w - 1, 1, "A2")
    belt(g, "belt", 9.4, height=1)
    blk(g, "handbell_grip", (-2.8, 9.8, -2.8), (1, 2, 1), "L", 3, "plain", 6804)
    bell = blk(g, "handbell", (-2.8, 11.6, -2.8), (2, 2, 2), "M", 3, "smooth", 6805)
    bell.bottom.fill("M0")
    scroll = blk(g, "proclamation", (2.8, 8.2, -2.75), (1, 4, 1), "S", 4, "plain", 6806, rotation=(0, 0, 10))
    scroll.strip.hline(0, scroll.strip.w - 1, 1, "A2")
