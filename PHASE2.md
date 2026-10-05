# Village Friends: Phase 2 structures

Implements the master specification's **Codex Phase 2: Worldgen & Structures** roadmap. Minecraft loads the packaged JSON registries and compressed NBT templates directly from the mod.

## Layout

`villagefriends:village` is a procedural plains village. One of three town centres (a fountain square, a village green under a great oak, or a market square with a timber market hall) starts the village at a random rotation. Around the 33×33 square stand the six guaranteed civic buildings: tavern, garrison with watchtower and training yard, carpenter-and-tailor workshop, chapel with bell tower and graveyard, apothecary and library. Two more slots hold market stalls or a pocket garden.

Four avenues leave the square and grow into a random street network: straights, S-bends, turns, tees, forks, crossroads and small well squares. Streets end in fading paths, lamp-and-bench ends or a timber gatehouse with palisade wings. Lots along the streets take timber-framed cottages, two-storey and jettied houses, townhouses, a farmhouse and the family house. Trade workshops (smithy, butcher, fletcher, shepherd, fisher, cartographer, mason and tannery) give unemployed residents vanilla jobs. Trees, haystacks and carts fill some gaps. Fields, paddocks with livestock, pumpkin patches and apiaries gather on the outermost streets.

The square holds the Notice Board, benches, the easel, music stand and a bell (the vanilla meeting point). The garrison has training dummies, archery targets, a Command Desk and a bunk room; the tavern a bar with tap stand and drinks barrel, a hearth, a kitchen with the stove and two guest rooms; the apothecary an Alchemical Press and treatment cots; the workshop a sawmill shed and a sewing table; the library Archives among bookshelves. The chapel's graves are decorative and do not represent saved deceased residents.

A typical village has 55–140 pieces, about 19 homes and 25–70 residents. The painter and bard work in the square; the other eight new professions work in the civic buildings, so all ten appear in every village. Residents use the existing resident entity, identity, trading and hometown systems. Profession residents begin with one villager XP to retain their authored role. Uniforms, specialized patrols, treatment, seating and meal routines remain later behavior work.

## Natural generation and commands

The structure generates in plains and meadow biomes using its own random-spread structure set: spacing 40 chunks, separation 12, salt 18374629. An exclusion zone avoids candidate vanilla village placements within ten chunks. Vanilla village templates, pools and placement remain available. The new structure joins the `minecraft:village` structure tag, allowing existing settlement discovery and naming to recognize it.

Buildings are rigid pieces that keep doors and floors level; streets are terrain-matching, so roads follow the ground and become plank bridges over water. Minecraft's `beard_thin` terrain adaptation blends foundations into the terrain. Depth six and a 100-block distance limit bound the village. As with vanilla worldgen, terrain and other structures can affect the surroundings.

New villages appear in **newly generated chunks**. Existing villages and explored chunks are not rebuilt. In a cheats-enabled world:

```text
/locate structure villagefriends:village
/place jigsaw villagefriends:village/town_centers villagefriends:town_start 3
/place template villagefriends:village/family_house
/place structure villagefriends:village
```

Use the place commands in a clear area or a development world; they place actual blocks and residents.

## Enclosed houses and future scans

Every home has at least one enclosed bedroom: cottages behind a partition, two-storey houses and townhouses upstairs, and the farmhouse in its wing. The tavern, garrison, workshop, apothecary and library also have enclosed bedrooms. Bedroom floors, ceilings, walls and windows are solid, with real two-part doors and a clear two-block walking route on each side. Beds have matching head and foot states, and rotating a template rotates doors, beds and custom blocks together.

The later spatial bed scanner is not implemented here. House Plaques instantiate the Phase 1 block entity with its existing empty scan hooks. The reproducible room catalog records room bounds, probes, bed feet, doors, fixtures and connectors so future scanning can use these layouts as fixtures. Treat doors as room boundaries even when open.

## Editing and verification

Buildings are written as small Python design programs in `tools/village_design/buildings/`, compiled to one layered JSON blueprint per template in `tools/village_blueprints/`. Pools, weights, processors and placement live in `tools/village_layout.json`. Read [BUILDING_EDITING.md](BUILDING_EDITING.md) for the design kit, lot contract, replacement pools, layout simulation and the in-game gallery.

Run `python tools/design_village.py` to rebuild blueprints from designs, then `python tools/create_village_structures.py` to regenerate templates, pools, processor lists, biome/structure tags, placement and `data/villagefriends/villagefriends/structure-catalog.json`. Use `--only tavern` to rebuild one building, or `--check` for validation without changes. Only Python's standard library is required; previews and maps use Pillow. The generator validates enclosed bedrooms, paired beds, lot entrances, start jigsaws and pool references before writing deterministic gzip-compressed NBT.

`gradlew.bat build` packages the worldgen resources and runs the existing JUnit checks. `gradlew.bat runClientGameTest -PstructuresOnly` exercises native template loading, rotated bedrooms and door access, fixture block entities, twelve procedural jigsaw assemblies, natural world generation, all ten professions/trades, hometown assignment and save/reload. The normal gameplay command also runs the five previous tests. `-PvillageGallery` captures art-direction screenshots. Test code and screenshots are excluded from the release JAR.
