#!/usr/bin/env python3
"""Offline wardrobe previews: a tiny orthographic renderer of the player mesh, its overlay
layers and every 3D piece, using Minecraft's box-UV polygon mapping. Previews are for fast
iteration only; the in-game gametest gallery is the source of truth.

    python tools/wardrobe/preview.py outfits [--palette ROYAL_VELVET] [--out file.png]
    python tools/wardrobe/preview.py hair [--color CHESTNUT]
    python tools/wardrobe/preview.py mix
    python tools/wardrobe/preview.py one --top t01_x --bottom b01_y --hair h01_z
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import wardrobe as W

BODY = W.ROOT / "src/main/resources/assets/villagefriends/textures/body"
SCRATCH = Path("/tmp/claude-0/wardrobe-preview")


def resolve(layer: W.Layer, palette: dict, hair: list[str]) -> np.ndarray:
    out = np.zeros((layer.h, layer.w, 4), np.uint8)
    for y in range(layer.h):
        for x in range(layer.w):
            k = layer.px[y][x]
            if k is None:
                continue
            if k in W.SHADOW_KEYS:
                out[y, x] = (0, 0, 0, W.SHADOW_KEYS[k])
                continue
            hexc = hair[int(k[1])] if k[0] == "H" else palette["ramps"][k[0]][int(k[1])]
            out[y, x] = (*W.hex_rgb(hexc), 255)
    return out


def composite(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    out = base.copy()
    opaque = layer[..., 3] == 255
    out[opaque] = layer[opaque]
    shadow = (layer[..., 3] > 0) & ~opaque
    k = 1 - layer[..., 3:4].astype(np.float32) / 255
    out[..., :3] = np.where(shadow[..., None], (out[..., :3] * k).round(), out[..., :3]).astype(np.uint8)
    return out


def skin_texture(complexion: int, garments: list[W.Garment], palette, hair) -> np.ndarray:
    skin = np.array(Image.open(BODY / f"{complexion}.png").convert("RGBA"))
    for g in garments:
        skin = composite(skin, resolve(g.skin, palette, hair))
    return skin


def layering(top, bottom, hair):
    order = [bottom, top] if not top.meta.get("tucked") else [top, bottom]
    return order + [hair]


# -- geometry ---------------------------------------------------------------------------------
def rot(rx, ry, rz):
    return np.array(W.rot_matrix(rx, ry, rz))


PARTS = [  # name, bone, box origin, size, uv, inflate
    ("head", "HEAD", (-4, -8, -4), (8, 8, 8), (0, 0), 0), ("hat", "HEAD", (-4, -8, -4), (8, 8, 8), (32, 0), .5),
    ("body", "TORSO", (-4, 0, -2), (8, 12, 4), (16, 16), 0), ("jacket", "TORSO", (-4, 0, -2), (8, 12, 4), (16, 32), .25),
    ("rarm", "RIGHT_ARM", (-3, -2, -2), (4, 12, 4), (40, 16), 0), ("rsl", "RIGHT_ARM", (-3, -2, -2), (4, 12, 4), (40, 32), .25),
    ("larm", "LEFT_ARM", (-1, -2, -2), (4, 12, 4), (32, 48), 0), ("lsl", "LEFT_ARM", (-1, -2, -2), (4, 12, 4), (48, 48), .25),
    ("rleg", "RIGHT_LEG", (-2, 0, -2), (4, 12, 4), (0, 16), 0), ("rpa", "RIGHT_LEG", (-2, 0, -2), (4, 12, 4), (0, 32), .25),
    ("lleg", "LEFT_LEG", (-2, 0, -2), (4, 12, 4), (16, 48), 0), ("lpa", "LEFT_LEG", (-2, 0, -2), (4, 12, 4), (0, 48), .25),
]


def cube_quads(origin, size, uv, inflate, scale=(1, 1, 1)):
    """Minecraft ModelPart.Cube polygons: (four vertices, (u1, v1, u2, v2), outward normal)."""
    x, y, z = origin
    w, h, d = size
    g = inflate
    x0, y0, z0, x1, y1, z1 = x - g, y - g, z - g, x + w + g, y + h + g, z + d + g
    sx, sy, sz = scale
    V = [np.array(v) * (sx, sy, sz) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    u, v = uv
    f, f1, f2, f3, f4, f5 = u, u + d, u + d + w, u + d + 2 * w, u + 2 * d + w, u + 2 * d + 2 * w
    f6, f7, f8 = v, v + d, v + d + h
    return [((V[5], V[4], V[0], V[1]), (f1, f6, f2, f7), (0, -1, 0)),
            ((V[2], V[3], V[7], V[6]), (f2, f7, f3, f6), (0, 1, 0)),
            ((V[0], V[4], V[7], V[3]), (f, f7, f1, f8), (-1, 0, 0)),
            ((V[1], V[0], V[3], V[2]), (f1, f7, f2, f8), (0, 0, -1)),
            ((V[5], V[1], V[2], V[6]), (f2, f7, f4, f8), (1, 0, 0)),
            ((V[4], V[5], V[6], V[7]), (f4, f7, f5, f8), (0, 0, 1))]


class Canvas:
    def __init__(self, w, h, bg=(241, 228, 203)):
        self.img = np.zeros((h, w, 3), np.float32) + bg
        self.z = np.full((h, w), np.inf, np.float32)
        self.w, self.h = w, h

    def quad(self, pts, uvs, tex, light):
        """pts: 4 screen points (x, y, depth) in polygon order; uvs: (u1, v1, u2, v2)."""
        p0, p1, p2 = pts[0], pts[1], pts[2]
        es, et = p0[:2] - p1[:2], p2[:2] - p1[:2]
        det = es[0] * et[1] - es[1] * et[0]
        if abs(det) < 1e-6:
            return
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1 = max(0, int(math.floor(min(xs)))), min(self.w - 1, int(math.ceil(max(xs))))
        y0, y1 = max(0, int(math.floor(min(ys)))), min(self.h - 1, int(math.ceil(max(ys))))
        if x0 > x1 or y0 > y1:
            return
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        dx, dy = gx - p1[0], gy - p1[1]
        s = (dx * et[1] - dy * et[0]) / det
        t = (es[0] * dy - es[1] * dx) / det
        inside = (s >= 0) & (s < 1) & (t >= 0) & (t < 1)
        if not inside.any():
            return
        depth = p1[2] + s * (p0[2] - p1[2]) + t * (p2[2] - p1[2])
        u1, v1, u2, v2 = uvs
        tu = np.floor(u1 + s * (u2 - u1) - 1e-4 * np.sign(u2 - u1)).astype(int)
        tv = np.floor(v1 + t * (v2 - v1) - 1e-4 * np.sign(v2 - v1)).astype(int)
        th, tw = tex.shape[:2]
        tu, tv = np.clip(tu, 0, tw - 1), np.clip(tv, 0, th - 1)
        texel = tex[tv, tu]
        zb = self.z[y0:y1 + 1, x0:x1 + 1]
        draw = inside & (texel[..., 3] > 127) & (depth < zb)
        region = self.img[y0:y1 + 1, x0:x1 + 1]
        region[draw] = texel[draw][:, :3] * light
        zb[draw] = depth[draw]


def render(canvas: Canvas, skin: np.ndarray, pieces, cx, cy, scale, yaw, pitch=-12, pose=None, head_only=False):
    """pieces: list of (Piece, texture). pose: optional bone rotations in degrees."""
    pose = pose or {}
    view = rot(pitch, 0, 0) @ rot(0, yaw, 0)
    bones = {}
    for b, pivot in W.BONE_PIVOT.items():
        bones[b] = (np.array(pivot, float), rot(*pose.get(b, (0, 0, 0))))
    items = []
    for name, bone, origin, size, uv, inflate in PARTS:
        items.append((bone, np.zeros(3), np.eye(3), origin, size, uv, inflate, None, skin))
    leg_r = pose.get("RIGHT_LEG", (0, 0, 0))[0]
    leg_l = pose.get("LEFT_LEG", (0, 0, 0))[0]
    for p, tex in pieces:
        rx, ry, rz = p.rotation
        if p.motion == "flap_front":
            rx += min(0, leg_r, leg_l)
        elif p.motion == "flap_back":
            rx += max(0, leg_r, leg_l)
        items.append((p.bone, np.array(p.pivot, float), rot(rx, ry, rz), p.origin, p.size, p.box.u_v,
                      p.inflate, p.scale, tex))
    for bone, ppivot, prot, origin, size, uv, inflate, pscale, tex in items:
        if head_only and bone != "HEAD":
            continue
        bpivot, brot = bones[bone]
        for verts, uvs, normal in cube_quads(origin, size, uv, inflate, pscale or (1, 1, 1)):
            world = [bpivot + brot @ (ppivot + prot @ v) for v in verts]
            n = view @ (brot @ (prot @ np.array(normal, float)))
            if n[2] >= -1e-6:
                continue
            light = 0.58 + 0.30 * max(0, -n[1]) + 0.12 * max(0, -n[2]) + 0.06 * max(0, -n[0])
            pts = [np.array([cx + (view @ wv)[0] * scale, cy + (view @ wv)[1] * scale, (view @ wv)[2]]) for wv in world]
            canvas.quad(pts, uvs, tex, min(1.0, light))


# Box carries its uv origin for the renderer.
W.Box.u_v = property(lambda self: (self.u, self.v))


def figure(canvas, x, y, scale, top, bottom, hair, palette, hair_ramp, complexion=2, yaw=-28, pitch=-10, pose=None, head_only=False):
    skin = skin_texture(complexion, layering(top, bottom, hair), palette, hair_ramp)
    pieces = []
    hidden_waist = top.meta.get("covers_waist")
    for g in (top, bottom, hair):
        tex = resolve(g.extras, palette, hair_ramp)
        for p in g.pieces:
            if hidden_waist and g is bottom and p.id.startswith("waist"):
                continue
            pieces.append((p, tex))
    render(canvas, skin, pieces, x, y, scale, yaw, pitch, pose, head_only)


def label(img: Image.Image, x, y, text, fill=(78, 56, 43)):
    d = ImageDraw.Draw(img)
    w = d.textlength(text)
    d.text((x - w / 2, y), text, fill=fill)


def save(canvas: Canvas, labels, out: Path):
    img = Image.fromarray(canvas.img.clip(0, 255).astype(np.uint8))
    for x, y, text in labels:
        label(img, x, y, text)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["outfits", "hair", "mix", "one", "palettes"])
    ap.add_argument("--palette", default=None)
    ap.add_argument("--color", default="CHESTNUT")
    ap.add_argument("--top"), ap.add_argument("--bottom"), ap.add_argument("--hair")
    ap.add_argument("--out", default=None)
    ap.add_argument("--back", action="store_true")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    garments = W.build_all()
    for g in garments.values():
        errs = g.validate()
        if errs:
            print(g.id, errs[:6])
    palettes, hairs = W.load_palettes(), W.load_hair_colors()
    plist = list(palettes)
    catalog = json.loads((W.TOOL / "outfits.json").read_text())
    tops = [g for g in garments.values() if g.kind == "tops"]
    bottoms = [g for g in garments.values() if g.kind == "bottoms"]
    hair_list = [g for g in garments.values() if g.kind == "hair"]
    pose = {"RIGHT_LEG": (28, 0, 0), "LEFT_LEG": (-28, 0, 0), "RIGHT_ARM": (-25, 0, 0), "LEFT_ARM": (25, 0, 0)} if a.walk else None
    yaw = 152 if a.back else -28
    if a.mode == "outfits":
        outfits = catalog["outfits"]
        cols, cw, ch, sc = 5, 300, 560, 11
        canvas = Canvas(cols * cw, ((len(outfits) + cols - 1) // cols) * ch)
        labels = []
        for i, o in enumerate(outfits):
            pal = palettes[a.palette or plist[i % len(plist)]]
            hair = hair_list[i % len(hair_list)] if hair_list else None
            x, y = (i % cols) * cw + cw // 2, (i // cols) * ch + 170
            figure(canvas, x, y, sc, garments[o["top"]], garments[o["bottom"]], hair, pal,
                   hairs[list(hairs)[i % len(hairs)]]["ramp"], complexion=i % 6, yaw=yaw, pose=pose)
            labels += [(x, y + 360, o["name"]), (x, y + 374, pal["name"])]
        save(canvas, labels, Path(a.out or SCRATCH / f"outfits{'_back' if a.back else ''}{'_walk' if a.walk else ''}.png"))
    elif a.mode == "hair":
        cols, cw, ch, sc = 5, 300, 330, 19
        canvas = Canvas(cols * cw, ((len(hair_list) + cols - 1) // cols) * ch)
        labels = []
        base_top = tops[0] if tops else None
        for i, h in enumerate(hair_list):
            x, y = (i % cols) * cw + cw // 2, (i // cols) * ch + 245
            color = a.color if a.color != "ALL" else list(hairs)[i % len(hairs)]
            figure(canvas, x, y, sc, base_top, bottoms[0], h, palettes[a.palette or plist[0]], hairs[color]["ramp"],
                   complexion=i % 6, yaw=yaw if not a.back else 160, pitch=-8, head_only=True)
            labels.append((x, i // cols * ch + 312, h.meta["name"]))
        save(canvas, labels, Path(a.out or SCRATCH / f"hair{'_back' if a.back else ''}.png"))
    elif a.mode == "mix":
        rng = random.Random(a.seed)
        cols, cw, ch, sc = 6, 250, 470, 10
        canvas = Canvas(cols * cw, 2 * ch)
        labels = []
        pairs = [(t, b) for t in tops for b in bottoms if W.compatible(t, b)]
        for i in range(12):
            t, b = rng.choice(pairs)
            pal = palettes[rng.choice(plist)]
            x, y = (i % cols) * cw + cw // 2, (i // cols) * ch + 110
            figure(canvas, x, y, sc, t, b, rng.choice(hair_list), pal, hairs[rng.choice(list(hairs))]["ramp"],
                   complexion=rng.randrange(6), yaw=yaw, pose=pose)
            labels += [(x, y + 345, t.meta["name"]), (x, y + 358, "+ " + b.meta["name"])]
        save(canvas, labels, Path(a.out or SCRATCH / "mix.png"))
    elif a.mode == "one":
        canvas = Canvas(1200, 760)
        pal = palettes[a.palette or plist[0]]
        t, b, h = garments[a.top], garments[a.bottom], garments[a.hair]
        for j, (yw, ps) in enumerate([(-28, None), (152, None), (-28, {"RIGHT_LEG": (30, 0, 0), "LEFT_LEG": (-30, 0, 0),
                                                                        "RIGHT_ARM": (-25, 0, 0), "LEFT_ARM": (25, 0, 0)})]):
            figure(canvas, 200 + j * 400, 250, 15, t, b, h, pal, hairs[a.color]["ramp"], yaw=yw, pose=ps)
        save(canvas, [], Path(a.out or SCRATCH / f"one_{a.top}.png"))
    elif a.mode == "palettes":
        img = Image.new("RGB", (900, 40 * len(palettes) + 40 * len(hairs)), (241, 228, 203))
        d = ImageDraw.Draw(img)
        for i, (pid, p) in enumerate(palettes.items()):
            d.text((6, i * 40 + 14), p["name"], fill=(60, 40, 30))
            for r, role in enumerate("PSALMK"):
                for s, c in enumerate(p["ramps"][role]):
                    d.rectangle([170 + r * 120 + s * 22, i * 40 + 6, 170 + r * 120 + s * 22 + 20, i * 40 + 34], fill=c)
        off = 40 * len(palettes)
        for i, (cid, c) in enumerate(hairs.items()):
            d.text((6, off + i * 40 + 14), c["name"], fill=(60, 40, 30))
            for s, col in enumerate(c["ramp"]):
                d.rectangle([170 + s * 22, off + i * 40 + 6, 190 + s * 22, off + i * 40 + 34], fill=col)
        out = Path(a.out or SCRATCH / "palettes.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        print(out)


if __name__ == "__main__":
    main()
