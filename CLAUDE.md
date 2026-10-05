# Village Friends handoff

Plains villages are procedural and art-directed: a random town centre ringed by the six guaranteed civic buildings, terrain-following streets, and lots filled with homes, vanilla-trade workshops, farms and small decorations. Keep every building an independent template with its own blueprint; improve one without touching the others.

Read [BUILDING_EDITING.md](BUILDING_EDITING.md) before changing structures. It documents the village graph, design kit, lot contract, simulation and gallery.

- Design programs: `tools/village_design/buildings/*.py` (shared helpers in `kit.py`, `parts.py`, `roads.py`). `python tools/design_village.py <name>` writes the blueprint; it never overwrites a hand-edited blueprint without `--force`.
- Building source for the compiler: one layered JSON file per template in `tools/village_blueprints/`.
- Village graph, pools, weights, processors, depth and distance: `tools/village_layout.json` (format 2).
- Compiler: `tools/create_village_structures.py`. Keep geometry in the designs/blueprints, not in this compiler.
- Runtime templates: `src/main/resources/data/villagefriends/structure/village/*.nbt`; pools under `worldgen/template_pool/village/`.

To improve an existing building, edit its design (or blueprint) under the same name and run:

```text
python tools/design_village.py tavern
python tools/create_village_structures.py --check
python tools/create_village_structures.py --only tavern
```

Lots keep one north-facing `villagefriends:building_entrance` jigsaw at `[x,1,0]` (air replacement, aligned joint, empty pool). Civic slots are at most 17 wide (large) or 11 wide (small). Preserve accessible enclosed bedrooms (`b.room`) and matched bed halves; doors need two clear blocks on both sides (the kit checks this). The catalog and tests derive required pools from the layout, so replacement filenames need no Java edits. Use `python tools/village_design/simulate.py` to balance pool weights, and `gradlew.bat runClientGameTest -PvillageGallery -Pgallery=name1,name2` to screenshot templates and whole villages in Minecraft.

Use the existing build target; changing Minecraft versions is separate work. `build.ps1` selects the installed user JDK and builds the mod. `gradlew.bat runClientGameTest -PstructuresOnly` validates structures in Minecraft; the default gameplay command runs all registered tests. Test code belongs in the gametest source set and is excluded from the release JAR.

The registry/items and village layout phases are implemented. The old wardrobe was removed and replaced with the palette-locked outfit engine; read [OUTFIT_ENGINE.md](OUTFIT_ENGINE.md). Definitions live in `src/main/java/dev/villagefriends/outfit/`. The fifteen active male starter entries are canonical compact JSON in `assets/villagefriends/outfits/male-registry.json`; read [MALE_ASSETS.md](MALE_ASSETS.md) before editing them. Female expansion is on hold; the draft female classes and JSON are excluded from the active renderer/factory catalog. Use `gradlew.bat runClientGameTest -PoutfitsOnly` for focused renderer verification. Names remain editable in `tools/name_pools.json`; preserve complexion eligibility.

Version 2.6 adds restrained resident walking and articulated eyes. Read [ANIMATION_EDITING.md](ANIMATION_EDITING.md) before changing them. Both resident and armor models share the same gait function; keep special vanilla poses and original face UV colors intact.

The spatial bed scanner, specialized guard routines, real-time medical treatment and seating remain future work. The existing block entity hooks are intentionally empty. See PHASE1.md, PHASE2.md, OUTFIT_ENGINE.md and VERIFICATION.md for scope and evidence.


