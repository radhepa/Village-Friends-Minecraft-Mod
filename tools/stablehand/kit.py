"""Shared helpers for the Stablehand tools: project paths, JSON and PNG bytes, item files, tag and
language merges. Every module in this folder builds `outputs() -> {Path: bytes}` with these, and
`stablehand.py` writes or checks the result.

Merged files (the language file, vanilla tags) are rebuilt from what is on disk plus our entries, so
other tools' keys keep their values and order and a rerun is a no-op.
"""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from item_sprites import raster  # noqa: E402,F401
from tavern.sprites import layered  # noqa: E402,F401

PROJECT = Path(__file__).resolve().parents[2]
RESOURCES = PROJECT / 'src/main/resources'
ASSETS = RESOURCES / 'assets/villagefriends'
DATA = RESOURCES / 'data'
NS = 'villagefriends'
# The data tables Java reads from the classpath (StableTable.load).
TABLES = DATA / 'villagefriends/villagefriends/stablehand'
LANG = ASSETS / 'lang/en_us.json'


def dump(data):
    """2-space JSON with a final newline, the repo's style for generated files."""
    return (json.dumps(data, indent=2) + '\n').encode()


def png_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    return buffer.getvalue()


def item_files(name, image):
    """A flat 16px item: texture, item model and item definition, as the playground sprite does."""
    return {
        ASSETS / f'textures/item/{name}.png': png_bytes(image),
        ASSETS / f'models/item/{name}.json': dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}}),
        ASSETS / f'items/{name}.json': dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}}),
    }


def _read(path):
    return path.read_bytes() if path.exists() else b''


def _endings(raw, text):
    """Keeps the file's own line endings (CRLF stays CRLF)."""
    return text.replace(b'\n', b'\r\n') if b'\r\n' in raw else text


def merge_tag(path, values):
    """A tag file with our values added (set union, sorted), `replace` kept as it was."""
    raw = _read(path)
    data = json.loads(raw.decode('utf-8')) if raw else {'replace': False, 'values': []}
    data['values'] = sorted(set(data.get('values', [])) | set(values))
    return _endings(raw, dump(data))


def merged_lang(names):
    """The language file with our names merged in: other keys keep their values and order (ours are added
    at the end or updated in place), in the file's own style (2-space indent, its line endings)."""
    raw = _read(LANG)
    data = json.loads(raw.decode('utf-8')) if raw else {}
    data.update(names)
    return _endings(raw, dump(data))
