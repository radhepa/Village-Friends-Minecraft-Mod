# Editing the plains village

Plains villages are assembled procedurally by Minecraft's jigsaw system from about sixty independent templates: three town centres, a street kit, six guaranteed civic buildings, homes, trade workshops, farms and small decorations. Every building is still **one independent file**, and replacing one never requires Java edits.

## How a village is put together

```text
town centre (random of 3, random rotation)
 ├─ 4 large + 4 small civic slots  → buildings/<role> pools (always placed first)
 └─ 4 exits → plains/avenues → plains/streets … (fallback plains/street_ends)
                                  └─ lot jigsaws → plains/lots (fallback plains/lots_outer)
```

- **Town centres** (`central_plaza`, `plaza_green`, `plaza_market`) are 33×33 squares. In pinwheel order each side has a large slot (≤ 17 wide), a street exit and a small slot (≤ 11 wide). Slots have selection priority 5, so the tavern, garrison, workshop, chapel, apothecary and library are placed before any street can take their space. Each centre assigns the roles to different sides; the painter's easel, the bard's music stand, the notice board, benches and the bell live in the square.
- **Streets** are terrain-matching, so roads follow the ground column by column. The kit has straights, S-bends, quarter turns, tees, a fork, a crossroads and a small well square. Streets offer `lot` jigsaws on their outer edges every few blocks.
- **Street ends** are used when a street can't continue or the depth runs out: a path that fades into grass, a lamp-and-bench end, or a timber gatehouse with palisade wings.
- **Lots** choose from homes, trade workshops, a few trees/decorations and `empty` gaps. Streets at the maximum depth only use `plains/lots_outer`, so fields, paddocks and orchards gather on the outskirts.
- `structure_void` cells keep the world's own ground, so yards and verges keep their natural grass. Processors add worn road patches, plank bridges where a road crosses water, and mossy/cracked stone on buildings.

`tools/village_layout.json` holds the pools, weights, fallbacks, processors, depth (6), maximum distance (100), biomes and placement.

## Where buildings come from

| Path | Purpose |
|---|---|
| `tools/village_design/buildings/*.py` | Design programs. Each module exposes `DESIGNS = {name: function}`. |
| `tools/village_design/kit.py`, `parts.py`, `roads.py` | Shared drawing helpers: block states, timber walls, roofs, windows, chimneys, furniture, trees, roads. |
| `tools/village_blueprints/<name>.json` | Compiled layered blueprint, one per template. This is what the structure compiler reads. |
| `tools/create_village_structures.py` | Compiles blueprints into NBT, pools, processors and the catalog. Keep geometry out of it. |

`python tools/design_village.py [names…]` runs designs and writes their blueprints. Each blueprint records its design source and a checksum. If a blueprint was edited by hand afterwards, the design script leaves it alone unless `--force` is given, so hand edits are never silently lost.

The kit fills in states Minecraft would normally derive from neighbours (fence, pane and wall connections, wall posts, stair corners) because jigsaw pieces are placed with a known shape. It also checks every door has two clear blocks on both sides and measures each recorded bedroom by flood fill.

## Improve one building

1. Edit its design function (for example `tavern()` in `buildings/civic.py`), or hand-edit `tools/village_blueprints/tavern.json`.
2. `python tools/design_village.py tavern --preview` writes the blueprint and isometric previews in `build/previews` (needs Pillow).
3. `python tools/create_village_structures.py --check`, then `python tools/create_village_structures.py --only tavern`.
4. `gradlew.bat build`, then `gradlew.bat runClientGameTest -PstructuresOnly`.

To look at it in Minecraft, run `gradlew.bat runClientGameTest -PvillageGallery -Pgallery=tavern,cottage_oak -PgalleryVillages=2`. The gallery places the listed templates and whole villages on a superflat world and saves screenshots to `build/run/clientGameTest/screenshots`. It is a development aid outside the regression suite.

## Lot contract (anything in a `buildings/…` or lot pool)

- Exactly one `minecraft:jigsaw` named `villagefriends:building_entrance` at **`[x, 1, 0]`** on the north edge, orientation `north_up`, pool `minecraft:empty`, final state `minecraft:air`, joint `aligned`. Its X can be anywhere along the front.
- Size 3–32 in each dimension. Civic slot buildings: large slots ≤ 17 wide, small slots ≤ 11 wide, with at most 8 (large) or 5 (small) blocks either side of the entrance. `slot_widths` in the layout makes the compiler check this. Depth is free.
- Y=0 is ground level. Raised floors stand on Y=1 with a step up to the door. Give the entrance a path at Y=0.
- Doors need two clear blocks on both sides. Beds are matched foot/head pairs. Homes need at least one enclosed bedroom recorded with `b.room(name, probe_cell)`.
- Keep profession workstations and residents in their building when improving it. Plaza templates must keep `villagefriends:town_start`, the easel, music stand, painter and bard.

## Replace or add variants

To swap a building, change its pool entry in `village_layout.json` and run the full generator (without `--only`). To add a variant, add another entry with a positive weight. The catalog derives required pools from `required_pools`, so tests accept replacements without hard-coded names. Every blueprint must be referenced by some pool. The compiler deletes stale NBT and pool files.

Balance a layout before testing in Minecraft:

```text
python tools/village_design/simulate.py --seeds 300 --map 4 --out build
```

The simulation imitates jigsaw assembly on flat ground. It reports piece and resident counts, how often each template appears, and whether a required building ever went missing. `--map` draws top-down plans. Minecraft remains the authority.

Building changes affect newly generated chunks only; existing villages are saved blocks. Data packs can still override any pool, processor list or template.
