"""Governess's Book-Belt Kirtle: a high-necked sober kirtle with a white standing collar, a row of
covered buttons and buttoned forearms with white wrist frills, and a broad book-belt: two lesson books
strapped at the right hip and a hornbook primer hanging at the left."""
from kit import body, sleeves
from kit_female import buttons, girdle
from kit_f05 import dangle
from paint import solid

META = {
    "name": "Governess's Book-Belt Kirtle",
    "gender": "female",
    "description": "A high-necked sober kirtle with a white collar, buttoned sleeves and a book-belt hung with two lesson books and a hornbook.",
    "tags": ["scholarly", "tailored", "simple"],
}


def book(box, cover):
    """A closed book: cover on the broad faces and spine, pale page edges on the others."""
    solid(box, cover, "plain", 55285, 2, edge=False)
    box.right.fill("S4"), box.left.fill("S4")
    for face in (box.right, box.left):
        for y in range(face.h):
            face.set(0, y, "S3")
    box.bottom.fill("S3")


def build(g):
    b = body(g, "P", "plain", 55281, base=1)
    buttons(b.front, 4, 1, 7, "P3", step=1, placket="P0")
    for y in range(1, 8):
        b.front.set(3, y, "P2")
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P0"), face.vline(6, 2, 11, "P0")
    for arm in sleeves(g, "P", "plain", 55282, base=1, rows=(0, 11)):
        arm.strip.hline(0, 15, 11, "S4")
        for x in range(0, 16, 2):
            arm.strip.set(x, 10, "S3")                                  # the wrist frill
        arm.front.vline(2, 5, 9, "P0")
        for y in (5, 7, 9):
            arm.front.set(2, y, "M3")                                   # buttoned forearms
    # The white standing collar.
    collar = g.piece("standing_collar", "TORSO", (-4.3, -1.2, -2.3), (9, 2, 5), inflate=.12)
    solid(collar, "S", "plain", 55283, 4, edge=False)
    for face in collar.sides:
        face.hline(0, face.w - 1, 1, "S3")
    # The book-belt.
    belt = girdle(g, "book_belt", 7.6, role="L", base=1, height=2, buckle="M")
    for face in (belt.left, belt.right):
        face.set(1, 1, "M3"), face.set(3, 1, "M3")
    # Two lesson books strapped together at the right hip.
    strap = dangle(g, "book_strap", -2.8, -.6, (1, 2, 1), "L", 2, "leather", top=9.0, seed=55284, edge=False)
    upper = dangle(g, "lesson_book_upper", -2.8, 1.4, (3, 2, 2), "A", 2, top=9.0, seed=55285)
    book(upper, "A")
    lower = dangle(g, "lesson_book_lower", -2.8, 3.4, (3, 2, 2), "L", 2, top=9.0, seed=55286)
    book(lower, "L")
    for bk in (upper, lower):
        for face in (bk.front, bk.back, bk.top, bk.bottom):
            face.vline(1, 0, face.h - 1, "L1")                          # the strap round both books
    upper.front.set(1, 0, "M3")
    # A hornbook primer on its cord at the left hip: a wooden paddle with a horn-covered sheet.
    cord = dangle(g, "hornbook_cord", 2.8, -.6, (1, 2, 1), "L", 3, "plain", top=9.0, seed=55288, edge=False)
    cord.front.set(0, 1, "L2")
    paddle = dangle(g, "hornbook", 2.8, 1.4, (3, 4, 1), "L", 3, "plain", top=9.0, seed=55289, edge=False)
    for y in range(3):
        paddle.front.hline(0, 2, y, "S3")
    paddle.front.set(1, 0, "S4")
    paddle.front.hline(0, 2, 1, "S2")
    paddle.front.hline(0, 2, 3, "L2")
    handle = dangle(g, "hornbook_handle", 2.8, 5.4, (1, 2, 1), "L", 2, "plain", top=9.0, seed=55290, edge=False)
    handle.front.set(0, 1, "L1")
