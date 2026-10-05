#!/usr/bin/env python3
"""Village Friends wardrobe compiler.

Every hairstyle, top and bottom is one Python module under tools/wardrobe/{hair,tops,bottoms}/.
A module paints pixel art in *key colors* (role + shade) and declares 3D cuboid pieces. The
compiler writes one PNG + JSON per piece of clothing to
src/main/resources/assets/villagefriends/wardrobe/, plus palettes.json, hair_colors.json and
catalog.json. The game resolves key colors through the one palette an outfit owns, so the art
is palette-locked: no garment carries its own RGB.

    python tools/wardrobe/wardrobe.py            # compile everything
    python tools/wardrobe/wardrobe.py --check    # validate and confirm outputs are current
    python tools/wardrobe/wardrobe.py --only t03_arcanist_longcoat
    python tools/wardrobe/preview.py             # offline 3D previews (see preview.py)
"""
from __future__ import annotations

import argparse
import colorsys
import importlib.util
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image

TOOL = Path(__file__).resolve().parent
ROOT = TOOL.parents[1]
OUT = ROOT / "src/main/resources/assets/villagefriends/wardrobe"
KINDS = ("hair", "tops", "bottoms")
KIND_NAME = {"hair": "hair", "tops": "top", "bottoms": "bottom"}

# --------------------------------------------------------------------------------------------
# Key colors. Each opaque authoring pixel names a palette role and one of five shades:
# 0 deep crease/outline, 1 shadow, 2 base, 3 light, 4 highlight. The authoring RGB values only
# make the PNGs readable in an image editor; the game maps them back to (role, shade).
# P primary 60%, S secondary 30%, A accent 10%, L leather, M metal, K ink, H natural hair.
# X1/X2 are translucent shadows that darken whatever is beneath them.
# --------------------------------------------------------------------------------------------
ROLES = "PSALMKH"
KEY_RGB = {
    "P": ["1f2d4d", "2f4673", "44619a", "6585bd", "93b0dc"],
    "S": ["6b5d47", "968566", "c4b28c", "e0d0ab", "f5ebcf"],
    "A": ["4d1519", "78232b", "a8363c", "cc5d57", "eb958e"],
    "L": ["2c1c13", "4a2f20", "6b4630", "8f6444", "b38962"],
    "M": ["39342f", "655b4d", "968870", "c4b594", "eee2c0"],
    "K": ["14100c", "221a14", "2f251d", "3c3026", "4a3c30"],
    "H": ["3a2213", "5c381f", "80522d", "a86f3c", "d09655"],
}
SHADOW_KEYS = {"X1": 46, "X2": 84}  # alpha of a black multiply
KEYS = {f"{r}{i}": KEY_RGB[r][i] for r in ROLES for i in range(5)}


def key_rgba(key: str) -> tuple[int, int, int, int]:
    if key in SHADOW_KEYS:
        return (0, 0, 0, SHADOW_KEYS[key])
    h = KEYS[key]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


RGBA_KEY = {key_rgba(k): k for k in list(KEYS) + list(SHADOW_KEYS)}
if len(RGBA_KEY) != len(KEYS) + len(SHADOW_KEYS):
    raise SystemExit("Key colors must be unique")


def shade(key: str, delta: int) -> str:
    """Same role, clamped shade offset: shade('P2', -1) == 'P1'."""
    if key in SHADOW_KEYS:
        return key
    return f"{key[0]}{max(0, min(4, int(key[1]) + delta))}"


# --------------------------------------------------------------------------------------------
# Palette ramps. Shadows cool and saturate, highlights warm and soften (classic pixel-art
# hue shifting). The compiler bakes the ramps into JSON so Java and the preview agree exactly.
# --------------------------------------------------------------------------------------------
def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c))) for c in rgb)


def _toward(h: float, target: float, amount: float) -> float:
    d = (target - h + 0.5) % 1.0 - 0.5
    return (h + max(-amount, min(amount, d))) % 1.0


def ramp(base: str, dark: float = 1.0, light: float = 1.0) -> list[str]:
    r, g, b = (c / 255 for c in hex_rgb(base))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    tint = min(1.0, s * 4)
    out = []
    for n in (-2, -1, 0, 1, 2):
        if n < 0:
            k = -n
            vv = v * (1 - 0.19 * k * dark)
            ss = min(1.0, s * (1 + 0.14 * k) + (0.035 * k if s > 0.04 else 0))
            hh = _toward(h, 0.68, 0.024 * k * tint)
        elif n > 0:
            vv = min(1.0, v + (1 - v) * 0.30 * n * light + 0.045 * n * light)
            ss = s * (1 - 0.15 * n * light)
            hh = _toward(h, 0.13, 0.016 * n * tint)
        else:
            hh, ss, vv = h, s, v
        out.append(rgb_hex(c * 255 for c in colorsys.hsv_to_rgb(hh, ss, vv)))
    return out


def load_palettes() -> dict:
    src = json.loads((TOOL / "palettes.json").read_text())
    result = {}
    for pid, p in src.items():
        ramps = {}
        for role in "PSALMK":
            spec = p[role]
            if isinstance(spec, list):
                ramps[role] = spec
            else:
                ramps[role] = ramp(spec, **p.get("tuning", {}).get(role, {}))
        result[pid] = {"name": p["name"], "ramps": ramps}
    return result


def load_hair_colors() -> dict:
    src = json.loads((TOOL / "hair_colors.json").read_text())
    return {cid: {"name": c["name"], "ramp": c["ramp"] if "ramp" in c else ramp(c["base"], **c.get("tuning", {}))}
            for cid, c in src.items()}


# --------------------------------------------------------------------------------------------
# Painting surfaces. Every cuboid uses Minecraft's box UV net: top/bottom above, then the four
# sides as one continuous strip (right, front, left, back). Face-local x always runs from the
# viewer's left to right while looking at that face from outside; y runs downward.
# --------------------------------------------------------------------------------------------
class Layer:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.px: list[list[str | None]] = [[None] * w for _ in range(h)]

    def set(self, x: int, y: int, key: str | None):
        if key is not None and key not in KEYS and key not in SHADOW_KEYS:
            raise ValueError(f"Unknown key color {key}")
        self.px[y][x] = key

    def get(self, x: int, y: int):
        return self.px[y][x]


class Face:
    def __init__(self, layer: Layer, x0: int, y0: int, w: int, h: int, name: str):
        self.layer, self.x0, self.y0, self.w, self.h, self.name = layer, x0, y0, w, h, name

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def set(self, x: int, y: int, key: str | None):
        if self.inside(x, y):
            self.layer.set(self.x0 + x, self.y0 + y, key)

    def get(self, x: int, y: int):
        return self.layer.get(self.x0 + x, self.y0 + y) if self.inside(x, y) else None

    def fill(self, key):
        self.rect(0, 0, self.w, self.h, key)

    def rect(self, x, y, w, h, key):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, key)

    def hline(self, x0, x1, y, key):
        for x in range(x0, x1 + 1):
            self.set(x, y, key)

    def vline(self, x, y0, y1, key):
        for y in range(y0, y1 + 1):
            self.set(x, y, key)

    def paint(self, fn):
        """fn(x, y, current) -> key or None (None leaves the pixel unchanged)."""
        for y in range(self.h):
            for x in range(self.w):
                k = fn(x, y, self.get(x, y))
                if k is not None:
                    self.set(x, y, k)

    def recolor(self, fn):
        """fn(key) -> key for every painted pixel."""
        for y in range(self.h):
            for x in range(self.w):
                k = self.get(x, y)
                if k is not None:
                    self.set(x, y, fn(k, x, y))

    def clear(self, x, y):
        self.set(x, y, None)


class Box:
    """Box-UV net of one cuboid of size w*h*d at (u, v) in a layer."""

    def __init__(self, layer: Layer, u: int, v: int, w: int, h: int, d: int):
        self.layer, self.u, self.v, self.w, self.h, self.d = layer, u, v, w, h, d
        self.top = Face(layer, u + d, v, w, d, "top")          # last row touches the front
        self.bottom = Face(layer, u + d + w, v, w, d, "bottom")  # last row touches the front
        self.right = Face(layer, u, v + d, d, h, "right")      # character's right; x: back -> front
        self.front = Face(layer, u + d, v + d, w, h, "front")  # x: character's right -> left
        self.left = Face(layer, u + d + w, v + d, d, h, "left")  # x: front -> back
        self.back = Face(layer, u + 2 * d + w, v + d, w, h, "back")  # x: character's left -> right
        self.strip = Face(layer, u, v + d, 2 * (w + d), h, "strip")
        self.faces = [self.top, self.bottom, self.right, self.front, self.left, self.back]
        self.sides = [self.right, self.front, self.left, self.back]

    @property
    def width(self):  # unfolded net size
        return 2 * (self.w + self.d)

    @property
    def height(self):
        return self.d + self.h

    # Strip coordinates of each side's first column.
    @property
    def sx_front(self):
        return self.d

    @property
    def sx_left(self):
        return self.d + self.w

    @property
    def sx_back(self):
        return 2 * self.d + self.w

    def fill(self, key):
        for f in self.faces:
            f.fill(key)

    def paint(self, fn):
        for f in self.faces:
            f.paint(lambda x, y, cur, f=f: fn(f, x, y, cur))


# Steve (wide-arm) player skin layout: (u, v, w, h, d). Overlays are inflated by the game model.
SKIN_PARTS = {
    "head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8),
    "body": (16, 16, 8, 12, 4), "jacket": (16, 32, 8, 12, 4),
    "right_arm": (40, 16, 4, 12, 4), "right_sleeve": (40, 32, 4, 12, 4),
    "left_arm": (32, 48, 4, 12, 4), "left_sleeve": (48, 48, 4, 12, 4),
    "right_leg": (0, 16, 4, 12, 4), "right_pants": (0, 32, 4, 12, 4),
    "left_leg": (16, 48, 4, 12, 4), "left_pants": (0, 48, 4, 12, 4),
}
ALLOWED_PARTS = {
    "hair": {"head", "hat"},
    "top": {"body", "jacket", "right_arm", "right_sleeve", "left_arm", "left_sleeve"},
    "bottom": {"body", "jacket", "right_leg", "right_pants", "left_leg", "left_pants"},
}
BONES = ("HEAD", "TORSO", "LEFT_ARM", "RIGHT_ARM", "LEFT_LEG", "RIGHT_LEG")
ALLOWED_BONES = {"hair": {"HEAD"}, "top": {"TORSO", "LEFT_ARM", "RIGHT_ARM"},
                 "bottom": {"TORSO", "LEFT_LEG", "RIGHT_LEG"}}
MOTIONS = ("none", "flap_front", "flap_back", "sway")
# Player model bone pivots (model pixels, y down, +x is the character's left).
BONE_PIVOT = {"HEAD": (0, 0, 0), "TORSO": (0, 0, 0), "RIGHT_ARM": (-5, 2, 0), "LEFT_ARM": (5, 2, 0),
              "RIGHT_LEG": (-1.9, 12, 0), "LEFT_LEG": (1.9, 12, 0)}

# Base-face pixels that the Living Eyes model samples or animates over: never paint them.
EYE_ROW = {(x, 12) for x in range(8, 16)} | {(11, 14)}


class Piece:
    def __init__(self, box: Box, pid, bone, origin, size, pivot, rotation, inflate, motion, scale):
        self.box, self.id, self.bone = box, pid, bone
        self.origin, self.size, self.pivot = origin, size, pivot
        self.rotation, self.inflate, self.motion, self.scale = rotation, inflate, motion, scale

    def json(self):
        data = {"id": self.id, "bone": self.bone, "pivot": list(self.pivot), "rotation": list(self.rotation),
                "origin": list(self.origin), "size": list(self.size), "uv": [self.box.u, self.box.v]}
        if self.inflate:
            data["inflate"] = self.inflate
        if self.motion != "none":
            data["motion"] = self.motion
        if self.scale:
            data["scale"] = list(self.scale)
        return data


class Garment:
    EXTRAS_W = 64

    def __init__(self, kind: str, gid: str, meta: dict):
        self.kind, self.id, self.meta = kind, gid, meta
        self.skin = Layer(64, 64)
        self.extras = Layer(self.EXTRAS_W, meta.get("extras_height", 160))
        self.pieces: list[Piece] = []
        self._shelf_x = self._shelf_y = self._shelf_h = 0
        self._parts = {name: Box(self.skin, *spec) for name, spec in SKIN_PARTS.items()}

    def part(self, name: str) -> Box:
        if name not in ALLOWED_PARTS[KIND_NAME[self.kind]]:
            raise ValueError(f"{self.id}: a {self.kind} may not paint {name}")
        return self._parts[name]

    def piece(self, pid: str, bone: str, origin, size, pivot=(0, 0, 0), rotation=(0, 0, 0),
              inflate=0.0, motion="none", scale=None) -> Box:
        if bone not in ALLOWED_BONES[KIND_NAME[self.kind]]:
            raise ValueError(f"{self.id}:{pid} may not attach to {bone}")
        if motion not in MOTIONS:
            raise ValueError(f"{self.id}:{pid} has unknown motion {motion}")
        w, h, d = size
        if min(w, h, d) < 1 or any(int(s) != s for s in size):
            raise ValueError(f"{self.id}:{pid} needs positive integer texture size")
        if inflate < 0:
            raise ValueError(f"{self.id}:{pid} cannot shrink (negative inflate)")
        tw, th = 2 * (w + d), d + h
        if self._shelf_x + tw > self.extras.w:
            self._shelf_x, self._shelf_y, self._shelf_h = 0, self._shelf_y + self._shelf_h + 1, 0
        if tw > self.extras.w or self._shelf_y + th > self.extras.h:
            raise ValueError(f"{self.id}: extras region full at {pid}; raise extras_height")
        box = Box(self.extras, self._shelf_x, self._shelf_y, w, h, d)
        self._shelf_x += tw + 1
        self._shelf_h = max(self._shelf_h, th)
        if any(p.id == pid for p in self.pieces):
            raise ValueError(f"{self.id}: duplicate piece {pid}")
        self.pieces.append(Piece(box, pid, bone, tuple(origin), tuple(size), tuple(pivot), tuple(rotation),
                                 float(inflate), motion, tuple(scale) if scale else None))
        return box

    # -- output -------------------------------------------------------------------------------
    def used_extras_height(self):
        rows = [y for y in range(self.extras.h) if any(self.extras.px[y])]
        return 0 if not rows else ((max(rows) + 16) // 16) * 16

    def image(self) -> Image.Image:
        eh = self.used_extras_height()
        img = Image.new("RGBA", (64, 64 + eh), (0, 0, 0, 0))
        for layer, oy, h in ((self.skin, 0, 64), (self.extras, 64, eh)):
            for y in range(h):
                for x in range(layer.w):
                    k = layer.px[y][x]
                    if k is not None:
                        img.putpixel((x, oy + y), key_rgba(k))
        return img

    def definition(self) -> dict:
        m = self.meta
        data = {"id": self.id, "kind": KIND_NAME[self.kind], "name": m["name"],
                "texture": f"{self.kind}/{self.id}.png", "extrasHeight": self.used_extras_height(),
                "tags": sorted(m.get("tags", [])), "requires": sorted(m.get("requires", [])),
                "rejects": sorted(m.get("rejects", [])), "pieces": [p.json() for p in self.pieces]}
        if self.kind == "tops":
            data["tucked"] = bool(m.get("tucked", False))
            data["coversWaist"] = bool(m.get("covers_waist", False))
        if "description" in m:
            data["description"] = m["description"]
        return data

    # -- validation ---------------------------------------------------------------------------
    def validate(self):
        errors = []
        kind = KIND_NAME[self.kind]
        allowed = set()
        for name in ALLOWED_PARTS[kind]:
            u, v, w, h, d = SKIN_PARTS[name]
            b = Box(self.skin, u, v, w, h, d)
            for f in b.faces:
                allowed |= {(f.x0 + x, f.y0 + y) for y in range(f.h) for x in range(f.w)}
        for y in range(64):
            for x in range(64):
                k = self.skin.px[y][x]
                if k is None:
                    continue
                if (x, y) not in allowed:
                    errors.append(f"skin pixel outside {kind} regions at {x},{y}")
                if kind != "hair" and k[0] == "H":
                    errors.append(f"natural hair key on a garment at {x},{y}")
                if kind == "hair":
                    if (x, y) in EYE_ROW:
                        errors.append(f"hair paints the protected eye row at {x},{y}")
                    if 8 <= x < 16 and 8 <= y < 16 and y > 8 and 9 <= x <= 14 and k not in SHADOW_KEYS:
                        errors.append(f"hair paints opaque face pixel {x},{y}")
                    # The hat layer sits in front of the animated lash/eye planes: a fringe may
                    # reach the brows (rows 0-2) but only the outer columns may fall lower.
                    if 40 <= x < 48 and 11 <= y < 16 and 1 <= x - 40 <= 6:
                        errors.append(f"hair hat-layer covers eyes/nose/mouth at {x},{y}")
        for p in self.pieces:
            if kind == "hair":
                lo, hi = world_bounds(p)
                if lo[2] < -4.1 and lo[0] < 3 and hi[0] > -3 and hi[1] > -5.02 and lo[1] < 0:
                    errors.append(f"piece {p.id} hangs over the eyes/nose/mouth")
            for f in p.box.faces:
                for y in range(f.h):
                    for x in range(f.w):
                        k = f.get(x, y)
                        if k is None:
                            errors.append(f"piece {p.id} has an unpainted {f.name} texel {x},{y}")
                            break
                        if kind != "hair" and k[0] == "H":
                            errors.append(f"piece {p.id} uses hair keys")
                    else:
                        continue
                    break
        if kind == "hair" and not any(p.size for p in self.pieces):
            errors.append("hair needs volumetric pieces")
        limit = 504 if kind == "hair" else 512   # the kind's shared slot in the game's 256x512 atlas
        if self.used_extras_height() > limit:
            errors.append(f"3D pieces need {self.used_extras_height()} rows; the {kind} slot holds {limit}")
        return errors


def rot_matrix(rx, ry, rz):
    """Minecraft PartPose rotation order: Z * Y * X applied to a column vector (ZYX intrinsic)."""
    ax, ay, az = (math.radians(a) for a in (rx, ry, rz))
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    X = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Y = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Z = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]

    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mul(mul(Z, Y), X)


def piece_corners(p: Piece):
    """Bone-local corners of a piece, including pivot, rotation, scale and inflation."""
    w, h, d = p.size
    sx, sy, sz = p.scale or (1, 1, 1)
    ox, oy, oz = p.origin
    g = p.inflate
    m = rot_matrix(*p.rotation)
    corners = []
    for cx in (ox - g, ox + w + g):
        for cy in (oy - g, oy + h + g):
            for cz in (oz - g, oz + d + g):
                v = (cx * sx, cy * sy, cz * sz)
                r = [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]
                corners.append((r[0] + p.pivot[0], r[1] + p.pivot[1], r[2] + p.pivot[2]))
    return corners


def world_bounds(p: Piece):
    c = piece_corners(p)
    return [min(v[i] for v in c) for i in range(3)], [max(v[i] for v in c) for i in range(3)]


# --------------------------------------------------------------------------------------------
# Module loading and compilation.
# --------------------------------------------------------------------------------------------
def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"wardrobe_{path.parent.name}_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(TOOL))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(TOOL))
    return module


def build(kind: str, path: Path) -> Garment:
    module = load_module(path)
    g = Garment(kind, path.stem, dict(module.META))
    module.build(g)
    return g


def sources(kind: str):
    return sorted(p for p in (TOOL / kind).glob("*.py") if not p.name.startswith("_"))


def build_all(only=None):
    out = {}
    for kind in KINDS:
        for path in sources(kind):
            if only and path.stem not in only:
                continue
            out[path.stem] = build(kind, path)
    return out


def png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def json_text(data) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def catalog(garments: dict) -> dict:
    templates = json.loads((TOOL / "outfits.json").read_text())
    data = {"schemaVersion": 1, "keys": {k: "#" + v for k, v in KEYS.items()},
            "shadowKeys": SHADOW_KEYS,
            "hair": [g.id for g in garments.values() if g.kind == "hair"],
            "tops": [g.id for g in garments.values() if g.kind == "tops"],
            "bottoms": [g.id for g in garments.values() if g.kind == "bottoms"],
            "outfits": templates["outfits"], "professions": templates["professions"]}
    return data


def compatible(top: Garment, bottom: Garment) -> bool:
    t, b = top.meta, bottom.meta
    tt, bt = set(t.get("tags", [])), set(b.get("tags", []))
    if set(t.get("rejects", [])) & bt or set(b.get("rejects", [])) & tt:
        return False
    if t.get("requires") and not set(t["requires"]) & bt:
        return False
    if b.get("requires") and not set(b["requires"]) & tt:
        return False
    return True


def validate_catalog(garments: dict, data: dict) -> list[str]:
    errors = []
    by_id = garments
    tops = [g for g in garments.values() if g.kind == "tops"]
    bottoms = [g for g in garments.values() if g.kind == "bottoms"]
    for o in data["outfits"]:
        for field, kind in (("top", "tops"), ("bottom", "bottoms")):
            if o[field] not in by_id or by_id[o[field]].kind != kind:
                errors.append(f"outfit {o['id']} names unknown {field} {o[field]}")
        if not errors and not compatible(by_id[o["top"]], by_id[o["bottom"]]):
            errors.append(f"outfit {o['id']} pairs incompatible pieces")
    outfit_ids = {o["id"] for o in data["outfits"]}
    worn = set()
    for job, ids in data["professions"].items():
        for oid in ids:
            if oid not in outfit_ids:
                errors.append(f"profession {job} names unknown outfit {oid}")
            worn.add(oid)
    for oid in sorted(outfit_ids - worn):
        errors.append(f"outfit {oid} is not worn by any profession")
    for top in tops:
        n = sum(compatible(top, b) for b in bottoms)
        if n == 0:
            errors.append(f"top {top.id} pairs with no bottom")
    for b in bottoms:
        if not any(compatible(t, b) for t in tops):
            errors.append(f"bottom {b.id} pairs with no top")
    return errors


def outputs(garments: dict, full: bool) -> dict[Path, bytes]:
    files = {}
    for g in garments.values():
        files[OUT / g.kind / f"{g.id}.png"] = png_bytes(g.image())
        files[OUT / g.kind / f"{g.id}.json"] = json_text(g.definition()).encode()
    if full:
        files[OUT / "palettes.json"] = json_text({"schemaVersion": 1, "palettes": load_palettes()}).encode()
        files[OUT / "hair_colors.json"] = json_text({"schemaVersion": 1, "colors": load_hair_colors()}).encode()
        files[OUT / "catalog.json"] = json_text(catalog(garments)).encode()
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate and fail if outputs are stale")
    ap.add_argument("--only", nargs="*", help="compile only these ids")
    args = ap.parse_args(argv)
    garments = build_all(set(args.only) if args.only else None)
    errors = []
    for g in garments.values():
        errors += [f"{g.id}: {e}" for e in g.validate()]
    full = not args.only
    if full:
        errors += validate_catalog(garments, catalog(garments))
        palettes = set(load_palettes())
        expected = {"WASHED_INDIGO_AND_CREAM", "FOREST_AND_HEARTH", "SCHOLARLY_PLUM", "DESERT_SUN", "ROYAL_VELVET",
                    "RUSTIC_TWEED", "TANNER_AMBER", "WINTER_TUNDRA", "SAGE_AND_TERRACOTTA", "ASH_AND_TEAL"}
        if palettes != expected:
            errors.append(f"palettes.json must define exactly {sorted(expected)}")
    if errors:
        print("\n".join(errors))
        return 1
    files = outputs(garments, full)
    if args.check:
        stale = [p for p, data in files.items() if not p.exists() or p.read_bytes() != data]
        if full:
            known = set(files)
            stale += [p for kind in KINDS for p in (OUT / kind).glob("*") if p not in known]
        if stale:
            print("Stale wardrobe outputs:\n" + "\n".join(str(p.relative_to(ROOT)) for p in stale))
            return 1
        print(f"Wardrobe current: {len(garments)} pieces")
        return 0
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    if full:
        known = set(files)
        for kind in KINDS:
            for p in (OUT / kind).glob("*"):
                if p not in known:
                    p.unlink()
    print(f"Compiled {len(garments)} wardrobe pieces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
