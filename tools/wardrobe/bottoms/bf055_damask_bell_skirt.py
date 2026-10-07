"""Damask Bell Skirt: a wide bell-shaped skirt woven with a quiet damask lattice, a pearl hem and gilt pointed shoes."""
from kit_female import lozenges, shoes, skirt, trim

META = {
    "name": "Damask Bell Skirt",
    "gender": "female",
    "description": "A wide bell skirt woven with a quiet damask lattice, edged in pearls, over gilt-toed pointed shoes.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "velvet", 15511, top=9.6, length=12, flare=10, folds=False, gather=False)
    s.paint(lambda f: lozenges(f, 0, 1, f.w, f.h - 1, "P2", "P1", None))
    for face in s.faces:
        face.hline(0, face.w - 1, 0, "P3")
        trim(face, face.h - 1, "pearls", "S4", "M4")
    shoes(g, "pointed", "K", 2, toe="M3")
