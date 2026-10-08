#!/usr/bin/env python3
"""Village Friends resident animation pack compiler.

Each pack is a folder of Python modules under tools/animations/<pack>/ whose clips are keyed with
kit.py. The compiler writes one JSON file per pack to
src/main/resources/assets/villagefriends/resident_animations/<pack>.json, which the game loads
(resource packs can add or replace these files). Never hand-edit the compiled JSON.

    python tools/animations/animations.py              # compile every pack
    python tools/animations/animations.py --check      # validate and confirm outputs are current
    python tools/animations/animations.py --list       # print every clip with its trigger
    python tools/animations/preview.py sheet           # offline contact sheet (see preview.py)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parent
ROOT = TOOL.parents[1]
OUT = ROOT / "src/main/resources/assets/villagefriends/resident_animations"
sys.path.insert(0, str(TOOL))
import kit  # noqa: E402

PACKS = {
    "village_life": {
        "name": "Village Life",
        "description": "The first resident animation pack: everyday idles, hobbies for every personality, "
                       "work for every profession, greetings, conversations, reactions, weather, children's play and games.",
        "modules": ["everyday", "hobbies", "work", "social", "reactions", "weather", "children",
                    "moments", "pastimes", "trades", "crafts", "company", "chatter", "feelings", "skies", "playtime",
                    "guards", "party", "pets", "games"],
    },
    "tavern": {
        "name": "Tavern",
        "description": "Residents at the tavern: sitting, eating, drinking, toasting, talking across the table, "
                       "listening to the bard, leaning on the bar.",
        "modules": ["seated", "dining", "chat", "bar"],
    },
}
MAX_ROT, MAX_POS = 400, 12


# Residents follow a daily routine (Routine.java): during working hours they mostly practice their
# trade, during their free hour their hobby. Clips from these modules are boosted for that part of the day.
WORK_HOURS = {"routine:work": 3.0, "routine:prayer": 3.0, "routine:night_watch": 2.0}
FREE_HOUR = {"routine:hobby": 4.0, "routine:rain_walk": 1.5}
# At a birthday party the party clips (weights 5-8) must outweigh a resident's ~150 of everyday idle weight.
PARTY = {"routine:party": 5.0}
ROUTINE_BOOSTS = {"work": WORK_HOURS, "trades": WORK_HOURS, "crafts": WORK_HOURS, "guards": WORK_HOURS,
                  "hobbies": FREE_HOUR, "pastimes": FREE_HOUR, "party": PARTY}


def load(pack: str):
    kit.CLIPS.clear()
    for name in PACKS[pack]["modules"]:
        before = len(kit.CLIPS)
        path = TOOL / pack / f"{name}.py"
        spec = importlib.util.spec_from_file_location(f"{pack}.{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for c in kit.CLIPS[before:]:
            if c.trigger == "idle":
                for tag, factor in ROUTINE_BOOSTS.get(name, {}).items():
                    c.boost.setdefault(tag, factor)
    return list(kit.CLIPS)


def validate(clips) -> list[str]:
    errors, seen = [], set()
    for c in clips:
        if c.id in seen:
            errors.append(f"duplicate clip {c.id}")
        seen.add(c.id)
        data = c.compile()
        if not data["tracks"]:
            errors.append(f"{c.id}: no keys")
        for channel, keys in data["tracks"].items():
            limit = 1 if channel == "eyes.lid" else MAX_POS if channel.endswith(".pos") or channel == "eyes.look" else MAX_ROT
            for k in keys:
                if any(abs(v) > limit for v in k[1:]):
                    errors.append(f"{c.id}: {channel} value out of range at {k[0]}s")
            if channel == "eyes.lid" and any(k[1] < 0 for k in keys):
                errors.append(f"{c.id}: eyelids cannot open wider than rest")
        a, b = c.blend
        if a + b > c.length:
            errors.append(f"{c.id}: blends longer than the clip")
    return errors


def build(pack: str) -> str:
    clips = load(pack)
    errors = validate(clips)
    if errors:
        raise SystemExit("\n".join(errors))
    meta = PACKS[pack]
    # One line per track keeps the file compact and readable in diffs.
    lines = ["{", '"format": 1,', f'"name": {json.dumps(meta["name"])},', f'"description": {json.dumps(meta["description"])},',
             '"clips": [']
    compiled = [c.compile() for c in clips]
    for i, data in enumerate(compiled):
        tracks = data.pop("tracks")
        head = json.dumps(data, separators=(", ", ": "))[:-1]
        body = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, separators=(',', ':'))}" for k, v in tracks.items())
        lines.append(f"{head}, \"tracks\": {{\n{body}\n}}}}" + ("," if i < len(compiled) - 1 else ""))
    lines += ["]", "}"]
    text = "\n".join(lines) + "\n"
    json.loads(text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    stale = []
    for pack in PACKS:
        text = build(pack)
        out = OUT / f"{pack}.json"
        if a.list:
            for c in load(pack):
                print(f"{c.trigger:12} {c.id:24} {c.length:4.1f}s  {c.name}")
        if a.check:
            if not out.exists() or out.read_text(encoding="utf-8") != text:
                stale.append(out)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
        print(f"{out.relative_to(ROOT)}: {len(json.loads(text)['clips'])} clips")
    if stale:
        raise SystemExit("Stale animation packs (run tools/animations/animations.py): " + ", ".join(map(str, stale)))
    if a.check:
        print("Animation packs are valid and current.")


if __name__ == "__main__":
    main()
