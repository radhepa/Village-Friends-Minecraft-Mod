# Graph Report - homes-and-deeds  (2026-10-08)

## Corpus Check
- 421 files · ~572,879 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .properties 2, .jar 1)

## Summary
- 7140 nodes · 20807 edges · 401 communities (157 shown, 244 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 1284 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82136fd0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Face
- kit_casual.py
- anime_female.py
- FriendshipScreen
- .bond
- anime_male.py
- workstations/paint.py
- Build
- kit_male.py
- numpy
- net.minecraft.server.level.ServerPlayer
- wardrobe.py
- net.minecraft.world.entity.LivingEntity
- wardrobe/paint.py
- list
- Profession
- Clip
- taiga/core_parts.py
- org.junit.jupiter.api.Test
- math
- snowy/civic.py
- design_village.py
- desert/homes.py
- Notice
- Outfit
- AnimationClip
- workstations.py
- Taverns
- BondState
- kit_female.py
- DialogueBank
- VillageMarkerBlock
- Wardrobe
- TavernClient.java
- AnimationPackTest
- ResidentLife
- snowy/homes_kit.py
- Bone
- parts.py
- kit_m04.py
- celebration_assets.py
- random
- ResidentRenderState
- ResidentNames
- ResidentMotion
- is_air
- Template
- Skirt
- GuardProgress
- .assembleOutfit
- .runTest
- VERIFICATION.md
- ResidentSkins
- identifier
- net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext
- desert/core_parts.py
- simulate.py
- net.minecraft.server.level.ServerLevel
- Village Friends README
- .runTest
- NoticeBoardScreen
- House
- animations/preview.py
- Patronage
- net.minecraft.core.BlockPos
- kit_m07.py
- Society
- StructuresGameTest
- net.minecraft.world.entity.Entity
- Deeds
- .texture
- VillageItems.java
- Procedural Plains Village (villagefriends:village)
- pathlib
- Townsfolk
- DeedLog
- homes_logs.py
- .runTest
- View
- VillagerPets
- CHANGELOG.md
- LedgerScreen
- VillageSocieties
- Block
- net.minecraft.world.item.Item
- Calendar
- net.minecraft.world.level.block.state.BlockState
- kit_m01.py
- AnimationTrack
- Chemistry
- .runTest
- ResidentModel
- furniture.py
- Wardrobe Python Module Pipeline (tools/wardrobe)
- kit_f04.py
- SocietyTest
- WolfPoseMixin.java
- Deed
- .runTest
- .affinity
- wardrobe/kit.py
- Emote
- .perform
- net.minecraft.world.item.ItemStack
- kit_m03.py
- Board
- kit_f07.py
- ResidentRoutines
- .onInitializeClient
- taiga/civic.py
- Station
- Dialogue
- org.spongepowered.asm.mixin.injection.Inject
- net.minecraft.client.gui.components.Button
- HouseSurvey
- kit_m05.py
- tavern_preview.py
- kit_f03.py
- net.minecraft.world.entity.npc.villager.Villager
- kit_f02.py
- Weather
- re
- rot_matrix
- net.fabricmc.api.ClientModInitializer
- shade
- kit_m06.py
- HouseCatalog
- json
- kit_m10.py
- Override
- kit_m08.py
- argparse
- kit_f01.py
- kit_f06.py
- HousePlaqueBlock.java
- Treatment
- kit_m02.py
- .book
- arm_blk
- leg_blk
- kit_f05.py
- .living
- .runTest
- back_drape
- bare_feet
- check
- flecks
- PetKeeping
- hood_down
- lacing
- lozenge
- mail
- toggles
- tartan
- net.minecraft.world.level.block.Block
- tippets
- kit_f10.py
- skirt_panels
- wraps
- stripes
- toe_pieces
- How a batch is built
- textures
- VillageProfessions.java
- .runTest
- Games
- create_village_structures.py
- PetScreen
- DeedKind
- Playground
- net.minecraft.world.entity.schedule.Activity
- dining.py
- notice_board.py
- PetTrick
- seated.py
- chat.py
- bar.py
- FoundationPreviewScreen
- org.spongepowered.asm.mixin.Mixin
- Move
- VillageStructure
- FoundationEntityBlock
- embroider
- VillageVegetationMixin.java
- .fromPlaque
- .start
- HousingAssignmentsTest
- PetProfile
- pets/preview.py
- net.minecraft.world.phys.Vec3
- .mention
- HousePlaqueBlockEntity
- net.minecraft.client.model.geom.ModelPart
- .runTest
- PlayTest
- .runTest
- .runTest
- .runTest
- PlaygroundGameTest
- Trick
- Move
- VillageSurveyGameTest
- Bone
- PetGoal
- Residents' pets
- Game
- Concepts
- How the director chooses
- .box
- point
- GuardMeleeMixin.java
- KnockoutState
- .randomVariant
- FelinePoseMixin.java
- staves
- games.py
- Fit
- Motion
- flower
- render
- GiftPreferences
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `Build` - 259 edges
2. `Society` - 99 edges
3. `VillagerPets` - 84 edges
4. `is_air()` - 83 edges
5. `Deeds` - 71 edges
6. `Townsfolk` - 65 edges
7. `Homes` - 62 edges
8. `Taverns` - 62 edges
9. `House` - 61 edges
10. `ring()` - 60 edges

## Surprising Connections (you probably didn't know these)
- `Focused Client GameTest Flags` --references--> `FriendshipGameTest`  [AMBIGUOUS]
  DEVELOPMENT.md → src/gametest/java/dev/villagefriends/FriendshipGameTest.java
- `Phase 2 Structures Verification` --references--> `StructuresGameTest`  [INFERRED]
  PHASE2.md → src/gametest/java/dev/villagefriends/StructuresGameTest.java
- `In-Game Village Gallery (-PvillageGallery)` --references--> `VillageGalleryGameTest`  [INFERRED]
  BUILDING_EDITING.md → src/gametest/java/dev/villagefriends/VillageGalleryGameTest.java
- `Initial Guard Equipment (UUID-selected iron/chainmail)` --references--> `GuardController`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardController.java
- `Combat Profession Lock` --references--> `GuardProgression`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardProgression.java

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Resident Clip Posing Flow (director, library, poser, models)** — src_client_java_dev_villagefriends_client_residentlife_residentlife, src_main_java_dev_villagefriends_animation_animationlibrary_animationlibrary, src_client_java_dev_villagefriends_client_residentposer_residentposer, src_client_java_dev_villagefriends_client_residentanimation_residentanimation, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, src_client_java_dev_villagefriends_client_residentarmormodel_residentarmormodel [EXTRACTED 1.00]
- **Village Building Pipeline (design -> blueprint -> NBT)** — building_editing_design_programs, tools_design_village, building_editing_layered_blueprints, tools_create_village_structures, building_editing_village_layout_json [EXTRACTED 1.00]
- **Guard Progression Architecture** — src_main_java_dev_villagefriends_guardprogress_guardprogress, src_main_java_dev_villagefriends_guarddamageledger_guarddamageledger, src_main_java_dev_villagefriends_guardprogression_guardprogression, guards_guard_progression, guards_damage_based_xp_credit [EXTRACTED 1.00]
- **Wardrobe Rendering Pipeline (bake, atlas, pose worn pieces)** — src_client_java_dev_villagefriends_client_residentskins_residentskins, src_client_java_dev_villagefriends_client_outfitatlas_outfitatlas, src_client_java_dev_villagefriends_client_wardrobelayer_wardrobelayer, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, outfit_engine_palette_lock [EXTRACTED 1.00]
- **Phase 1 Foundation Registration Sequence** — src_main_java_dev_villagefriends_villagefoundation_villagefoundation, src_main_java_dev_villagefriends_villageblocks_villageblocks, src_main_java_dev_villagefriends_villageitems_villageitems, src_main_java_dev_villagefriends_villageblockentities_villageblockentities, src_main_java_dev_villagefriends_villageprofessions_villageprofessions [INFERRED 0.85]

## Communities (401 total, 244 thin omitted)

### Community 0 - "Face"
Cohesion: 0.08
Nodes (7): lozenges(), overlay_dags(), sub(), tartan(), grid(), Face, Layer

### Community 1 - "kit_casual.py"
Cohesion: 0.06
Nodes (17): chest_pocket(), collar_points(), crew_neck(), jeans(), leather_belt(), long_sleeves(), placket(), plain_tee() (+9 more)

### Community 2 - "anime_female.py"
Cohesion: 0.07
Nodes (23): aim(), braided_bun(), bubble_face(), bun(), _caps(), coil_face(), combed(), curve() (+15 more)

### Community 3 - "FriendshipScreen"
Cohesion: 0.12
Nodes (3): DockButton, FriendshipScreen, ReplyButton

### Community 4 - ".bond"
Cohesion: 0.09
Nodes (5): WorkstationGameTest, Choice, NarrativeEngine, Question, TalkWorld

### Community 5 - "anime_male.py"
Cohesion: 0.06
Nodes (18): clipped(), clipped_scalp(), coil_face(), combed_face(), cornrow(), cornrow_path(), fade(), loc_face() (+10 more)

### Community 6 - "workstations/paint.py"
Cohesion: 0.12
Nodes (22): archives_front(), arrow(), barrel_end(), blank(), bolt_end(), bottle(), cabinet_front(), candle() (+14 more)

### Community 7 - "Build"
Cohesion: 0.02
Nodes (74): cart(), flowerbed(), haystack(), lamp_bench(), tree_birch(), tree_oak(), well(), woodpile() (+66 more)

### Community 8 - "kit_male.py"
Cohesion: 0.13
Nodes (6): fur(), fur_face(), herringbone(), ribbing(), sash(), shoulder_cape()

### Community 9 - "numpy"
Cohesion: 0.11
Nodes (21): envelope(), finish(), glottal(), hum(), make_ui(), make_voice(), resonator(), voiced() (+13 more)

### Community 10 - "net.minecraft.server.level.ServerPlayer"
Cohesion: 0.09
Nodes (4): Quest, QuestLog, Words, VillageQuests

### Community 11 - "wardrobe.py"
Cohesion: 0.09
Nodes (25): build(), build_all(), catalog(), compatible(), Garment, hex_rgb(), json_text(), key_rgba() (+17 more)

### Community 12 - "net.minecraft.world.entity.LivingEntity"
Cohesion: 0.06
Nodes (15): The deeds, Friendship Forgiveness for Player Hits, Unlimited Safe Archer Arrows, Automatic Village Defense (Knights and Archers), villager_predators Entity Tag, Gifts and Promises, GuardProgressGameTest, Combat (+7 more)

### Community 13 - "wardrobe/paint.py"
Cohesion: 0.08
Nodes (21): band(), button(), cap(), cloth_shade(), curls_box(), curls_face(), dark_seams(), fabric() (+13 more)

### Community 15 - "Profession"
Cohesion: 0.06
Nodes (33): Focused Client GameTest Flags, Resident, ResidentSampleGameTest, Profession, ADVENTURER, APOTHECARY, ARCHER, ARMORER (+25 more)

### Community 16 - "Clip"
Cohesion: 0.15
Nodes (3): _channel_value(), Clip, register()

### Community 17 - "taiga/core_parts.py"
Cohesion: 0.02
Nodes (62): road(), _iron_chains(), square(), stone(), market_paving(), paving(), road(), end_gate() (+54 more)

### Community 18 - "org.junit.jupiter.api.Test"
Cohesion: 0.08
Nodes (9): Village Friends 2.17.0 — Guard duty and knockouts, CommunityTest, FriendshipTest, GuardDutyTest, GuardPolicyTest, RoadmapTest, RoutineTest, Where things live (+1 more)

### Community 19 - "math"
Cohesion: 0.11
Nodes (24): bell_frame(), big_oak(), _dir(), fountain(), fountain_square(), gazebo(), lamp_ring(), market_hall() (+16 more)

### Community 20 - "snowy/civic.py"
Cohesion: 0.05
Nodes (58): apothecary(), chapel(), crow_steps(), gallery_roof(), garrison(), grave(), library(), market_hall() (+50 more)

### Community 21 - "design_village.py"
Cohesion: 0.10
Nodes (14): Building Design Programs (DESIGNS = {name: function}), Layered JSON Blueprints (tools/village_blueprints), Foundation Catalog (foundation-catalog.json), Future Spatial Bed Scanner, Room/Structure Catalog (structure-catalog.json), main(), designs(), checksum() (+6 more)

### Community 22 - "desert/homes.py"
Cohesion: 0.06
Nodes (68): canopy(), cart(), haystack(), palm_pair(), palm_single(), pottery(), well(), cactus_garden() (+60 more)

### Community 23 - "Notice"
Cohesion: 0.13
Nodes (8): Notice, Reward, Gift, HouseNeed, Hunt, Postings, Want, Writer

### Community 24 - "Outfit"
Cohesion: 0.06
Nodes (20): Block, OutfitAtlas, Baked, Shown, WardrobeLayer, BodyPart, HEAD, LEFT_ARM (+12 more)

### Community 26 - "AnimationClip"
Cohesion: 0.08
Nodes (11): Village Life Animation Pack (99 clips), AnimationLayer, AnimationPacks, FoundationGameTest, AnimationClip, Mirror, FREE, HAND (+3 more)

### Community 27 - "workstations.py"
Cohesion: 0.17
Nodes (20): alchemical_press(), archery_target(), archives(), blockstate(), boxes(), check(), designs(), drinks_barrel() (+12 more)

### Community 29 - "Taverns"
Cohesion: 0.12
Nodes (6): Plan, House, Order, Patron, Runner, Taverns

### Community 30 - "BondState"
Cohesion: 0.06
Nodes (11): Per-Player Co-op Relationship State, Relationship Tiers (New Neighbor to Best Friend), Resident-to-Resident Connections, Milestone 7: Romance and Family (future), Shared Activities (Walk, Picnic, Exploration, Gathering), BondBook, BondState, FriendshipBook (+3 more)

### Community 31 - "kit_female.py"
Cohesion: 0.03
Nodes (32): bodice(), buttons(), chemise(), cloak(), collar_flat(), dags(), fur(), fur_box() (+24 more)

### Community 32 - "DialogueBank"
Cohesion: 0.07
Nodes (14): Village Friends 2.14.0 — Village days, working workstations and 5,898 pieces of dialogue, Answer, DialogueBank, Context, Line, Talk, DialogueBankTest, TalkTest (+6 more)

### Community 34 - "Wardrobe"
Cohesion: 0.09
Nodes (7): Village Friends 2.8.0 — Casual medieval and anime hair expansion, Gender, FEMALE, MALE, NON_BINARY, Wardrobe, WardrobeTest

### Community 37 - "AnimationPackTest"
Cohesion: 0.09
Nodes (17): Animation packs, Gaits, Resident movement, animation packs and eyes, Verification, Village Friends 2.15.0 — Village Life grows to 349 clips, Village Friends 2.19.0 — The tavern, AnimationPackTest, TavernPackTest (+9 more)

### Community 38 - "ResidentLife"
Cohesion: 0.05
Nodes (8): Playing, ResidentLife, Nearby, TavernClient, AnimationCast, Role, AnimationFilmGameTest, AnimationPackGameTest

### Community 39 - "snowy/homes_kit.py"
Cohesion: 0.04
Nodes (67): _tavern_common_room(), firewood(), lamp_bench(), snowman(), spruce_grove(), tree_spruce(), crop(), frost_field() (+59 more)

### Community 40 - "Bone"
Cohesion: 0.14
Nodes (10): ResidentPoser, Bone, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG (+2 more)

### Community 42 - "parts.py"
Cohesion: 0.03
Nodes (54): Village Design Kit (kit.py, parts.py, roads.py), Lots (homes, workshops, decorations, empty gaps), Vanilla Trade Workshops, apothecary(), chapel(), crenellate(), garrison(), grave() (+46 more)

### Community 43 - "kit_m04.py"
Cohesion: 0.05
Nodes (18): baldric(), chain(), diag(), hanging(), key_shape(), lamellar(), lames(), leg_prop() (+10 more)

### Community 44 - "celebration_assets.py"
Cohesion: 0.13
Nodes (18): check(), encode(), hat_on_cone(), item(), merged_lang(), outputs(), party_hat(), png() (+10 more)

### Community 45 - "random"
Cohesion: 0.05
Nodes (62): cart(), drying_rack(), haystack(), termite_mound(), tree_acacia(), tree_acacia_twin(), trough(), coop() (+54 more)

### Community 46 - "ResidentRenderState"
Cohesion: 0.11
Nodes (4): PartyHatLayer, Pose, ResidentRenderer, ResidentRenderState

### Community 47 - "ResidentNames"
Cohesion: 0.07
Nodes (15): Editable Name Pools (tools/name_pools.json), Narrative Content Pack (content.json), Four-Chapter Personal Stories, Conditions, Data, NarrativeContent, Personality, Request (+7 more)

### Community 48 - "ResidentMotion"
Cohesion: 0.08
Nodes (14): Shared Gait Function (resident and armor models), Living Villagers (walking styles, breathing, articulated eyes), ResidentAnimation, ResidentArmorModel, AnimationPreviewScreen, Gait, CURIOUS, EASY (+6 more)

### Community 49 - "is_air"
Cohesion: 0.03
Nodes (61): base(), apothecary(), band(), chapel(), garrison(), grave(), library(), market_kraal() (+53 more)

### Community 50 - "Template"
Cohesion: 0.12
Nodes (4): Byte, state(), Template, plain()

### Community 51 - "Skirt"
Cohesion: 0.10
Nodes (5): band(), pleats(), Skirt, tier(), trim()

### Community 52 - "GuardProgress"
Cohesion: 0.09
Nodes (8): Combat Profession Lock, Damage-Based Guard XP Credit, Guard Level Progression (0-50), GuardDamageLedger, Hit, GuardProgress, GuardDamageLedgerTest, GuardProgressTest

### Community 53 - ".assembleOutfit"
Cohesion: 0.04
Nodes (27): Mix and match, Palette lock, Pieces, Professions, Recipes and genders, Rendering, Verification, Wardrobe and outfit engine (+19 more)

### Community 54 - ".runTest"
Cohesion: 0.18
Nodes (5): Locked One-Piece Outfits (locked_to), AnimationShowcaseScreen, Cell, OutfitGameTest, OutfitTemplate

### Community 55 - "VERIFICATION.md"
Cohesion: 0.11
Nodes (15): Village Friends 2.24.0 — Homes and beds, and residents who remember what you did, HouseCatalogTest, Guard defense verification (2.9.0), Guard progression verification (2.10.0), Guard spawn egg verification (2.10.1), Homes and beds, and deeds verification (2.24.0), Male asset registry Phase 2 verification, Male starter texture rebuild verification (+7 more)

### Community 56 - "ResidentSkins"
Cohesion: 0.14
Nodes (3): Entry, Loaded, ResidentSkins

### Community 57 - "identifier"
Cohesion: 0.09
Nodes (11): ActionPayload, EmotePayload, FriendshipPayload, Detail, Entry, LedgerPayload, Tie, LedgerRequestPayload (+3 more)

### Community 58 - "net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext"
Cohesion: 0.07
Nodes (3): TavernVillageGameTest, VillageGalleryGameTest, Routine

### Community 59 - "desert/core_parts.py"
Cohesion: 0.04
Nodes (56): apothecary(), _caravanserai_bar(), _caravanserai_court(), _caravanserai_hall(), _caravanserai_kitchen(), _caravanserai_upstairs(), chapel(), deck() (+48 more)

### Community 60 - "simulate.py"
Cohesion: 0.20
Nodes (15): Village Layout Simulation, Replacement Pools and required_pools, Structure Processors (worn roads, plank bridges, weathered stone), In-Game Village Gallery (-PvillageGallery), Village Layout Config (tools/village_layout.json, format 2), assemble(), draw(), horizontal() (+7 more)

### Community 62 - "net.minecraft.server.level.ServerLevel"
Cohesion: 0.08
Nodes (15): Around the village, Extension points, Homes and beds, House Plaques, Upkeep and performance, Vanilla stays in charge of sleeping, Verification, Snapshot (+7 more)

### Community 63 - "Village Friends README"
Cohesion: 0.24
Nodes (7): Editing the Plains Village, Village Friends Developer Handoff, Knights and Archers Guide, Phase 1 Implementation: Registry & Item Foundation, Phase 2 Structures: Worldgen & Structures, Village Friends README, Village Friends 2.12.0 Fabric Mod

### Community 64 - ".runTest"
Cohesion: 0.07
Nodes (7): Persistent Resident Identity (stable ID), CommunityGameTest, FriendshipGameTest, KnockoutGameTest, CompanionState, ResidentAppearance, ResidentProfile

### Community 65 - "NoticeBoardScreen"
Cohesion: 0.11
Nodes (4): NoticeBoardScreen, Card, NoticeBoardPayload, Task

### Community 66 - "House"
Cohesion: 0.07
Nodes (16): Saves, Who sleeps where, Assignments, Unit, Bed, House, Kind, FOUND (+8 more)

### Community 67 - "animations/preview.py"
Cohesion: 0.17
Nodes (8): draw(), load_pack(), main(), pose(), render_frame(), Resident, sample(), Track

### Community 68 - "Patronage"
Cohesion: 0.09
Nodes (18): Choice, Kind, ARMCHAIR, BENCH, CHAIR, STOOL, Mood, Neighbor (+10 more)

### Community 69 - "net.minecraft.core.BlockPos"
Cohesion: 0.14
Nodes (4): Spot, Stand, Tavern, TavernSurvey

### Community 70 - "kit_m07.py"
Cohesion: 0.07
Nodes (13): baldric(), coil(), disc(), dust(), hang(), leg_shell(), outer(), ring_marks() (+5 more)

### Community 71 - "Society"
Cohesion: 0.10
Nodes (4): News, Society, SocietyBook, Tie

### Community 74 - "Deeds"
Cohesion: 0.10
Nodes (4): Deeds, Pair, Place, Tally

### Community 75 - ".texture"
Cohesion: 0.10
Nodes (9): Eyes and face, HairFaceGameTest, EyeStyle, SOFT_GLINT, STARLIT, FaceDetails, HandcraftedFaceTest, Starlit and Soft Glint faces verification (2.13.0) (+1 more)

### Community 77 - "Procedural Plains Village (villagefriends:village)"
Cohesion: 0.19
Nodes (13): Civic Slots (priority 5), Lot Contract (building_entrance jigsaw), Village Jigsaw Graph, Master Specification (Codex roadmap), Native Trade Sets (50 sets, 100 offers), Ten New Professions and Workstations, Six Guaranteed Civic Buildings, Enclosed Bedrooms (+5 more)

### Community 78 - "pathlib"
Cohesion: 0.22
Nodes (8): card(), font(), main(), emit(), fade(), hold(), play(), scene_frames()

### Community 80 - "DeedLog"
Cohesion: 0.07
Nodes (14): Changing it, Deeds: residents remember what you did, Prices: one engine (the decision), Residents bring it up, Standing, Where things live, Who knows, DeedBook (+6 more)

### Community 81 - "homes_logs.py"
Cohesion: 0.04
Nodes (21): berry_bush(), chair(), chimney(), door(), drying_rack(), fern(), hearth(), lantern_post() (+13 more)

### Community 83 - "View"
Cohesion: 0.19
Nodes (8): Cell, OutfitPreviewScreen, View, BACK, FRONT, HEAD, HEAD_BACK, WALK

### Community 84 - "VillagerPets"
Cohesion: 0.10
Nodes (3): PetLink, Attention, VillagerPets

### Community 85 - "CHANGELOG.md"
Cohesion: 0.10
Nodes (19): 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0, 2.6.0, Male asset registry — Phase 2 (+11 more)

### Community 88 - "Block"
Cohesion: 0.04
Nodes (41): Block, BREAKFAST, DEFEND, EVENING, HOBBY, LESSONS, LUNCH, LUNCH_HOME (+33 more)

### Community 89 - "net.minecraft.world.item.Item"
Cohesion: 0.11
Nodes (10): Phase 1 Foundation Gameplay Verification, Bread, Stew and Coffee Consumables, 17 New Foundation Blocks, 24 New Items and 41 Recipes, Registration Order (blocks, items, block entities, professions), Codex Phase 1: Registry & Item Foundation, Wearable Uniforms and Rain Gear, VillageFoundation (+2 more)

### Community 90 - "Calendar"
Cohesion: 0.21
Nodes (3): Village Friends 2.20.0 — Birthdays and notice boards, Calendar, BirthdayTest

### Community 91 - "net.minecraft.world.level.block.state.BlockState"
Cohesion: 0.09
Nodes (4): NoticeBoardBlock, NoticeBoardBlockEntity, VillageLedgerItem, WorkstationBlock

### Community 92 - "kit_m01.py"
Cohesion: 0.07
Nodes (14): gathers(), hanging_basket(), leg_tube(), mud(), outer(), patch(), piebald(), rod() (+6 more)

### Community 94 - "Chemistry"
Cohesion: 0.17
Nodes (8): Chemistry, Conversation window, Friendship levels, Speech bubbles, The model, Village Ledger, Village life: families, love, friendship levels, speech bubbles and the Village Ledger, Where things live

### Community 97 - "furniture.py"
Cohesion: 0.06
Nodes (28): bar_stool(), blockstate(), boxes(), check(), cloth(), cloth_tacks(), corners(), cushion() (+20 more)

### Community 98 - "Wardrobe Python Module Pipeline (tools/wardrobe)"
Cohesion: 0.11
Nodes (12): Supreme Casual Line (t101-t120, b101-b120), Wardrobe Python Module Pipeline (tools/wardrobe), back_fan(), bangs(), cel_box(), cel_face(), lock(), clump() (+4 more)

### Community 99 - "kit_f04.py"
Cohesion: 0.07
Nodes (9): back_prop(), front_prop(), lamellae(), lames(), mud(), quilt_rows(), Rod, shaft() (+1 more)

### Community 100 - "SocietyTest"
Cohesion: 0.23
Nodes (5): Village Friends 2.13.0 — Village life and new faces, FriendshipLevelsTest, SocietyTest, Village life verification (2.13.0), Verification

### Community 101 - "WolfPoseMixin.java"
Cohesion: 0.24
Nodes (4): Files, WolfHeadAccessor, WolfPoseMixin, PetCarryLayer

### Community 102 - "Deed"
Cohesion: 0.10
Nodes (6): Deed, Know, Reactions, Circles, Rumors, RumorTest

### Community 103 - ".runTest"
Cohesion: 0.12
Nodes (3): CelebrationsGameTest, Birthdays, Gift

### Community 105 - "wardrobe/kit.py"
Cohesion: 0.08
Nodes (11): arm_bone(), arm_x(), belt(), flaps(), footwear(), leg_bone(), leg_ring(), legs() (+3 more)

### Community 106 - "Emote"
Cohesion: 0.11
Nodes (16): Bubble, EmoteBubbles, Pending, Emote, ANGER, BLUSH, DOTS, EXCLAIM (+8 more)

### Community 107 - ".perform"
Cohesion: 0.31
Nodes (3): Song, Songbook, Note

### Community 111 - "net.minecraft.world.item.ItemStack"
Cohesion: 0.14
Nodes (4): WorkstationBlockEntity, Combo, Daily, Workstations

### Community 112 - "kit_m03.py"
Cohesion: 0.09
Nodes (10): coil(), drips(), gloss(), knit_stockings(), leg_piece(), low_shoes(), rope(), rope_box() (+2 more)

### Community 114 - "kit_f07.py"
Cohesion: 0.09
Nodes (10): dust(), front_hung(), legs_both(), patch(), prop(), rope(), rope_box(), strap() (+2 more)

### Community 115 - "ResidentRoutines"
Cohesion: 0.12
Nodes (5): GuardPatrols, Squad, ResidentRoutines, Spot, Weather

### Community 116 - ".onInitializeClient"
Cohesion: 0.08
Nodes (5): Village Friends 2.18.0 — Names that fit, and arriving in a village, ArrivalBanner, ArrivalGameTest, Line, VillageArrival

### Community 117 - "taiga/civic.py"
Cohesion: 0.07
Nodes (23): apothecary(), chapel(), garrison(), library(), _lodge_bar(), _lodge_common_room(), _lodge_deck(), _lodge_facade() (+15 more)

### Community 118 - "Station"
Cohesion: 0.09
Nodes (14): Canvas, Lit, Station, ALCHEMICAL_PRESS, ARCHERY_TARGET, ARCHIVES, DRINKS_BARREL, EASEL_CANVAS (+6 more)

### Community 119 - "Dialogue"
Cohesion: 0.24
Nodes (3): Conversation Window (Talk/Story/Journal/Time/Travel tabs), Wordless Human-like Hum Voices, Dialogue

### Community 120 - "org.spongepowered.asm.mixin.injection.Inject"
Cohesion: 0.10
Nodes (10): Guard Equipment Exchange (Equip held item), Adventure Companions (Follow/Wait/Return home), CompanionPortalMixin, InjuredBodyMixin, ResidentPetMixin, SleepInBedRoutineMixin, VillagerCompanionMixin, VillagerFamilyMixin (+2 more)

### Community 122 - "HouseSurvey"
Cohesion: 0.08
Nodes (19): Houses, Names, Flood, FloodFill, Grid, Result, Status, NO_ROOM (+11 more)

### Community 123 - "kit_m05.py"
Cohesion: 0.09
Nodes (9): cord_end(), dust(), grime(), hose(), knee_patch(), leg_prop(), over_panels(), soft_shoes() (+1 more)

### Community 124 - "tavern_preview.py"
Cohesion: 0.19
Nodes (11): bar_patron(), check(), holds_dish(), load(), main(), probe(), Scene, seated() (+3 more)

### Community 132 - "kit_f03.py"
Cohesion: 0.11
Nodes (10): basket(), cord(), front_prop(), net(), net_box(), rope(), rope_box(), wet_hem() (+2 more)

### Community 133 - "net.minecraft.world.entity.npc.villager.Villager"
Cohesion: 0.08
Nodes (5): Where things live, CompanionController, Outing, Knockouts, VillageFriends

### Community 134 - "kit_f02.py"
Cohesion: 0.11
Nodes (9): back_prop(), cord(), hung(), lace(), prop(), ring(), sheen(), specks() (+1 more)

### Community 135 - "Weather"
Cohesion: 0.18
Nodes (6): Weather, CLEAR, CLEARING, RAIN, SNOW, THUNDER

### Community 136 - "re"
Cohesion: 0.24
Nodes (14): boxes(), check_text(), compile_all(), count(), fail(), main(), parse_answer(), read_lines() (+6 more)

### Community 137 - "rot_matrix"
Cohesion: 0.13
Nodes (9): axis(), braid(), finish(), link(), local(), plait_path(), _step(), chain() (+1 more)

### Community 139 - "shade"
Cohesion: 0.17
Nodes (7): checks(), lacing(), motif(), scatter(), patch(), darken_rows(), shade()

### Community 140 - "kit_m06.py"
Cohesion: 0.11
Nodes (8): brocade(), chain_links(), fleece(), fur_patch(), hose(), lower_legs(), robe_skirts(), blk()

### Community 141 - "HouseCatalog"
Cohesion: 0.12
Nodes (10): Use, BARRACKS, HOME, INN, QUARTERS, Anchor, HouseCatalog, RoomSpec (+2 more)

### Community 142 - "json"
Cohesion: 0.09
Nodes (21): Foundation Asset Generation Pipeline, icon(), merge(), recipe(), save(), tag(), save(), item_sprite() (+13 more)

### Community 143 - "kit_m10.py"
Cohesion: 0.11
Nodes (7): arm_ring(), cable(), channels(), leg_ring(), outer(), patch(), tie()

### Community 145 - "kit_m08.py"
Cohesion: 0.11
Nodes (8): brocade(), coat_skirt(), crossed_collar(), fringe(), hanging_tail(), pleats(), roundel(), tassel()

### Community 146 - "argparse"
Cohesion: 0.11
Nodes (16): build(), load(), main(), validate(), frame(), gait(), main(), walking() (+8 more)

### Community 148 - "kit_f01.py"
Cohesion: 0.13
Nodes (7): bundle(), cut_ends(), handle(), produce(), stalks(), twist(), wicker()

### Community 149 - "kit_f06.py"
Cohesion: 0.12
Nodes (7): bow(), charm(), cut_velvet(), prop(), tablet_band(), tablet_column(), train()

### Community 150 - "HousePlaqueBlock.java"
Cohesion: 0.12
Nodes (5): FoundationBlock, HousePlaqueBlock, Mount, STANDING, WALL

### Community 151 - "Treatment"
Cohesion: 0.16
Nodes (8): Future Real-Time Knockout Controller, Medical Treatment Contract, Downed Companion Rescue, MedicalSupplyItem, Treatment, BANDAGE_WRAP, REVIVAL_TONIC, SMELLING_SALTS

### Community 152 - "kit_m02.py"
Cohesion: 0.14
Nodes (5): apron_panel(), bar(), bib(), dashes(), hoop()

### Community 153 - ".book"
Cohesion: 0.08
Nodes (9): Random-Spread Structure Placement, Hometown Names and Settlements, Village Marker, VillageBook, VillageLedger, VillageNames, VillageRecord, Arrival (+1 more)

### Community 156 - "kit_f05.py"
Cohesion: 0.15
Nodes (5): beads(), dangle(), fixed(), glass(), lap_panel()

### Community 157 - ".living"
Cohesion: 0.17
Nodes (8): Birthdays, Birthdays and notice boards, Changing things, Notice boards, The calendar, Verification, Where things live, Guests

### Community 163 - "PetKeeping"
Cohesion: 0.14
Nodes (4): Longing, Nature, PetKeeping, ResidentPetsTest

### Community 172 - "kit_f10.py"
Cohesion: 0.12
Nodes (8): cord(), frills(), lambswool(), panel_prop(), arm_rings(), bells(), cuffs(), puffs()

### Community 177 - "How a batch is built"
Cohesion: 0.13
Nodes (15): How a batch is built, Outfit templates, Read first, in this order, Rules for shared files, Save progress as you go, Seeds, Style rules (non-negotiable), The META block (+7 more)

### Community 189 - "textures"
Cohesion: 0.15
Nodes (24): brass(), burlap(), cloth(), copper(), dummy_chest(), dummy_face(), herbs(), iron() (+16 more)

### Community 192 - "Games"
Cohesion: 0.13
Nodes (5): File format, How it works, PlaytimeClient, Since, Games

### Community 193 - "create_village_structures.py"
Cohesion: 0.12
Nodes (16): check_lot(), location(), main(), payload(), pool(), remove_stale(), string(), tag_type() (+8 more)

### Community 195 - "DeedKind"
Cohesion: 0.07
Nodes (23): DeedKind, BANDAGED, BIRTHDAY_GIFT, BROKE_HOME, HIT_GOLEM, HIT_RESIDENT, HURT_PET, KILLED_GOLEM (+15 more)

### Community 196 - "Playground"
Cohesion: 0.15
Nodes (4): Curious, Kid, Playground, Session

### Community 197 - "net.minecraft.world.entity.schedule.Activity"
Cohesion: 0.14
Nodes (4): Initial Guard Equipment (UUID-selected iron/chainmail), BrainRoutineMixin, GuardArmorMixin, RoutineBrain

### Community 199 - "notice_board.py"
Cohesion: 0.10
Nodes (20): blockstate(), check(), cork(), designs(), encode(), inkwell(), layer(), Model (+12 more)

### Community 200 - "PetTrick"
Cohesion: 0.13
Nodes (5): PetRenderStateMixin, PetPoser, State, PetTricks, PetTrick

### Community 205 - "org.spongepowered.asm.mixin.Mixin"
Cohesion: 0.15
Nodes (6): VillagerEventMixin, ContainerCloseMixin, GuardArrowMixin, GuardTradeDisplayMixin, HousingBlockChangeMixin, WorkAtPoiMixin

### Community 206 - "Move"
Cohesion: 0.14
Nodes (15): Move, APPROACH, CHASE, CIRCLE, COAX, FETCH, FLEE, FRONT (+7 more)

### Community 217 - "VillageStructure"
Cohesion: 0.16
Nodes (3): Prune, Terrain, VillageStructure

### Community 218 - "FoundationEntityBlock"
Cohesion: 0.33
Nodes (6): FoundationEntityBlock, Kind, APOTHECARY_COT, COMMAND_DESK, HOUSE_PLAQUE, NOTICE_BOARD

### Community 298 - "VillageVegetationMixin.java"
Cohesion: 0.17
Nodes (3): ChunkGeneratorDecorationMixin, VillageVegetationMixin, VillageGrounds

### Community 299 - ".fromPlaque"
Cohesion: 0.16
Nodes (8): Cell, DOOR, OPEN, SKY, SOLID, UNLOADED, FloodFillTest, World

### Community 300 - ".start"
Cohesion: 0.09
Nodes (12): Catch, Phase, CHEER, COUNT, FALL, FUMBLE, GATHER, HOLD (+4 more)

### Community 303 - "pets/preview.py"
Cohesion: 0.14
Nodes (8): apply(), draw(), transform(), main(), rot(), texture(), Track, vanilla_pose()

### Community 305 - ".mention"
Cohesion: 0.24
Nodes (3): Gossip, GossipTest, Dialogue

### Community 306 - "HousePlaqueBlockEntity"
Cohesion: 0.12
Nodes (6): Patrols, Command Desk Controls and Shields (future), Empty Block Entity Integration Hooks, ApothecaryCotBlockEntity, CommandDeskBlockEntity, HousePlaqueBlockEntity, VillageBlockEntities

### Community 310 - "PlayTest"
Cohesion: 0.15
Nodes (10): Village Friends 2.22.0 — Children at play, Animations, Children at play, Following a player, The games, The leather ball, Verification, When children get bored (+2 more)

### Community 316 - "Trick"
Cohesion: 0.18
Nodes (3): channels(), Trick, wave()

### Community 317 - "Move"
Cohesion: 0.17
Nodes (8): Move, FLAP, HOP, SALUTE, SPIN, STAR, STOMP, FollowTheLeader

### Community 319 - "Bone"
Cohesion: 0.18
Nodes (11): Bone, BODY, HEAD, LEFT_FRONT_LEG, LEFT_HIND_LEG, RIGHT_FRONT_LEG, RIGHT_HIND_LEG, ROOT (+3 more)

### Community 321 - "Residents' pets"
Cohesion: 0.20
Nodes (9): Befriending a stray, Following and resting, Pet tricks, Playing together, Residents' pets, The pet card, When a resident or pet is gone, Who keeps a pet (+1 more)

### Community 322 - "Game"
Cohesion: 0.22
Nodes (6): Game, CATCH, FOLLOW_THE_LEADER, HIDE_AND_SEEK, RING, TAG

### Community 323 - "Concepts"
Cohesion: 0.20
Nodes (9): Concepts, f02: Women, crafts and trades (tf/bf 086–110). Seeds 52000–52999. Outfit file female_f02.json, f06: Women, noble court and town (tf/bf 186–210). Seeds 56000–56999. Outfit file female_f06.json, f08: Women, the wider medieval world (tf/bf 236–260). Seeds 58000–58999. Outfit file female_f08.json, f09: Women, festivals, ceremony and seasons (tf/bf 261–285). Seeds 59000–59999. Outfit file female_f09.json, m02: Men, craft guilds and workshops (t/b 146–170). Seeds 32000–32999. Outfit file male_m02.json, m06: Men, nobles, court and town officials (t/b 246–270). Seeds 36000–36999. Outfit file male_m06.json, m09: Men, festivals, seasons and ceremony (t/b 321–345). Seeds 39000–39999. Outfit file male_m09.json (+1 more)

### Community 324 - "How the director chooses"
Cohesion: 0.25
Nodes (6): Authoring Village Life, How the director chooses, Resident animation packs, Village Life (pack 1), Village Friends 2.21.0 — Residents' pets, pet()

### Community 326 - "point"
Cohesion: 0.25
Nodes (4): point(), pointed(), points(), world()

### Community 331 - "staves"
Cohesion: 0.33
Nodes (4): shade(), staves(), stove_bricks(), vat_side()

### Community 333 - "Fit"
Cohesion: 0.40
Nodes (4): Fit, FEMALE, MALE, UNISEX

### Community 334 - "Motion"
Cohesion: 0.40
Nodes (5): Motion, FLAP_BACK, FLAP_FRONT, NONE, SWAY

### Community 335 - "flower"
Cohesion: 0.40
Nodes (3): bow(), flower(), tie()

### Community 336 - "render"
Cohesion: 0.50
Nodes (4): render(), at(), project(), rotate()

## Ambiguous Edges - Review These
- `FriendshipGameTest` → `Focused Client GameTest Flags`  [AMBIGUOUS]
  DEVELOPMENT.md · relation: references
- `GuardArmorMixin` → `Initial Guard Equipment (UUID-selected iron/chainmail)`  [AMBIGUOUS]
  GUARDS.md · relation: references

## Knowledge Gaps
- **332 isolated node(s):** `Loaded`, `FRONT`, `BACK`, `HEAD`, `HEAD_BACK` (+327 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2148 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **244 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `FriendshipGameTest` and `Focused Client GameTest Flags`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Wardrobe Python Module Pipeline (tools/wardrobe)` connect `Wardrobe Python Module Pipeline (tools/wardrobe)` to `kit_casual.py`, `anime_female.py`, `anime_male.py`, `kit_male.py`, `wardrobe/kit.py`, `wardrobe.py`, `.assembleOutfit`, `design_village.py`, `.runTest`, `Village Friends README`, `kit_female.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **What connects `Loaded`, `FRONT`, `BACK` to the rest of the system?**
  _332 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Face` be split into smaller, more focused modules?**
  _Cohesion score 0.08045977011494253 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `GuardArmorMixin` and `Initial Guard Equipment (UUID-selected iron/chainmail)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Society` connect `Society` to `list`, `HomesGameTest.java`, `Notice`, `.book`, `Taverns.java`, `util`, `.living`, `.mention`, `.runTest`, `net.minecraft.server.level.ServerLevel`, `Deeds`, `Townsfolk`, `VillageSocieties`, `Calendar`, `Chemistry`, `SocietyTest`, `Deed`, `.affinity`, `Board`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `kit_casual.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06116642958748222 - nodes in this community are weakly interconnected._