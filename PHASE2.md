# Village Friends: Phase 2 structures

Implements the master specification's **Codex Phase 2: Worldgen & Structures** roadmap. Minecraft loads the packaged JSON registries and compressed NBT templates directly from the mod.

## Layout

`villagefriends:village` generates a complete 13-piece settlement: a fountain plaza, four streets, a tavern, garrison, cemetery, family house, cottage, apothecary, workshop and library. The cottage pool chooses among oak, birch and spruce variants. Fifteen authored templates and thirteen pools provide those pieces and variants.

The plaza includes a Notice Board, benches, campfire seating, an easel and music stand. The garrison contains training equipment, a Command Desk, beds and an accessible battlement. The tavern has a partitioned kitchen, drinks equipment, tables, seating and a guest loft reached by a ladder. The apothecary has an Alchemical Press, treatment cots and a private bedroom. The workshop and library provide the other new profession anchors. The cemetery contains decorative graves and planting; its graves do not represent saved deceased residents.

Fourteen starter villagers include all ten new professions, three unemployed adults and one child. They use the existing resident entity, identity, trading and hometown systems. Profession residents begin with one villager XP to retain their authored role. Uniforms, specialized patrols, treatment, seating and meal routines remain later behavior work.

## Natural generation and commands

The structure generates in plains and meadow biomes using its own random-spread structure set: spacing 40 chunks, separation 12, salt 18374629. An exclusion zone avoids candidate vanilla village placements within ten chunks. Vanilla village templates, pools and placement remain available. The new structure joins the `minecraft:village` structure tag, allowing existing settlement discovery and naming to recognize it.

Rigid pieces keep doors, street surfaces and floors aligned. Minecraft's `beard_thin` terrain adaptation blends foundations into terrain. Depth three and an 80-block distance limit allow the entire planned layout to assemble. As with vanilla worldgen, terrain and other structures can affect the surroundings.

New villages appear in **newly generated chunks**. Existing villages and explored chunks are not rebuilt. In a cheats-enabled world:

```text
/locate structure villagefriends:village
/place jigsaw villagefriends:village/town_centers villagefriends:town_start 3
/place template villagefriends:village/family_house
```

Use the place commands in a clear area or a development world; they place actual blocks and residents.

## Enclosed houses and future scans

The family house has a living room, central hallway and two independently enclosed bedrooms. Each cottage has a living room, hallway and enclosed bedroom. The apothecary's private bedroom is also enclosed. All bedroom floors, ceilings, walls and windows are solid, with real two-part doors and a clear two-block walking route on each side. Bedrooms contain beds with matching head and foot states; rotating a template rotates doors, beds and custom blocks together.

The later spatial bed scanner is not implemented here. House Plaques instantiate the Phase 1 block entity with its existing empty scan hooks. The reproducible room catalog records room bounds, probes, bed feet, doors, fixtures and connectors so future scanning can use these layouts as fixtures. Treat doors as room boundaries even when open.

## Editing and verification

Each building has its own editable layered JSON blueprint in `tools/village_blueprints/`. Pool choices and placement live separately in `tools/village_layout.json`. The buildings are basic layouts intended for later improvement. Read [BUILDING_EDITING.md](BUILDING_EDITING.md) for per-building edits, replacement/variant pools and the stable entrance contract.

Run `python tools/create_village_structures.py` to regenerate all templates, pools, biome/structure tags, placement and `data/villagefriends/villagefriends/structure-catalog.json`. Use `--only tavern` to rebuild one building without touching other templates/pools, or `--check` for validation without changes. Only Python's standard library is required. The generator validates enclosed bedrooms, paired beds and compatible entrances before writing deterministic gzip-compressed NBT.

`gradlew.bat build` packages the worldgen resources and runs the existing JUnit checks. `gradlew.bat runClientGameTest -PstructuresOnly` exercises native template loading, rotated bedrooms and door access, fixture block entities, twelve complete jigsaw assemblies, natural world generation, all ten professions/trades, hometown assignment and save/reload. The normal gameplay command also runs the five previous tests. Test code and screenshots are excluded from the release JAR.
