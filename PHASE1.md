# Village Friends: Phase 1 implementation

Implements the **Codex Phase 1: Registry & Item Foundation** roadmap from the supplied master specification, using the project's existing build target.

## Implementation plan

1. **Phase 1:** register professions, workstation POIs, blocks, items and block entity types; package usable models, textures, recipes, loot, localization and trades; expose hooks for the later controllers. Use vanilla job acquisition and trading for the new professions.
2. **Phase 2:** add plaza, tavern, garrison, cemetery and enclosed-house templates and jigsaw pools. Coordinate house interiors with the future bed scanner.
3. **Outfit engine:** replace the previous wardrobe with the four-role palette system, volumetric hair and cohesive garment factory in [OUTFIT_ENGINE.md](OUTFIT_ENGINE.md).

Specialized guard AI, daily schedules, the real-time knockout system, recruitment, housing scans and animation remain separate work. Knights and archers use the existing resident villager entity; this phase does not need a new entity type.

## Content

All identifiers below use the `villagefriends` namespace.

| Profession | Workstation IDs |
|---|---|
| Knight | `training_dummy` |
| Archer | `archery_target` |
| Cook | `kitchen_stove` |
| Tavern Keeper | `drinks_barrel`, `tap_stand` |
| Apothecary | `alchemical_press` |
| Painter | `easel_canvas` |
| Bard | `music_stand` |
| Tailor | `sewing_table` |
| Carpenter | `sawmill` |
| Scholar | `archives` |

Each workstation orientation is a job POI with one ticket and a range of one. The `minecraft:acquirable_job_site` tag makes it discoverable. Sewing Tables and Archives provide distinct anchors: vanilla looms, lecterns and barrels keep their original profession assignments. All ten jobs have localized names, work dialogue and ordinary villager work behavior.

There are **50 native trade sets and 100 offers**, two per profession level across all five levels. Residents sell job products and buy appropriate supplies. Prices are initial balance choices, editable in `data/villagefriends/trade_set` and `villager_trade`.

**17 new blocks:** eleven workstation blocks, Village Bench, Campfire Bench, Apothecary Cot, House Plaque, Notice Board and Command Desk. Each has four facing states, matching collision/model geometry, an item definition, a crafting recipe/unlock, localization and a self-drop loot table. The existing Village Marker remains available.

**24 new items:** Smelling Salts, Revival Tonic, Bandage Wrap, Empty Coffee Mug, Steaming Coffee Mug, Fresh Village Bread, Hearty Stew, Rain Cloak, Hooded Poncho, ten profession uniforms, Broom, Paintbrush, Lute, Carpenter Hammer and Field Journal. There are **41 new crafting recipes** in total.

Bread supplies food/saturation and heals two health points; stew heals six and returns a bowl. Coffee can be drunk at full hunger, grants Speed I for 30 seconds and returns its mug. Consumption effects run on the server. NPC meal routines are later work.

The twelve wearables equip in the chest slot with original equipment textures and no armor protection. They can be given to traveling companions with **Travel → Equip held item**. Automatic weather equipment and automatic custom-profession outfits are later work. The five tools are registered handheld props; sweeping, painting, music playback, construction and writable-journal behavior are future systems.

The medical recipes match the specification. Revival Tonic requires an **Awkward Potion** through Fabric's component ingredient; water and other potions are rejected. Where the specification gave no recipe, this phase supplies initial craftable recipes.

## Integration hooks and limits

`VillageFoundation.register()` runs from `VillageFriends.onInitialize()` before narrative content loading. Registration order is blocks → items → block entity types → professions. New content appears in the existing Functional Blocks, Food & Drinks, Tools & Utilities and Combat creative tabs.

| Block entity | Public hook methods |
|---|---|
| `HousePlaqueBlockEntity` | `scanForBeds()`, `scanForWorkstations()` |
| `NoticeBoardBlockEntity` | `refreshNotices()` |
| `CommandDeskBlockEntity` | `updatePatrolAssignments()`, `refreshGuardRoster()` |
| `ApothecaryCotBlockEntity` | `updatePatient()` |

These hooks are intentionally empty, with no tickers. Placement creates the correct registered entity; vanilla chunk serialization retains its type and position. Housing, notice, patrol and patient state should receive a versioned persistence schema when those systems are implemented.

`MedicalSupplyItem.treatment()` exposes this future treatment contract:

| Supply | Restored maximum-health fraction | Extra revival time |
|---|---|---|
| Smelling Salts | 0.20 | zero |
| Revival Tonic | 1.00 | zero |
| Bandage Wrap | 0.00 | 12 real-time hours |

**Medical items do not revive residents or extend timers yet.** The future knockout controller should validate the patient, apply the contract on the server and consume the supply only on success. The existing companion rescue/recovery behavior is retained.

Benches declare a planned capacity of two in `VillageBlocks.BENCH_CAPACITY`; actual seating is later work. The cot is a single-block medical anchor and does not claim home POIs. The House Plaque is placed on top of a block and faces the player; wall attachment and housing recognition are later work. Workstations are job anchors and do not open processing menus yet.

## Assets and verification

`tools/create_foundation_assets.py` reads the block geometry and profession IDs from Java and reproduces the Phase 1 assets/data using Python + Pillow. It paints original 16×16 block/item art and 64×32 equipment textures. Static voxel models provide usable initial geometry; final Blockbench models and animations can replace assets at the same IDs. Players need neither Python nor an art service.

Run `python tools/create_foundation_assets.py` to regenerate. Item sprites are authored pixel by pixel in `tools/item_sprites.py`: original transparent 16×16 textures with Minecraft-style material outlines, stepped highlights/shadows and diagonal tools. The script creates `build/phase1-assets.png` and `build/phase1-item-sprites.png`, development contact sheets, and packages `data/villagefriends/villagefriends/foundation-catalog.json` for verification/integrations. The catalog is documentation data rather than a reloadable registry configuration. Both this script and `create_village_marker.py` merge shared language/axe-tag files to preserve each other's content.

`FoundationGameTest` runs first in the Fabric client gameplay suite. It validates actual registry/POI loading, all recipes, exact potion matching, every trade level, block-item placement and drops, natural acquisition of all ten professions, consumption/equipment effects and block entity/profession/trade/uniform save/reload. It captures a gallery of models rendered by Minecraft as `village-friends-phase1-content.png`.

Run `gradlew.bat build` for release packaging and the existing JUnit checks, then `gradlew.bat runClientGameTest` for the new gameplay test and four existing regressions. Tests use development worlds; test code/screenshots are excluded from the release JAR.

For a focused Phase 1 content/asset recheck, use `gradlew.bat runClientGameTest -PfoundationOnly`. With Phase 2 added, the normal command runs all six gameplay tests. Worldgen implementation details are in [PHASE2.md](PHASE2.md).

