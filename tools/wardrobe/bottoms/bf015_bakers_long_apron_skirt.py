"""Baker's Long Apron Skirt: a wool skirt under a long gathered white apron with a floury print and a tucked cloth."""
from kit_female import gathers, shoes, skirt
from paint import grid, solid

META = {
    "name": "Baker's Long Apron Skirt",
    "gender": "female",
    "description": "A wool skirt under a long gathered white apron with a floury handprint and a striped cloth tucked in.",
    "tags": ["work", "apron", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 11511, top=9.8, length=12)
    s.hem("P1")
    apron = g.piece("apron", "TORSO", (-4.5, 0, 0), (9, 11, 1), pivot=(0, 9.4, -3.05), motion="flap_front")
    solid(apron, "S", "weave", 11512, 4)
    f = apron.front
    gathers(f, "S", 4, 0, 1)
    f.hline(0, 8, 10, "S3")
    grid(f, 1, 5, [".a.a", "aaaa", ".aa."], {"a": "S3"})            # a floury print
    tie = g.piece("waist_apron_tie", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.2, 0), inflate=.05)
    solid(tie, "S", "weave", 11513, 4, edge=False)
    cloth = g.piece("tucked_cloth", "TORSO", (-1, 0, 0), (2, 5, 1), pivot=(3.0, 9.4, -3.25), motion="flap_front")
    solid(cloth, "S", "weave", 11514, 3)
    for y in (1, 3):
        cloth.front.hline(0, 1, y, "A2")
    shoes(g, "shoe", "L", 2)
