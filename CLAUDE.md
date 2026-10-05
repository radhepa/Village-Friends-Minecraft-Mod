# Village Friends handoff

The user wants **basic, independently replaceable buildings**. Claude will improve them later. Keep each building separate; avoid adding elaborate behavior as part of a building edit.

Read [BUILDING_EDITING.md](BUILDING_EDITING.md) before changing structures. It documents the blueprint format, entrance contract, regeneration and replacement workflow.

- Building source: one layered JSON file per building in `tools/village_blueprints/`.
- Village graph and pool choices: `tools/village_layout.json`.
- Compiler: `tools/create_village_structures.py`. Keep geometry in the blueprints, not in this compiler.
- Runtime templates: `src/main/resources/data/villagefriends/structure/village/*.nbt`.
- Runtime role pools: `src/main/resources/data/villagefriends/worldgen/template_pool/village/buildings/*.json`.

To improve an existing building, edit its blueprint under the same filename and run:

```text
python tools/create_village_structures.py --check
python tools/create_village_structures.py --only tavern
```

Replace `tavern` with the edited filename without `.json`. To swap in a new file or add variants, change that role's pool in `village_layout.json` and run the full generator.

Building lots are padded to 17×19 blocks. Preserve the north-facing `villagefriends:building_entrance` jigsaw at `[8,1,0]`, its air replacement, aligned joint and terminating empty pool. Preserve accessible enclosed bedrooms and matched bed halves; update the blueprint's room bounds/probes if partitions move. The generated catalog and tests derive pool choices from the layout so replacement filenames do not require Java edits.

Use the existing build target; changing Minecraft versions is separate work. `build.ps1` selects the installed user JDK and builds the mod. `gradlew.bat runClientGameTest -PstructuresOnly` validates structures in Minecraft; the default gameplay command runs all registered tests. Test code belongs in the gametest source set and is excluded from the release JAR.

The registry/items and village layout phases are implemented. The old wardrobe was removed and replaced with the palette-locked outfit engine; read [OUTFIT_ENGINE.md](OUTFIT_ENGINE.md). Definitions live in `src/main/java/dev/villagefriends/outfit/`. The fifteen active male starter entries are canonical compact JSON in `assets/villagefriends/outfits/male-registry.json`; read [MALE_ASSETS.md](MALE_ASSETS.md) before editing them. Female expansion is on hold; the draft female classes and JSON are excluded from the active renderer/factory catalog. Use `gradlew.bat runClientGameTest -PoutfitsOnly` for focused renderer verification. Names remain editable in `tools/name_pools.json`; preserve complexion eligibility.

Version 2.6 adds restrained resident walking and articulated eyes. Read [ANIMATION_EDITING.md](ANIMATION_EDITING.md) before changing them. Both resident and armor models share the same gait function; keep special vanilla poses and original face UV colors intact.

The spatial bed scanner, specialized guard routines, real-time medical treatment and seating remain future work. The existing block entity hooks are intentionally empty. See PHASE1.md, PHASE2.md, OUTFIT_ENGINE.md and VERIFICATION.md for scope and evidence.


