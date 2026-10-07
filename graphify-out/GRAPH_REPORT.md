# Graph Report - Village-Friends-Minecraft-Mod  (2026-10-07)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2949 nodes · 7761 edges · 133 communities (74 shown, 59 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 575 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `abd19cbb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Women's Garment Kit
- Casual Garment Kit
- Women's Anime Hair Kit
- Conversation Window
- Mod Init and Companions
- Men's Anime Hair Kit
- Civic and Trade Buildings
- Village Build Kit and Farms
- Men's Garment Kit
- Previews and Voice Synthesis
- Mixins and Guard Hooks
- Wardrobe Compiler
- Guard Combat Controller
- Pixel Painting Helpers
- Professions and Resident Sample
- Animation Clip Authoring
- Village Streets
- Wardrobe Editing Docs
- Plazas and Village Greens
- Building Parts Library
- Tool Entry Points
- Guard Progression Saves
- Outfit Palettes and Hair Colors
- Wardrobe 3D Piece Layer
- Animation Pack Loading
- Settlements and Ledger Pages
- Unit Test Suite
- Block Entity Hooks
- Friendship Levels and Tiers
- Garment Trims and Accessories
- Palettes and Garments
- Village Marker Block
- Gendered Wardrobe Selection
- Resident Behavior Rules
- Animation Film Capture
- Resident Life Director
- Resident Clip Posing
- Client Screen Plumbing
- Homes and Cottages
- Guard Policy and Gifts
- Foundation Asset Generators
- Resident Look Recipes
- Resident Render State
- Narrative Content Packs
- Gaits and Blinking
- Block State Helpers
- Structure Template Compiler
- Skirts and Pleats
- Guard Level Progress
- Garment Pieces
- Outfit Game Test
- Wardrobe Unit Tests
- Resident Skin Baking
- Network Payloads
- Village Layout Simulation
- Saved Companion Codecs
- Project Docs Index
- Resident Identity and Community Test
- Resident Bonds
- Animation Preview Renderer
- Resident Name Pools
- Foundation Blocks
- Friendship and Gallery Tests
- Society, Romance and Ties
- Structures Game Test
- Medical Treatment
- Eye Styles and Blink Geometry
- Face Swatch Colors
- Structure Gallery Imports
- Procedural Village Design
- Animation Film Assembly
- Townsfolk and Households
- Foundation Game Test
- Guard Damage Credit
- Animation Game Test
- Resident Sample Test
- Animation Pack Unit Tests
- Changelog Releases
- Village Ledger Screen
- Village Society Sync
- Block Registry and Phase 1
- Village Items
- Gossip Dialogue
- Foundation Entity Blocks
- Village Design CLI
- Animation Track Curves
- Chemistry and Daily Life
- Guard Spawn Egg Test
- Resident Model Planes
- Voice Synthesis
- Body Parts
- Animation Showcase Screen
- Society and Level Tests
- Village Life Game Test
- Outfit Assembly
- Farms and Market Stalls
- Animation Clip Playback
- Emote Bubbles
- Gifts and Friendship Tests
- Dock Buttons and Foundation Preview
- Social Asset Generator
- Friendship Screen and Payloads
- Village Life Docs
- Village Records
- Animation Library Loading
- Conversation Payload Updates
- Building Preview Renderer
- Handwritten Dialogue
- Resident Render State
- Conversation Button
- Roadmap Bond Tests
- Friendship State and History
- Animation Preview Screen

## God Nodes (most connected - your core abstractions)
1. `k()` - 115 edges
2. `Build` - 77 edges
3. `Society` - 62 edges
4. `solid()` - 57 edges
5. `GuardController` - 46 edges
6. `FriendshipScreen` - 46 edges
7. `Profession` - 45 edges
8. `Face` - 44 edges
9. `VillageFriends` - 42 edges
10. `Outfit` - 37 edges

## Surprising Connections (you probably didn't know these)
- `Initial Guard Equipment (UUID-selected iron/chainmail)` --references--> `GuardArmorMixin`  [AMBIGUOUS]
  GUARDS.md → src/main/java/dev/villagefriends/mixin/GuardArmorMixin.java
- `Unlimited Safe Archer Arrows` --references--> `GuardArrowMixin`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/mixin/GuardArrowMixin.java
- `Initial Guard Equipment (UUID-selected iron/chainmail)` --references--> `GuardController`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardController.java
- `Per-Player Co-op Relationship State` --references--> `SharedHistory`  [INFERRED]
  README.md → src/main/java/dev/villagefriends/SharedHistory.java
- `Palette lock` --references--> `HairColor`  [INFERRED]
  OUTFIT_ENGINE.md → src/main/java/dev/villagefriends/outfit/HairColor.java

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Resident Clip Posing Flow (director, library, poser, models)** — src_client_java_dev_villagefriends_client_residentlife_residentlife, src_main_java_dev_villagefriends_animation_animationlibrary_animationlibrary, src_client_java_dev_villagefriends_client_residentposer_residentposer, src_client_java_dev_villagefriends_client_residentanimation_residentanimation, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, src_client_java_dev_villagefriends_client_residentarmormodel_residentarmormodel [EXTRACTED 1.00]
- **Village Building Pipeline (design -> blueprint -> NBT)** — building_editing_design_programs, tools_design_village, building_editing_layered_blueprints, tools_create_village_structures, building_editing_village_layout_json [EXTRACTED 1.00]
- **Guard Progression Architecture** — src_main_java_dev_villagefriends_guardprogress_guardprogress, src_main_java_dev_villagefriends_guarddamageledger_guarddamageledger, src_main_java_dev_villagefriends_guardprogression_guardprogression, guards_guard_progression, guards_damage_based_xp_credit [EXTRACTED 1.00]
- **Wardrobe Rendering Pipeline (bake, atlas, pose worn pieces)** — src_client_java_dev_villagefriends_client_residentskins_residentskins, src_client_java_dev_villagefriends_client_outfitatlas_outfitatlas, src_client_java_dev_villagefriends_client_wardrobelayer_wardrobelayer, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, outfit_engine_palette_lock [EXTRACTED 1.00]
- **Phase 1 Foundation Registration Sequence** — src_main_java_dev_villagefriends_villagefoundation_villagefoundation, src_main_java_dev_villagefriends_villageblocks_villageblocks, src_main_java_dev_villagefriends_villageitems_villageitems, src_main_java_dev_villagefriends_villageblockentities_villageblockentities, src_main_java_dev_villagefriends_villageprofessions_villageprofessions [INFERRED 0.85]

## Communities (133 total, 59 thin omitted)

### Community 0 - "Women's Garment Kit"
Cohesion: 0.04
Nodes (36): belt(), arm_rings(), band(), bells(), brooch(), buttons(), checks(), cuffs() (+28 more)

### Community 1 - "Casual Garment Kit"
Cohesion: 0.05
Nodes (39): arm_bone(), arm_x(), body(), chest_pocket(), collar_points(), crew_neck(), jeans(), leather_belt() (+31 more)

### Community 2 - "Women's Anime Hair Kit"
Cohesion: 0.04
Nodes (38): aim(), axis(), bow(), braid(), braided_bun(), bubble_face(), bun(), _caps() (+30 more)

### Community 4 - "Mod Init and Companions"
Cohesion: 0.15
Nodes (4): CompanionController, Choice, NarrativeEngine, VillageFriends

### Community 5 - "Men's Anime Hair Kit"
Cohesion: 0.05
Nodes (29): Supreme Casual Line (t101-t120, b101-b120), Wardrobe Python Module Pipeline (tools/wardrobe), back_fan(), bangs(), cel_box(), cel_face(), lock(), chain() (+21 more)

### Community 6 - "Civic and Trade Buildings"
Cohesion: 0.13
Nodes (16): apothecary(), chapel(), crenellate(), garrison(), grave(), library(), market_garden(), plaque() (+8 more)

### Community 7 - "Village Build Kit and Farms"
Cohesion: 0.06
Nodes (11): cart(), flowerbed(), haystack(), tree_birch(), tree_oak(), well(), woodpile(), block() (+3 more)

### Community 8 - "Men's Garment Kit"
Cohesion: 0.04
Nodes (25): arm_blk(), bare_feet(), blk(), check(), embroider(), flecks(), fur(), fur_face() (+17 more)

### Community 9 - "Previews and Voice Synthesis"
Cohesion: 0.15
Nodes (12): Canvas, composite(), cube_quads(), figure(), label(), layering(), main(), render() (+4 more)

### Community 10 - "Mixins and Guard Hooks"
Cohesion: 0.08
Nodes (12): Guard Equipment Exchange (Equip held item), Initial Guard Equipment (UUID-selected iron/chainmail), Adventure Companions (Follow/Wait/Return home), VillagerEventMixin, CompanionPortalMixin, GuardArmorMixin, GuardArrowMixin, GuardMeleeMixin (+4 more)

### Community 11 - "Wardrobe Compiler"
Cohesion: 0.08
Nodes (25): build(), build_all(), catalog(), compatible(), Garment, hex_rgb(), json_text(), key_rgba() (+17 more)

### Community 12 - "Guard Combat Controller"
Cohesion: 0.10
Nodes (7): Unlimited Safe Archer Arrows, Automatic Village Defense (Knights and Archers), villager_predators Entity Tag, GuardGameTest, Combat, GuardController, RecentAttack

### Community 13 - "Pixel Painting Helpers"
Cohesion: 0.06
Nodes (19): wave_face(), band(), button(), cloth_shade(), curls_box(), curls_face(), dark_seams(), hair_box() (+11 more)

### Community 15 - "Professions and Resident Sample"
Cohesion: 0.06
Nodes (30): Profession, ADVENTURER, APOTHECARY, ARCHER, ARMORER, BARD, BUTCHER, CARPENTER (+22 more)

### Community 17 - "Village Streets"
Cohesion: 0.08
Nodes (21): lamp_bench(), avenue(), avenue_bend(), bend_left(), bend_right(), crossroads(), end_fade(), end_gate() (+13 more)

### Community 18 - "Wardrobe Editing Docs"
Cohesion: 0.12
Nodes (14): File format, Mix and match, Palette lock, Pieces, Professions, Recipes and genders, Rendering, Verification (+6 more)

### Community 19 - "Plazas and Village Greens"
Cohesion: 0.11
Nodes (19): sine(), base(), bell_frame(), big_oak(), _dir(), fountain(), fountain_square(), gazebo() (+11 more)

### Community 20 - "Building Parts Library"
Cohesion: 0.07
Nodes (23): is_air(), along(), beam_ring(), bench(), door_cells(), floor(), foundation(), gable_roof() (+15 more)

### Community 21 - "Tool Entry Points"
Cohesion: 0.22
Nodes (7): Editable Name Pools (tools/name_pools.json), build(), load(), main(), validate(), main(), unique()

### Community 22 - "Guard Progression Saves"
Cohesion: 0.11
Nodes (7): Combat Profession Lock, Guard Level Progression (0-50), GuardProgressGameTest, Incident, Credit, GuardProgression, Probe

### Community 23 - "Outfit Palettes and Hair Colors"
Cohesion: 0.11
Nodes (4): Cell, Garment, HairColor, Outfit

### Community 24 - "Wardrobe 3D Piece Layer"
Cohesion: 0.13
Nodes (4): ResidentArmorModel, Baked, Shown, WardrobeLayer

### Community 26 - "Animation Pack Loading"
Cohesion: 0.25
Nodes (5): Mirror, FREE, HAND, NEVER, AnimationPack

### Community 29 - "Block Entity Hooks"
Cohesion: 0.10
Nodes (10): Patrols, Command Desk Controls and Shields (future), Foundation Catalog (foundation-catalog.json), Empty Block Entity Integration Hooks, Future Spatial Bed Scanner, Room/Structure Catalog (structure-catalog.json), ApothecaryCotBlockEntity, CommandDeskBlockEntity, HousePlaqueBlockEntity (+2 more)

### Community 30 - "Friendship Levels and Tiers"
Cohesion: 0.09
Nodes (11): Friendship Forgiveness for Player Hits, Per-Player Co-op Relationship State, Four-Chapter Personal Stories, Relationship Tiers (New Neighbor to Best Friend), Milestone 7: Romance and Family (future), Shared Activities (Walk, Picnic, Exploration, Gathering), Outing, FriendshipBook (+3 more)

### Community 31 - "Garment Trims and Accessories"
Cohesion: 0.06
Nodes (19): tie(), cloak(), collar_flat(), hanging(), leg_ring_fold(), leg_rings(), mantle(), over_flaps() (+11 more)

### Community 32 - "Palettes and Garments"
Cohesion: 0.10
Nodes (4): Ten Master Palettes, Sims-style Men's and Women's Wardrobes, ColorPalette, MasterPalettes

### Community 33 - "Village Marker Block"
Cohesion: 0.07
Nodes (11): Replacement Pools and required_pools, Structure Processors (worn roads, plank bridges, weathered stone), Village Layout Config (tools/village_layout.json, format 2), Random-Spread Structure Placement, Hometown Names and Settlements, Village Marker, Block, OutfitAtlas (+3 more)

### Community 34 - "Gendered Wardrobe Selection"
Cohesion: 0.12
Nodes (7): Village Friends 2.8.0 — Casual medieval and anime hair expansion, Gender, FEMALE, MALE, NON_BINARY, Vec3, Wardrobe

### Community 38 - "Animation Film Capture"
Cohesion: 0.10
Nodes (4): AnimationCast, Role, AnimationFilmGameTest, AnimationPackGameTest

### Community 40 - "Resident Clip Posing"
Cohesion: 0.13
Nodes (10): ResidentPoser, Bone, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG (+2 more)

### Community 42 - "Homes and Cottages"
Cohesion: 0.09
Nodes (25): Lots (homes, workshops, decorations, empty gaps), Vanilla Trade Workshops, cottage(), family_house(), farmhouse(), garden(), kitchen(), path() (+17 more)

### Community 44 - "Foundation Asset Generators"
Cohesion: 0.14
Nodes (11): Foundation Asset Generation Pipeline, boxes(), icon(), merge(), recipe(), save(), tag(), save() (+3 more)

### Community 45 - "Resident Look Recipes"
Cohesion: 0.11
Nodes (12): PaletteID, ASH_AND_TEAL, DESERT_SUN, FOREST_AND_HEARTH, ROYAL_VELVET, RUSTIC_TWEED, SAGE_AND_TERRACOTTA, SCHOLARLY_PLUM (+4 more)

### Community 47 - "Narrative Content Packs"
Cohesion: 0.17
Nodes (8): Narrative Content Pack (content.json), Gifts and Promises, Conditions, Data, NarrativeContent, Personality, Request, Story

### Community 48 - "Gaits and Blinking"
Cohesion: 0.11
Nodes (11): Shared Gait Function (resident and armor models), Living Villagers (walking styles, breathing, articulated eyes), Gait, CURIOUS, EASY, MEASURED, NIMBLE, SPRIGHTLY (+3 more)

### Community 49 - "Block State Helpers"
Cohesion: 0.22
Nodes (13): bid(), can_take(), stairs_at(), full_cube(), gate_connects(), is_fence(), is_gate(), is_pane() (+5 more)

### Community 50 - "Structure Template Compiler"
Cohesion: 0.09
Nodes (14): Byte, check_lot(), location(), main(), payload(), pool(), pool_name(), pool_spec() (+6 more)

### Community 51 - "Skirts and Pleats"
Cohesion: 0.13
Nodes (3): pleats(), Skirt, tier()

### Community 53 - "Garment Pieces"
Cohesion: 0.14
Nodes (10): Kind, BOTTOM, HAIR, TOP, Motion, FLAP_BACK, FLAP_FRONT, NONE (+2 more)

### Community 54 - "Outfit Game Test"
Cohesion: 0.28
Nodes (3): Locked One-Piece Outfits (locked_to), OutfitGameTest, OutfitTemplate

### Community 55 - "Wardrobe Unit Tests"
Cohesion: 0.09
Nodes (16): Fit, FEMALE, MALE, UNISEX, WardrobeTest, Guard defense verification (2.9.0), Guard progression verification (2.10.0), Guard spawn egg verification (2.10.1) (+8 more)

### Community 56 - "Resident Skin Baking"
Cohesion: 0.15
Nodes (3): Entry, Loaded, ResidentSkins

### Community 57 - "Network Payloads"
Cohesion: 0.14
Nodes (8): ActionPayload, EmotePayload, Detail, Entry, LedgerPayload, Tie, LedgerRequestPayload, Where things live

### Community 60 - "Village Layout Simulation"
Cohesion: 0.27
Nodes (11): Village Layout Simulation, In-Game Village Gallery (-PvillageGallery), assemble(), draw(), load(), main(), overlaps(), placed_box() (+3 more)

### Community 63 - "Project Docs Index"
Cohesion: 0.18
Nodes (13): Animation packs, Gaits, Resident movement, animation packs and eyes, Verification, Editing the Plains Village, graphify, Village Friends, Village Friends Developer Handoff (+5 more)

### Community 64 - "Resident Identity and Community Test"
Cohesion: 0.14
Nodes (4): Persistent Resident Identity (stable ID), CommunityGameTest, CompanionState, ResidentProfile

### Community 65 - "Resident Bonds"
Cohesion: 0.21
Nodes (3): Resident-to-Resident Connections, BondBook, BondState

### Community 67 - "Animation Preview Renderer"
Cohesion: 0.18
Nodes (8): draw(), load_pack(), main(), pose(), render_frame(), Resident, sample(), Track

### Community 68 - "Resident Name Pools"
Cohesion: 0.22
Nodes (4): ResidentAppearance, Data, Pool, ResidentNames

### Community 71 - "Society, Romance and Ties"
Cohesion: 0.15
Nodes (3): Society, SocietyBook, Tie

### Community 73 - "Medical Treatment"
Cohesion: 0.16
Nodes (8): Future Real-Time Knockout Controller, Medical Treatment Contract, Downed Companion Rescue, MedicalSupplyItem, Treatment, BANDAGE_WRAP, REVIVAL_TONIC, SMELLING_SALTS

### Community 74 - "Eye Styles and Blink Geometry"
Cohesion: 0.27
Nodes (4): Eyes and face, EyeStyle, SOFT_GLINT, STARLIT

### Community 75 - "Face Swatch Colors"
Cohesion: 0.15
Nodes (4): HairFaceGameTest, FaceDetails, HandcraftedFaceTest, Starlit and Soft Glint faces verification (2.13.0)

### Community 77 - "Procedural Village Design"
Cohesion: 0.19
Nodes (13): Civic Slots (priority 5), Village Design Kit (kit.py, parts.py, roads.py), Building Design Programs (DESIGNS = {name: function}), Lot Contract (building_entrance jigsaw), Village Jigsaw Graph, Master Specification (Codex roadmap), Six Guaranteed Civic Buildings, Enclosed Bedrooms (+5 more)

### Community 78 - "Animation Film Assembly"
Cohesion: 0.24
Nodes (8): card(), font(), main(), emit(), fade(), hold(), play(), scene_frames()

### Community 81 - "Guard Damage Credit"
Cohesion: 0.46
Nodes (3): Damage-Based Guard XP Credit, GuardDamageLedger, Hit

### Community 83 - "Resident Sample Test"
Cohesion: 0.15
Nodes (9): Focused Client GameTest Flags, View, BACK, FRONT, HEAD, HEAD_BACK, WALK, Resident (+1 more)

### Community 84 - "Animation Pack Unit Tests"
Cohesion: 0.20
Nodes (5): Authoring Village Life, How the director chooses, Resident animation packs, Village Life (pack 1), AnimationPackTest

### Community 85 - "Changelog Releases"
Cohesion: 0.11
Nodes (17): 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0, 2.6.0, Male asset registry — Phase 2 (+9 more)

### Community 88 - "Block Registry and Phase 1"
Cohesion: 0.14
Nodes (8): Phase 1 Foundation Gameplay Verification, Native Trade Sets (50 sets, 100 offers), 17 New Foundation Blocks, Registration Order (blocks, items, block entities, professions), Codex Phase 1: Registry & Item Foundation, Ten New Professions and Workstations, VillageBlocks, VillageFoundation

### Community 89 - "Village Items"
Cohesion: 0.19
Nodes (5): Bread, Stew and Coffee Consumables, 24 New Items and 41 Recipes, Wearable Uniforms and Rain Gear, VillageItems, VillageMealItem

### Community 91 - "Foundation Entity Blocks"
Cohesion: 0.24
Nodes (6): FoundationEntityBlock, Kind, APOTHECARY_COT, COMMAND_DESK, HOUSE_PLAQUE, NOTICE_BOARD

### Community 92 - "Village Design CLI"
Cohesion: 0.15
Nodes (5): Layered JSON Blueprints (tools/village_blueprints), main(), designs(), checksum(), dump()

### Community 97 - "Voice Synthesis"
Cohesion: 0.31
Nodes (9): envelope(), finish(), glottal(), hum(), make_ui(), make_voice(), resonator(), voiced() (+1 more)

### Community 98 - "Body Parts"
Cohesion: 0.25
Nodes (7): BodyPart, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG, TORSO

### Community 100 - "Society and Level Tests"
Cohesion: 0.23
Nodes (4): Village Friends 2.13.0 — Village life and new faces, FriendshipLevelsTest, SocietyTest, Village life verification (2.13.0)

### Community 103 - "Farms and Market Stalls"
Cohesion: 0.22
Nodes (9): market_stalls(), apiary(), farm_beets(), farm_mixed(), farm_wheat(), field(), paddock(), pumpkin_patch() (+1 more)

### Community 106 - "Emote Bubbles"
Cohesion: 0.08
Nodes (17): Bubble, EmoteBubbles, Pending, VillageFriendsClient, Emote, ANGER, BLUSH, DOTS (+9 more)

### Community 112 - "Social Asset Generator"
Cohesion: 0.28
Nodes (8): bubble(), dots(), emote_sheet(), main(), mask_image(), png(), rgba(), write()

### Community 114 - "Village Life Docs"
Cohesion: 0.18
Nodes (8): Relations, Conversation window, Dialogue, Friendship levels, Speech bubbles, Verification, Village Ledger, Village life: families, love, friendship levels, speech bubbles and the Village Ledger

### Community 116 - "Animation Library Loading"
Cohesion: 0.25
Nodes (3): Village Life Animation Pack (99 clips), AnimationPacks, AnimationLibrary

### Community 118 - "Building Preview Renderer"
Cohesion: 0.25
Nodes (5): boxes(), color(), _lookup(), main(), render()

### Community 119 - "Handwritten Dialogue"
Cohesion: 0.24
Nodes (3): Conversation Window (Talk/Story/Journal/Time/Travel tabs), Wordless Human-like Hum Voices, Dialogue

## Ambiguous Edges - Review These
- `GuardArmorMixin` → `Initial Guard Equipment (UUID-selected iron/chainmail)`  [AMBIGUOUS]
  GUARDS.md · relation: references
- `FriendshipGameTest` → `Focused Client GameTest Flags`  [AMBIGUOUS]
  DEVELOPMENT.md · relation: references

## Knowledge Gaps
- **149 isolated node(s):** `Loaded`, `ANGER`, `BLUSH`, `DOTS`, `EXCLAIM` (+144 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 824 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **59 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `GuardArmorMixin` and `Initial Guard Equipment (UUID-selected iron/chainmail)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Wardrobe Python Module Pipeline (tools/wardrobe)` connect `Men's Anime Hair Kit` to `Palettes and Garments`, `Casual Garment Kit`, `Women's Anime Hair Kit`, `Women's Garment Kit`, `Men's Garment Kit`, `Wardrobe Compiler`, `Procedural Village Design`, `Outfit Game Test`, `Project Docs Index`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **What connects `Loaded`, `ANGER`, `BLUSH` to the rest of the system?**
  _149 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Women's Garment Kit` be split into smaller, more focused modules?**
  _Cohesion score 0.036133694670280034 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `FriendshipGameTest` and `Focused Client GameTest Flags`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Sims-style Men's and Women's Wardrobes` connect `Palettes and Garments` to `Wardrobe 3D Piece Layer`, `Gendered Wardrobe Selection`, `Men's Anime Hair Kit`, `Project Docs Index`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Should `Casual Garment Kit` be split into smaller, more focused modules?**
  _Cohesion score 0.04912280701754386 - nodes in this community are weakly interconnected._