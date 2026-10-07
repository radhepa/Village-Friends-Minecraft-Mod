# Graph Report - Village-Friends-Minecraft-Mod  (2026-10-07)

## Corpus Check
- 175 files · ~134,352 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .properties 2, .jar 1)

## Summary
- 2657 nodes · 6752 edges · 111 communities (73 shown, 38 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 495 edges (avg confidence: 0.85)
- Token cost: 335,178 input · 0 output

## Community Hubs (Navigation)
- Women's Garment Kit
- Casual Garment Kit
- Women's Anime Hair Kit
- Friendship Screen and Payloads
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
- Outfit Engine Concepts
- Plazas and Village Greens
- Building Parts Library
- Tool Entry Points
- Guard Progression Saves
- Outfit Palettes and Hair Colors
- Wardrobe 3D Piece Layer
- Animation Pack Loading
- Village Settlements
- Unit Test Suite
- Block Entity Hooks
- Friendship State and History
- Garment Trims and Accessories
- Village Marker Block
- Gendered Wardrobe Selection
- Animation Director and Packs
- Animation Film Capture
- Resident Life Director
- Resident Clip Posing
- Screen and GUI Rendering
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
- Wardrobe Catalog Loading
- Outfit Game Test
- Wardrobe Unit Tests
- Resident Skin Baking
- Animation Pack Game Test
- Resident Model Imports
- Village Pool Compiler
- Village Layout Simulation
- Saved Companion Codecs
- Project Docs Index
- Resident Names and Identity
- Resident Bonds
- Roofs and Windows
- Animation Preview Renderer
- Resident Name Pools
- Foundation Blocks
- Friendship and Gallery Tests
- Guard Game Test
- Structures Game Test
- Medical Treatment
- Eye Styles and Blink Geometry
- Face Swatch Colors
- Procedural Village Design
- Animation Film Assembly
- Gaits and Always-On Motion
- Foundation Game Test
- Guard Damage Credit
- Animation Game Test
- Outfit Preview Screen
- Animation Pack Unit Tests
- Outfit Engine Verification
- Starlit and Soft Glint Faces
- Phase 1 Registry Foundation
- Village Items
- Animation Pack Mechanics
- Foundation Entity Blocks
- Room and Foundation Catalogs
- Animation Track Curves
- Face and Hair Unit Tests
- Guard Spawn Egg Test
- Resident Model Planes
- Meals and Wearables
- Body Parts
- Animation Showcase Screen
- Block Entity Registry
- Block Registry
- Hair and Face Game Test
- Village Layout Config
- Outfit Atlas Layout
- Village Professions
- Client Initializer
- Garment Piece Motions

## God Nodes (most connected - your core abstractions)
1. `k()` - 115 edges
2. `Build` - 77 edges
3. `solid()` - 57 edges
4. `GuardController` - 47 edges
5. `Profession` - 46 edges
6. `Face` - 44 edges
7. `VillageFriends` - 41 edges
8. `Outfit` - 38 edges
9. `FriendshipScreen` - 35 edges
10. `Garment` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Typed Conversation Dialogue` --references--> `FriendshipScreen`  [INFERRED]
  CHANGELOG.md → src/client/java/dev/villagefriends/client/FriendshipScreen.java
- `-PanimationsOnly Game Test` --references--> `AnimationGameTest`  [INFERRED]
  ANIMATION_EDITING.md → src/gametest/java/dev/villagefriends/AnimationGameTest.java
- `Focused Client GameTest Flags` --references--> `FriendshipGameTest`  [AMBIGUOUS]
  DEVELOPMENT.md → src/gametest/java/dev/villagefriends/FriendshipGameTest.java
- `Guard Spawn Egg Verification (2.10.1)` --references--> `GuardSpawnEggGameTest`  [INFERRED]
  VERIFICATION.md → src/gametest/java/dev/villagefriends/GuardSpawnEggGameTest.java
- `-PhairFacesOnly Game Test` --references--> `HairFaceGameTest`  [INFERRED]
  OUTFIT_ENGINE.md → src/gametest/java/dev/villagefriends/HairFaceGameTest.java

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Phase 1 Foundation Registration Sequence** — src_main_java_dev_villagefriends_villagefoundation_villagefoundation, src_main_java_dev_villagefriends_villageblocks_villageblocks, src_main_java_dev_villagefriends_villageitems_villageitems, src_main_java_dev_villagefriends_villageblockentities_villageblockentities, src_main_java_dev_villagefriends_villageprofessions_villageprofessions [INFERRED 0.85]
- **Village Building Pipeline (design -> blueprint -> NBT)** — building_editing_design_programs, tools_design_village, building_editing_layered_blueprints, tools_create_village_structures, building_editing_village_layout_json [EXTRACTED 1.00]
- **Guard Progression Architecture** — src_main_java_dev_villagefriends_guardprogress_guardprogress, src_main_java_dev_villagefriends_guarddamageledger_guarddamageledger, src_main_java_dev_villagefriends_guardprogression_guardprogression, guards_guard_progression, guards_damage_based_xp_credit [EXTRACTED 1.00]
- **Wardrobe Rendering Pipeline (bake, atlas, pose worn pieces)** — src_client_java_dev_villagefriends_client_residentskins_residentskins, src_client_java_dev_villagefriends_client_outfitatlas_outfitatlas, src_client_java_dev_villagefriends_client_wardrobelayer_wardrobelayer, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, outfit_engine_palette_lock [EXTRACTED 1.00]
- **Profession Outfit Assembly** — src_main_java_dev_villagefriends_outfit_outfitfactory_outfitfactory, src_main_java_dev_villagefriends_outfit_wardrobe_wardrobe, outfit_engine_outfit_templates, outfit_engine_mix_and_match, outfit_engine_locked_sets, outfit_engine_natural_hair_colors [EXTRACTED 1.00]
- **Resident Clip Posing Flow (director, library, poser, models)** — src_client_java_dev_villagefriends_client_residentlife_residentlife, src_main_java_dev_villagefriends_animation_animationlibrary_animationlibrary, src_client_java_dev_villagefriends_client_residentposer_residentposer, src_client_java_dev_villagefriends_client_residentanimation_residentanimation, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, src_client_java_dev_villagefriends_client_residentarmormodel_residentarmormodel [EXTRACTED 1.00]

## Communities (111 total, 38 thin omitted)

### Community 0 - "Women's Garment Kit"
Cohesion: 0.03
Nodes (33): belt(), arm_rings(), bells(), buttons(), cuffs(), dags(), fur(), fur_box() (+25 more)

### Community 1 - "Casual Garment Kit"
Cohesion: 0.05
Nodes (41): arm_bone(), arm_x(), body(), chest_pocket(), collar_points(), crew_neck(), jeans(), leather_belt() (+33 more)

### Community 2 - "Women's Anime Hair Kit"
Cohesion: 0.05
Nodes (38): aim(), axis(), braid(), braided_bun(), bubble_face(), bun(), _caps(), coil_face() (+30 more)

### Community 3 - "Friendship Screen and Payloads"
Cohesion: 0.06
Nodes (5): ConversationButton, FriendshipScreen, RoadmapGameTest, ActionPayload, FriendshipPayload

### Community 4 - "Mod Init and Companions"
Cohesion: 0.14
Nodes (6): 2.0.0: Friendship, stories and companions, CompanionController, Outing, Choice, NarrativeEngine, VillageFriends

### Community 5 - "Men's Anime Hair Kit"
Cohesion: 0.05
Nodes (30): Supreme Casual Line (t101-t120, b101-b120), Wardrobe Python Module Pipeline (tools/wardrobe), back_fan(), bangs(), cel_box(), cel_face(), lock(), chain() (+22 more)

### Community 6 - "Civic and Trade Buildings"
Cohesion: 0.09
Nodes (26): apothecary(), chapel(), crenellate(), garrison(), grave(), library(), market_garden(), market_stalls() (+18 more)

### Community 7 - "Village Build Kit and Farms"
Cohesion: 0.05
Nodes (16): cart(), haystack(), tree_birch(), well(), woodpile(), apiary(), farm_beets(), farm_mixed() (+8 more)

### Community 8 - "Men's Garment Kit"
Cohesion: 0.04
Nodes (26): arm_blk(), back_drape(), bare_feet(), blk(), check(), embroider(), flecks(), fur() (+18 more)

### Community 9 - "Previews and Voice Synthesis"
Cohesion: 0.08
Nodes (24): Conversation Window (Talk/Story/Journal/Time/Travel tabs), Wordless Human-like Hum Voices, Dialogue, envelope(), finish(), glottal(), hum(), make_ui() (+16 more)

### Community 10 - "Mixins and Guard Hooks"
Cohesion: 0.09
Nodes (10): Guard Equipment Exchange (Equip held item), Initial Guard Equipment (UUID-selected iron/chainmail), Adventure Companions (Follow/Wait/Return home), VillagerEventMixin, CompanionPortalMixin, GuardArmorMixin, GuardArrowMixin, GuardMeleeMixin (+2 more)

### Community 11 - "Wardrobe Compiler"
Cohesion: 0.08
Nodes (25): build(), build_all(), catalog(), compatible(), Garment, hex_rgb(), json_text(), key_rgba() (+17 more)

### Community 12 - "Guard Combat Controller"
Cohesion: 0.12
Nodes (8): Unlimited Safe Archer Arrows, Automatic Village Defense (Knights and Archers), villager_predators Entity Tag, Combat, GuardController, Incident, RecentAttack, Probe

### Community 13 - "Pixel Painting Helpers"
Cohesion: 0.06
Nodes (20): checks(), lacing(), scatter(), band(), button(), cloth_shade(), curls_box(), dark_seams() (+12 more)

### Community 15 - "Professions and Resident Sample"
Cohesion: 0.06
Nodes (32): Resident, ResidentSampleGameTest, Profession, ADVENTURER, APOTHECARY, ARCHER, ARMORER, BARD (+24 more)

### Community 16 - "Animation Clip Authoring"
Cohesion: 0.05
Nodes (5): Python Clip Authoring (mirror-friendly kit), Village Life Pack, _channel_value(), Clip, sine()

### Community 17 - "Village Streets"
Cohesion: 0.08
Nodes (21): lamp_bench(), avenue(), avenue_bend(), bend_left(), bend_right(), crossroads(), end_fade(), end_gate() (+13 more)

### Community 18 - "Outfit Engine Concepts"
Cohesion: 0.08
Nodes (31): 2.11.0: Men's and women's wardrobes, 2.7.0: Sims-style wardrobe, 2.8.0: Casual medieval and anime hair expansion, 3D Pieces (box-UV cuboids on bones), Anime-Inspired Hairstyles, Appearance Recipe (outfitN:complexion:GENDER:PALETTE_ID:seed), Denim Material Role, Gendered Wardrobe Lookup and Fallback (+23 more)

### Community 19 - "Plazas and Village Greens"
Cohesion: 0.10
Nodes (22): flowerbed(), tree_oak(), base(), bell_frame(), big_oak(), _dir(), fountain(), fountain_square() (+14 more)

### Community 20 - "Building Parts Library"
Cohesion: 0.08
Nodes (18): block(), along(), beam_ring(), bench(), door_cells(), floor(), foundation(), hanging_lamp_post() (+10 more)

### Community 21 - "Tool Entry Points"
Cohesion: 0.11
Nodes (15): Building Design Programs (DESIGNS = {name: function}), build(), load(), main(), validate(), main(), main(), unique() (+7 more)

### Community 23 - "Outfit Palettes and Hair Colors"
Cohesion: 0.10
Nodes (4): ColorPalette, Garment, HairColor, Outfit

### Community 24 - "Wardrobe 3D Piece Layer"
Cohesion: 0.12
Nodes (7): ResidentArmorModel, Baked, Shown, WardrobeLayer, Piece, Vec3, Men's and Women's Wardrobe Verification (2.11.0)

### Community 26 - "Animation Pack Loading"
Cohesion: 0.12
Nodes (8): AnimationLayer, AnimationClip, Mirror, FREE, HAND, NEVER, AnimationLibrary, AnimationPack

### Community 27 - "Village Settlements"
Cohesion: 0.15
Nodes (4): CommunityGameTest, VillageBook, VillageRecord, VillageSettlements

### Community 29 - "Block Entity Hooks"
Cohesion: 0.13
Nodes (6): Patrols, Command Desk Controls and Shields (future), Empty Block Entity Integration Hooks, ApothecaryCotBlockEntity, CommandDeskBlockEntity, HousePlaqueBlockEntity, NoticeBoardBlockEntity

### Community 30 - "Friendship State and History"
Cohesion: 0.12
Nodes (5): Per-Player Co-op Relationship State, FriendshipBook, FriendshipState, SharedHistory, FriendshipTest

### Community 31 - "Garment Trims and Accessories"
Cohesion: 0.08
Nodes (16): bow(), flower(), tie(), tie(), brooch(), cloak(), collar_flat(), hanging() (+8 more)

### Community 34 - "Gendered Wardrobe Selection"
Cohesion: 0.13
Nodes (6): Gender, FEMALE, MALE, NON_BINARY, OutfitFactory, OutfitEngineTest

### Community 37 - "Animation Director and Packs"
Cohesion: 0.11
Nodes (16): Activity and Reaction Layers, villagefriends:temperament Synced Attachment, Animation Pack, Animation Clip, Clip Triggers (idle, chat, greet, talk, reactions, hurt), Clip Eligibility Tags, Left-Handed Mirroring, Animation Pack JSON Format (format 1) (+8 more)

### Community 38 - "Animation Film Capture"
Cohesion: 0.18
Nodes (3): AnimationCast, Role, AnimationFilmGameTest

### Community 40 - "Resident Clip Posing"
Cohesion: 0.12
Nodes (10): ResidentPoser, Bone, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG (+2 more)

### Community 42 - "Homes and Cottages"
Cohesion: 0.18
Nodes (13): cottage(), family_house(), farmhouse(), garden(), kitchen(), path(), tall_house(), townhouse() (+5 more)

### Community 43 - "Guard Policy and Gifts"
Cohesion: 0.10
Nodes (10): 2.9.0: Knight and Archer defense, Friendship Forgiveness for Player Hits, Gifts and Promises, Relationship Tiers (New Neighbor to Best Friend), Milestone 7: Romance and Family (future), Shared Activities (Walk, Picnic, Exploration, Gathering), GiftPreferences, GuardPolicy (+2 more)

### Community 44 - "Foundation Asset Generators"
Cohesion: 0.14
Nodes (11): Foundation Asset Generation Pipeline, boxes(), icon(), merge(), recipe(), save(), tag(), save() (+3 more)

### Community 45 - "Resident Look Recipes"
Cohesion: 0.11
Nodes (12): PaletteID, ASH_AND_TEAL, DESERT_SUN, FOREST_AND_HEARTH, ROYAL_VELVET, RUSTIC_TWEED, SAGE_AND_TERRACOTTA, SCHOLARLY_PLUM (+4 more)

### Community 46 - "Resident Render State"
Cohesion: 0.16
Nodes (3): ResidentAnimation, ResidentRenderer, ResidentRenderState

### Community 47 - "Narrative Content Packs"
Cohesion: 0.17
Nodes (8): Narrative Content Pack (content.json), Four-Chapter Personal Stories, Conditions, Data, NarrativeContent, Personality, Request, Story

### Community 48 - "Gaits and Blinking"
Cohesion: 0.16
Nodes (3): AnimationPreviewScreen, ResidentMotion, ResidentMotionTest

### Community 49 - "Block State Helpers"
Cohesion: 0.20
Nodes (13): bid(), can_take(), stairs_at(), full_cube(), gate_connects(), is_fence(), is_gate(), is_pane() (+5 more)

### Community 50 - "Structure Template Compiler"
Cohesion: 0.14
Nodes (4): Byte, state(), Template, plain()

### Community 51 - "Skirts and Pleats"
Cohesion: 0.10
Nodes (5): band(), pleats(), Skirt, tier(), trim()

### Community 52 - "Guard Level Progress"
Cohesion: 0.15
Nodes (4): 2.10.0: Guard progression, GuardProgress, GuardProgressTest, Guard Progression Verification (2.10.0)

### Community 53 - "Wardrobe Catalog Loading"
Cohesion: 0.15
Nodes (5): Kind, BOTTOM, HAIR, TOP, Wardrobe

### Community 54 - "Outfit Game Test"
Cohesion: 0.22
Nodes (3): Locked One-Piece Outfits (locked_to), OutfitGameTest, OutfitTemplate

### Community 55 - "Wardrobe Unit Tests"
Cohesion: 0.16
Nodes (5): Fit, FEMALE, MALE, UNISEX, WardrobeTest

### Community 56 - "Resident Skin Baking"
Cohesion: 0.13
Nodes (3): Entry, Loaded, ResidentSkins

### Community 59 - "Village Pool Compiler"
Cohesion: 0.19
Nodes (12): Layered JSON Blueprints (tools/village_blueprints), 2.4.0: Phase 2 village structures, check_lot(), location(), main(), payload(), pool(), pool_name() (+4 more)

### Community 60 - "Village Layout Simulation"
Cohesion: 0.18
Nodes (14): Village Layout Simulation, In-Game Village Gallery (-PvillageGallery), Procedural Plains Villages, assemble(), draw(), load(), main(), overlaps() (+6 more)

### Community 63 - "Project Docs Index"
Cohesion: 0.23
Nodes (14): ANIMATION_EDITING.md (Resident movement, animation packs and eyes), ANIMATION_PACKS.md (Resident animation packs), Editing the Plains Village, Village Friends Developer Handoff, Knights and Archers Guide, OUTFIT_ENGINE.md (Wardrobe and outfit engine), Phase 1 Implementation: Registry & Item Foundation, Phase 2 Structures: Worldgen & Structures (+6 more)

### Community 64 - "Resident Names and Identity"
Cohesion: 0.15
Nodes (5): 2.1.0: Children, village names and Village Marker, Persistent Resident Identity (stable ID), ResidentProfile, VillageNames, CommunityTest

### Community 65 - "Resident Bonds"
Cohesion: 0.21
Nodes (3): Resident-to-Resident Connections, BondBook, BondState

### Community 66 - "Roofs and Windows"
Cohesion: 0.14
Nodes (5): is_air(), gable_roof(), put(), plinth_skirt(), window()

### Community 67 - "Animation Preview Renderer"
Cohesion: 0.18
Nodes (8): draw(), load_pack(), main(), pose(), render_frame(), Resident, sample(), Track

### Community 68 - "Resident Name Pools"
Cohesion: 0.22
Nodes (5): 2.5.0: Codex Phase 3 compositor and name import, Editable Name Pools (tools/name_pools.json), Data, Pool, ResidentNames

### Community 73 - "Medical Treatment"
Cohesion: 0.16
Nodes (8): Future Real-Time Knockout Controller, Medical Treatment Contract, Downed Companion Rescue, MedicalSupplyItem, Treatment, BANDAGE_WRAP, REVIVAL_TONIC, SMELLING_SALTS

### Community 74 - "Eye Styles and Blink Geometry"
Cohesion: 0.25
Nodes (3): EyeStyle, SOFT_GLINT, STARLIT

### Community 77 - "Procedural Village Design"
Cohesion: 0.21
Nodes (13): Civic Slots (priority 5), Village Design Kit (kit.py, parts.py, roads.py), Lot Contract (building_entrance jigsaw), Lots (homes, workshops, decorations, empty gaps), Village Jigsaw Graph, Native Trade Sets (50 sets, 100 offers), Ten New Professions and Workstations, Six Guaranteed Civic Buildings (+5 more)

### Community 78 - "Animation Film Assembly"
Cohesion: 0.22
Nodes (8): card(), font(), main(), emit(), fade(), hold(), play(), scene_frames()

### Community 79 - "Gaits and Always-On Motion"
Cohesion: 0.15
Nodes (12): Always-On Motion Layer, -PanimationsOnly Game Test, Six Gait Styles, Shared Gait Function (resident and armor models), Living Villagers (walking styles, breathing, articulated eyes), Gait, CURIOUS, EASY (+4 more)

### Community 81 - "Guard Damage Credit"
Cohesion: 0.26
Nodes (6): Combat Profession Lock, Damage-Based Guard XP Credit, Guard Level Progression (0-50), GuardDamageLedger, Hit, Credit

### Community 83 - "Outfit Preview Screen"
Cohesion: 0.19
Nodes (8): Cell, OutfitPreviewScreen, View, BACK, FRONT, HEAD, HEAD_BACK, WALK

### Community 85 - "Outfit Engine Verification"
Cohesion: 0.17
Nodes (10): Male Asset Registry Phase 2, Male Starter Set and Texture Overhaul, Outfit Engine Rebuild, 2.2.0: Glasses and profession clothing, Armor Hiding of Wardrobe Pieces, -PoutfitsOnly Game Test, Per-Outfit Skin Baking, Male Asset Registry Phase 2 Verification (+2 more)

### Community 86 - "Starlit and Soft Glint Faces"
Cohesion: 0.23
Nodes (8): Face Detail Swatches (64..71, 0), Masculine and Feminine Face Details, Soft Glint Eyes, Starlit Eyes, Unreleased: Starlit and Soft Glint faces, -PhairFacesOnly Game Test, Living Eyes (protected eye row), Starlit and Soft Glint Faces Verification

### Community 88 - "Phase 1 Registry Foundation"
Cohesion: 0.17
Nodes (11): 2.10.1: Guard spawn eggs, 2.3.0: Phase 1 foundation, Phase 1 Foundation Gameplay Verification, Master Specification (Codex roadmap), 17 New Foundation Blocks, Registration Order (blocks, items, block entities, professions), Codex Phase 1: Registry & Item Foundation, Phase 2 Structures Verification (+3 more)

### Community 90 - "Animation Pack Mechanics"
Cohesion: 0.27
Nodes (8): -PanimationPack Game Test, Blink and Glance Mechanics, Clip Pose Layering Order (limbs, waist, root), Root Bone, Animation Tracks (bone.rot, bone.pos, eyes.lid, eyes.look), Waist Bone, 2.6.0: Gaits, breathing and articulated eyes, Village Life Animation Pack Verification (2.12.0)

### Community 91 - "Foundation Entity Blocks"
Cohesion: 0.24
Nodes (6): FoundationEntityBlock, Kind, APOTHECARY_COT, COMMAND_DESK, HOUSE_PLAQUE, NOTICE_BOARD

### Community 92 - "Room and Foundation Catalogs"
Cohesion: 0.24
Nodes (4): Foundation Catalog (foundation-catalog.json), Future Spatial Bed Scanner, Room/Structure Catalog (structure-catalog.json), designs()

### Community 97 - "Meals and Wearables"
Cohesion: 0.25
Nodes (4): Bread, Stew and Coffee Consumables, 24 New Items and 41 Recipes, Wearable Uniforms and Rain Gear, VillageMealItem

### Community 98 - "Body Parts"
Cohesion: 0.25
Nodes (7): BodyPart, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG, TORSO

### Community 99 - "Animation Showcase Screen"
Cohesion: 0.38
Nodes (3): -PanimationVideo Showcase, AnimationShowcaseScreen, Cell

### Community 103 - "Village Layout Config"
Cohesion: 0.33
Nodes (6): Replacement Pools and required_pools, Structure Processors (worn roads, plank bridges, weathered stone), Village Layout Config (tools/village_layout.json, format 2), Random-Spread Structure Placement, Hometown Names and Settlements, Village Marker

### Community 107 - "Garment Piece Motions"
Cohesion: 0.40
Nodes (5): Motion, FLAP_BACK, FLAP_FRONT, NONE, SWAY

## Ambiguous Edges - Review These
- `FriendshipGameTest` → `Focused Client GameTest Flags`  [AMBIGUOUS]
  DEVELOPMENT.md · relation: references
- `GuardArmorMixin` → `Initial Guard Equipment (UUID-selected iron/chainmail)`  [AMBIGUOUS]
  GUARDS.md · relation: references

## Knowledge Gaps
- **102 isolated node(s):** `Loaded`, `FRONT`, `BACK`, `HEAD`, `HEAD_BACK` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 745 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `FriendshipGameTest` and `Focused Client GameTest Flags`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Wardrobe Python Module Pipeline (tools/wardrobe)` connect `Men's Anime Hair Kit` to `Women's Garment Kit`, `Casual Garment Kit`, `Women's Anime Hair Kit`, `Men's Garment Kit`, `Wardrobe Compiler`, `Tool Entry Points`, `Outfit Game Test`, `Project Docs Index`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **What connects `Loaded`, `FRONT`, `BACK` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Women's Garment Kit` be split into smaller, more focused modules?**
  _Cohesion score 0.03425925925925926 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `GuardArmorMixin` and `Initial Guard Equipment (UUID-selected iron/chainmail)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `WARDROBE_EDITING.md (Editing the wardrobe)` connect `Project Docs Index` to `Previews and Voice Synthesis`, `Outfit Engine Concepts`, `Outfit Engine Verification`, `Men's Anime Hair Kit`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Should `Casual Garment Kit` be split into smaller, more focused modules?**
  _Cohesion score 0.04828504828504829 - nodes in this community are weakly interconnected._