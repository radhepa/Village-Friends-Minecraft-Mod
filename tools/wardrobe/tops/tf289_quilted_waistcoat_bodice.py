"""Quilted Waistcoat Bodice: a sleeveless quilted waistcoat with bound edges and basque tabs, over a chemise pushed to the elbow."""
from kit_female import checks, chemise, girdle, lozenges, over_panel
from kit_f10 import frills
from paint import solid

META = {
    "name": "Quilted Waistcoat Bodice",
    "gender": "female",
    "description": "A sleeveless diamond-quilted waistcoat hooked up the front, bound in a bright tape and finished with little basque tabs, over a chemise pushed up to the elbow.",
    "tags": ["casual", "work"],
    "covers_waist": True,
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 60120, neckline="round", sleeve_rows=(0, 6))
    for arm in arms:
        arm.front.vline(1, 1, 5, "S2")
    frills(g, "elbow_frill", 4.4, "S", 3)
    j = g.part("jacket")
    for face in (j.front, j.back):
        lozenges(face, 0, 0, 8, 9, "P2", "P1", "P3")                   # diamond quilting, a puff in each
    for face in (j.right, j.left):
        lozenges(face, 0, 2, 4, 7, "P2", "P1", "P3")                   # deep armholes
        face.hline(0, 3, 2, "A2")
    for x in (0, 1, 6, 7):
        j.top.vline(x, 0, 3, "P3")                                     # the shoulder straps
    f = j.front
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2)]:
        f.clear(x, y)                                                  # the V showing the chemise
    for x, y in [(1, 0), (2, 1), (2, 2), (3, 3), (6, 0), (5, 1), (5, 2), (4, 3)]:
        f.set(x, y, "A2")                                              # bound edges
    for y in range(4, 9):
        f.set(3, y, "A1"), f.set(4, y, "A2")
        if y % 2 == 0:
            f.set(3, y, "M3")                                          # hooks and eyes
    for x in (2, 3, 4, 5):
        j.back.set(x, 0, "A2")
    for face in (f, j.back):
        face.vline(0, 0, 2, "A2"), face.vline(7, 0, 2, "A2")             # the armhole binding
    # The bound bottom edge round the waist, enclosing the tabs' hinges.
    edge = girdle(g, "waistcoat_edge", 8.4, role="A", base=2, height=1, buckle=None, texture="plain", wide=True)
    for face in edge.sides:
        for x in range(1, face.w, 2):
            face.set(x, 0, "A1")
    for back in (False, True):
        for i, x in enumerate((-3.15, -1.05, 1.05, 3.15)):
            tab = over_panel(g, f"tab_{'back' if back else 'front'}_{i}", 3, "P", "weave", 60124 + i, 2, width=2,
                             top=9.0, x=x, back=back)
            tab.hline(0, 1, 0, "P1"), tab.set(0, 1, "P3"), tab.set(1, 1, "P1")
            tab.hline(0, 1, 2, "A2")
    # A checked kitchen cloth tucked in at the right hip.
    cloth = g.piece("kitchen_cloth", "TORSO", (-1, 0, 0), (2, 5, 1), pivot=(-3.7, 8.6, -3.45), motion="flap_front")
    solid(cloth, "S", "plain", 60128, 4)
    checks(cloth.front, "S4", "A3", 1, c="A2")
    cloth.front.hline(0, 1, 0, "S3")
    cloth.back.fill("S3")
