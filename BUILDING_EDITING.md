# Editing or replacing one Village Friends building

The buildings are intentionally basic starting layouts. **Each building has an independent JSON blueprint**, and each building role has a separate jigsaw pool. Claude can edit one building without touching Java, other buildings, or village placement.

## Fastest workflow: keep the building's ID

1. Edit its file in `tools/village_blueprints/`, for example `tavern.json`, `garrison.json`, `family_house.json` or `cottage_oak.json`.
2. Validate with `python tools/create_village_structures.py --check`.
3. Regenerate only that building with `python tools/create_village_structures.py --only tavern`.
4. Run `gradlew.bat build`, then `gradlew.bat runClientGameTest -PstructuresOnly` for Minecraft validation.

`--only tavern` writes `src/main/resources/data/villagefriends/structure/village/tavern.nbt` and refreshes the room catalog. It leaves the other NBT templates, pools and natural placement unchanged. The filename determines the template ID; keeping it preserves the pool's existing reference.

## Blueprint format

`size` is `[width, height, depth]`. Coordinates are **X east, Y up, Z south**, starting at zero. `layers` contains one object per Y level. Each object's `rows` run from north to south (increasing Z); each character within a row runs west to east (increasing X). One character represents one complete block state from `palette`. `.` is real air, which clears terrain/foliage inside the lot.

Palette entries use Minecraft IDs and optional state properties, for example:

```json
"A": {"id": "minecraft:oak_planks"},
"B": {"id": "minecraft:glass"},
"C": {"id": "minecraft:oak_stairs", "properties": {
  "facing": "east", "half": "bottom", "shape": "straight", "waterlogged": "false"
}}
```

Reuse or add palette symbols, then edit the rows. Every layer must have exactly `depth` rows, each exactly `width` characters. Change `size[1]` and add/remove layers together to change height. The generator is the compiler; these blueprint files are the source of truth. Do not put building geometry back into the compiler.

`block_entities` stores coordinates and NBT for jigsaws, beds and the four Phase 1 fixture types. When moving one of these blocks, move its NBT entry to the same coordinate. `entities` stores starter villagers and their local positions/role NBT. These are optional furnishings/population choices, independently editable per building; preserve the job's workstation and room access when improving a profession building.

`rooms` records enclosed bedroom bounds and an air probe for later spatial scans. Update bounds/probes when changing partitions. Bed and door coordinates are discovered from the layers, and bed counts are recalculated. Validation checks each room's floor, ceiling, walls, windows and separation; it treats doors as boundaries even when open. Native Minecraft tests also check door walking routes and all four rotations.

## Drop-in entrance contract

For any entry in a `buildings/...` pool:

- Keep the padded lot **17 blocks wide × 19 deep**. Height may be **3–32 blocks**. A smaller building can use air padding inside that lot.
- Keep exactly one `minecraft:jigsaw` at **`[8, 1, 0]`**, with block state `orientation: north_up`.
- Its NBT `name` is **`villagefriends:building_entrance`**, `pool` is **`minecraft:empty`**, `final_state` is **`minecraft:air`**, and `joint` is **`aligned`**.
- Put a solid path/floor at Y=0 beneath the entrance, with a two-block walking route into the building at Y=1–2. Place an actual front door farther inside the lot.
- Keep beds as matching head/foot pairs with the same color and facing. Homes need enclosed, separately accessible bedrooms for the future scanner.

The road rotates the entire template to face its lot. With this contract unchanged, Claude can redesign walls, roof, partitions, furniture and materials without changing the streets. Increasing width/depth requires redesigning the street spacing and rerunning assembly checks.

## Swap to a new file or add variants

Copy a blueprint to a new name such as `tavern_improved.json`. In `tools/village_layout.json`, edit only the `buildings/tavern` pool:

```json
"buildings/tavern": [
  {"template": "tavern_improved", "weight": 1}
]
```

Run the generator **without `--only`** after changing pool references. To add a variant, keep both entries and choose positive weights. The generated catalog derives the required template choices and resident counts from the layout, so assembly tests accept replacements without hardcoding the original building filenames.

The packaged pool is `data/villagefriends/worldgen/template_pool/village/buildings/tavern.json`. Advanced users can also override that pool or its native NBT template with a normal Minecraft data pack. Building changes affect newly generated villages; existing villages are saved blocks and are not rebuilt.

Central plaza and street blueprints are separate files too. Their connectors define the village graph, so changes to them require the full generator and assembly test. `village_layout.json` also holds biome and placement settings. Keep those unchanged when improving just a house.
