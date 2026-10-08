#!/usr/bin/env python3
"""Check and preview ONE Village Life module on its own, without compiling the whole pack.

    python tools/animations/vlcheck.py tools/animations/village_life/trades.py
    python tools/animations/vlcheck.py tools/animations/village_life/trades.py --sheet out.png --clips a,b,c --frames 6

Validates the module's clips (the compiler's rules plus the unit/game test limits), reports id
collisions with the rest of the pack, prints a summary, and optionally renders a contact sheet.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

TOOL = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL))
import kit  # noqa: E402
import animations  # noqa: E402

TAG = re.compile(r"(adult|child|smith|guard|social|holding|rain|thunder|cold|morning|day|evening|night|birthday|"
                 r"job:[a-z_]+|personality:[a-z]+|routine:[a-z_]+)")


def run(path: Path):
    kit.CLIPS.clear()
    spec = importlib.util.spec_from_file_location(f"check.{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(kit.CLIPS)


def other_ids(target: Path):
    ids = {}
    for f in sorted((TOOL / "village_life").glob("*.py")):
        if f.resolve() == target.resolve():
            continue
        for m in re.finditer(r"@clip\(\s*\"([a-z0-9_]+)\"", f.read_text(encoding="utf-8")):
            ids[m.group(1)] = f.stem
        for m in re.finditer(r"also=\{([^}]*)\}", f.read_text(encoding="utf-8")):
            for twin in re.findall(r"\"([a-z0-9_]+)\"\s*:", m.group(1)):
                ids[twin] = f.stem
    return ids


def check(clips, target):
    errors = animations.validate(clips)
    others = other_ids(target)
    for c in clips:
        if c.id in others:
            errors.append(f"{c.id}: id already used in {others[c.id]}.py")
        if not re.fullmatch(r"[a-z0-9_]+", c.id):
            errors.append(f"{c.id}: ids are lowercase letters, digits and underscores")
        if not (0.5 < c.length <= 8):
            errors.append(f"{c.id}: length must be over 0.5s and at most 8s")
        data = c.compile()
        for k in data["tracks"].get("root.pos", []):
            x, y, z = k[1:]
            if abs(x) > .55 or abs(z) > .8 or y < -5.5 or y > 6.5:
                errors.append(f"{c.id}: root_pos {x, y, z} at {k[0]}s moves the feet out from under the resident "
                              "(keep |x|<=.55, |z|<=.8, -5.5<=y<=6.5)")
        tags = [t for group in c.require for t in group.split("|")] + list(c.avoid) + list(c.boost)
        errors += [f"{c.id}: unknown tag {t!r}" for t in tags if not TAG.fullmatch(t)]
        if c.trigger == "greet" and not c.require:
            errors.append(f"{c.id}: greetings require an age (adult, child or adult|child)")
        if "," in c.name:
            errors.append(f"{c.id}: clip names never contain commas ({c.name!r})")
    return errors


def sheet(clips, out: Path, frames: int, scale: float, yaw: float):
    compiled = {}
    for c in clips:
        d = c.compile()
        compiled[d["id"]] = d
    # The wardrobe has its own `kit` module; let the preview import that one.
    sys.modules.pop("kit", None)
    spec = importlib.util.spec_from_file_location("animation_preview", TOOL / "preview.py")
    V = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(V)
    P = V.P
    chosen = list(compiled.values())
    for c in chosen:
        c["_tracks"] = {k: V.Track(v) for k, v in c["tracks"].items()}
    who = V.Resident(3)
    sc = scale
    cw, ch = int(150 * sc / 5.2), int(230 * sc / 5.2)
    canvas = P.Canvas(frames * cw + 190, len(chosen) * ch)
    labels = []
    for row, c in enumerate(chosen):
        for col in range(frames):
            t = c["length"] * (col + 1) / (frames + 1)
            V.render_frame(canvas, who, c, t, 190 + col * cw + cw // 2, row * ch + int(70 * sc / 5.2), sc, yaw=yaw)
            labels.append((190 + col * cw + cw // 2, row * ch + ch - 18, f"{t:.2f}s"))
        labels.append((95, row * ch + 100, c["id"]))
        labels.append((95, row * ch + 114, c["trigger"]))
    out.parent.mkdir(parents=True, exist_ok=True)
    P.save(canvas, labels, out)
    print(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--sheet", default=None, help="write a contact sheet PNG here")
    ap.add_argument("--clips", default="", help="comma-separated clip ids for the sheet (default: all)")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--scale", type=float, default=4.0)
    ap.add_argument("--yaw", type=float, default=-30)
    a = ap.parse_args()
    target = Path(a.module)
    clips = run(target)
    errors = check(clips, target)
    print(f"{target.name}: {len(clips)} clips  " + ", ".join(f"{t}={n}" for t, n in sorted(Counter(c.trigger for c in clips).items())))
    for c in clips:
        req = " ".join(c.require)
        print(f"  {c.trigger:11} {c.id:28} {c.length:4.1f}s w={c.weight:<4} {req}")
    if errors:
        print("\nERRORS:")
        print("\n".join("  " + e for e in errors))
    else:
        print("OK: valid")
    if a.sheet:
        chosen = [c for c in clips if not a.clips or c.id in a.clips.split(",")]
        sheet(chosen, Path(a.sheet), a.frames, a.scale, a.yaw)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
