# Homes and beds

Version 2.24 gives every resident a home. Each village knows its houses, their rooms, beds, doors and workstations; every resident owns one bed, so neighbors stop fighting over beds; partners sleep side by side, children live with their parents, and a baby gets a bed in the family's house. Residents go home to their own house for meals and the evening, and sleep in their own bed. House Plaques read a house out, name it, and turn a house a player built into a home that residents in need move into.

Before 2.24 the House Plaque's `scanForBeds()` and `scanForWorkstations()` were empty hooks, and residents took whichever bed vanilla's AI found free that night.

## Where things live

| Piece | Code |
|---|---|
| Data (records with Codecs, saved as the level attachment `villagefriends:housing`) | `home/HousingBook` (format 1) → `home/HousingIndex` per village → `home/House` (rooms, beds, doors, workstations, plaque, name, private) |
| The structure catalog at runtime | `home/HouseCatalog` reads `data/villagefriends/villagefriends/structure-catalog.json`, written by `tools/create_village_structures.py` |
| Who sleeps where (pure, unit-tested) | `home/Assignments` |
| Player-built houses (pure, unit-tested) | `home/FloodFill` |
| House names (pure) | `home/HouseNames` |
| Reading houses from the world | `home/HouseSurvey` |
| Upkeep, plaques, vanilla integration, Ledger/Journal/notice helpers | `home/Homes` (one `Homes.register()` call from `VillageFriends`; installs `home/HouseBounds`) |
| The plaque | `home/HousePlaqueBlock` (wall or standing mount), `HousePlaqueBlockEntity` (house id and anvil name); models from `tools/create_foundation_assets.py` |
| Block changes | `mixin/HousingBlockChangeMixin` on `ServerLevel.updatePOIOnBlockStateChange` |
| Hooks elsewhere | `ResidentRoutines.update` (`Homes.keep`) and `steer` (`Homes.homeward`); `VillagerPets.rest` (`Homes.bedside`); `Knockouts.tend` (`helpHome`), `lieDown`, `drive`, `revive`, `KnockoutState.bed`; `VillageLedger`; `NarrativeEngine.about`; `quest/Notice.HOUSE`, `quest/Postings.refresh(..., needs)`, `VillageQuests.board/ready/gather`; `talk/Talk.pools` and one line in `TalkWorld.context` (`Homes.talk`); `client/ResidentRenderer` (a patient in bed renders as a sleeper) |
| Dialogue | `home.mine`, `home.shared`, `home.homeless`, `home.crowded`, `home.new`, `home.newborn_bed`, `home.partner_moved`, `home.vacant`, `notice.house`, `notice.thanks.house`, `baby.notice.house` in `tools/dialogue/lines/homes.txt`. Every key is optional: a missing pool is skipped and notices fall back to built-in text. |

## Houses

**Village houses come from the village structure, not from the blocks.** The first time a resident of a village is loaded, `Homes` asks `StructureManager.getStructureWithPieceAt(pos, #minecraft:village)` for the village structure (the way `TavernSurvey` finds the tavern) and turns every jigsaw piece whose template has beds into a `House`, with the catalog's rooms, beds (foot, facing, room), doors, workstation anchors and plaque anchor turned and moved the way the piece was placed (`HouseCatalog.place`, which is vanilla's `StructureTemplate.transform`). This reads no blocks. All five village types work: the catalog has room data for every template with beds.

Each house is then checked once its chunks are loaded (`HouseSurvey.verify`): one block read per catalog bed (a broken bed is marked `present=false` and nobody is given it), plus vanilla's points of interest for beds and job sites inside the house's box (beds and workstations a player added count). Only checked houses are given out.

The compiler gives each template with beds (`Template.save` in `tools/create_village_structures.py`):

| Field | Meaning |
|---|---|
| `use` | `home` (lots), `inn` (`*/buildings/tavern`), `barracks` (`*/buildings/garrison`), `quarters` (other civic buildings: apothecary, library, workshop) |
| `bed_facing` | each bed's facing, read from its foot block |
| `bed_room` | the room each bed's flood belongs to |
| `exterior_doors` | doors whose far side floods out of the template |

Every `home` template has a `villagefriends:house_plaque` anchor; the eight taiga homes got theirs in their designs (`tools/village_design/buildings/taiga/homes.py`). `HouseCatalogTest` fails if a home loses its plaque.

**Villages with no structure** (placed with `/place`, or claimed with a Village Marker) find their houses around their beds: each loaded bed that no house covers is flooded from the room it stands in (`HouseSurvey.found`), or, in an open shelter, becomes a one-bed "Bed nook".

House ids are stable: `g:<template>@<piece corner>`, `p:<plaque position>`, `f:<first bed head>`. Bed order is by head position.

### Names

The plaque's anvil name wins; then "The <Surname> House" after the grown-up who has lived there longest; then what the building is for ("The Garrison", "Guest rooms at the tavern", "The Apothecary's Rooms", "The Library Rooms", "The Workshop Loft"); then what it looks like ("Oak Cottage", "Tall Brick House", "A-Frame"); a player's empty house is "A house you built".

## Who sleeps where

`Assignments.assign` is pure and deterministic (same input, same beds, whatever the order), and keeps beds people already have while they still make sense.

1. **Households.** Partners; their minor children; minors who share a household key. Largest households first, then the longest-settled.
2. **Leaving.** A resident who passed away or is no longer in the village frees their bed, recorded as a `Vacancy(resident, name, house, bed, day, why)` (`passed`, `moved`, `cursed`; the last 32 are kept for a later memorial or mourning feature). A resident turned into a zombie villager keeps their bed for 7 days.
3. **Keeping.** Each household keeps the beds it has in the house that holds most of it.
4. **Moving in together.** A household not yet settled (someone without a bed, split between houses, or lodging in guest rooms or barracks that aren't theirs) moves as a whole into the first house with room for all of them: the house they already live in; the house of the bed vanilla had given them; their parents' house (a grown child living alone); their own quarters for someone on their own (apothecary over the shop, knights and archers in the barracks, the tavern keeper and cook at the inn); then the smallest family home with room.
5. **Player houses.** Households that fit nowhere move into a house a player built, unless it is Private; households with an open "bigger house" notice go first.
6. **Overflow.** Whoever is still without a bed keeps the bed they had if it's free, or takes any free bed: their family's house, the inn, the barracks, then anyone's spare bed. A baby only takes a bed in the family's house.
7. **Beds within a house.** Partners take the two closest beds in one room (side by side when there are); children take a bed in another room when there is one.

The household is recorded as a **need** when it is short of room: `homeless` (no beds at all), `crowded` (split, someone without a bed, or lodging at the inn or barracks) or `newborn` (only the baby is waiting for a bed).

Assignment runs when the houses change (a house checked, a bed broken, a plaque put up) or the village's families change (a society fingerprint compared every 5 seconds: births, deaths, new partners, curses, newcomers, and the day), at most once every 5 seconds per village.

## Vanilla stays in charge of sleeping

`Homes.keep(v)` runs once a second for every resident (from `ResidentRoutines.update`) and when they load:

- With a bed of their own, their `MemoryModuleType.HOME` is set to its head, the bed's point-of-interest ticket is taken, and their old home's ticket given back. Vanilla's `AcquirePoi`, `ValidateNearbyPoi`, `SleepInBed` and the rest package do the rest, unchanged.
- Without one, vanilla behaves as before, except that a bed assigned to someone else is taken back (memory erased, ticket released).
- When beds are handed out, newly assigned beds take their ticket and freed ones give it back (loaded chunks only; `keep` mends the rest, and re-takes a lost ticket every 30 seconds).

With `HOME` on their own bed, the rest package already walks residents home for bed, breakfast, supper, the evening and shelter. On top of that, a resident more than 24 blocks from their house at breakfast, supper or in the evening walks back to an open floor cell in its first room (`Homes.homeward`).

## Upkeep and performance

- **Nothing is rescanned on a timer, and nothing loads a chunk** (the one exception is the structure lookup itself, which, like the tavern's, reads the village start's chunk to `STRUCTURE_STARTS`).
- `HousingBlockChangeMixin` sees every block change, returns at once off the main thread (world generation) or when neither state is a bed, door, trapdoor, fence gate, plaque or point of interest, and otherwise turns the change into a queued look at the house around it (a chunk-to-house map, rebuilt when the index changes). A new bed outside any house in a village with no structure queues a new found house.
- `Homes.tick` runs at most one survey, flood or found house per tick, and verifications within 4,096 block reads per tick.
- Walls and roofs aren't watched block by block: after changing a house you built, use its plaque and it is flooded again.
- The per-resident cost each second is one memory comparison when nothing changed.

## House Plaques

- **Put up on the side of a block** it hangs on the wall (`mount=wall`, the default, which every plaque in a village template has); **on top of a block** it stands on a post (`mount=standing`).
- **Use** reads the house out (chat, with the name on the action bar):
  `✦ The Ashford House` / `Lives here: Mira Ashford (Farmer), Tobin Ashford (Fisherman), Pip Ashford (child)` / `Beds: 3 of 4 used · Workstation: Composter (Mira)` / `Needs: a bed for the new baby`.
- **Sneak and use** makes a house you built (or an empty village house) Private: its residents move out and nobody moves in. Again, and it's open. A family's village home can't be made private.
- **In a house a player built** the plaque floods the air around it (`FloodFill`): the cell in front of it (or, for a plaque hung on an outside wall, the first open cell behind the wall). Doors, fence gates and trapdoors are always room edges; each door's far side is flooded too, becoming another room unless it leaks outdoors (then it's an outside door). Limits: 6,000 open cells, a box of 32×24×32, 12 rooms. Beds belong to the room above their head or foot. Messages:
  - "★ The Reed House: 2 rooms, 3 beds, 1 workstation." (or "...no beds yet; residents can move in once it has one.")
  - "This house is open to the sky above X Y Z." (happy-villager particles mark the spot)
  - "This house is too big or not closed in (over 6000 blocks of room). Put the plaque in a smaller, closed house."
  - "Part of this house isn't loaded yet. Try again up close."
  - "The plaque needs to be on a wall of a closed room."
  - "This house is outside any village. The plaque still names it, but nobody will move in."
- **In a village house** the plaque simply names that house.
- Rename the plaque on an anvil to name the house.

## Around the village

- **Ledger:** each resident's page says "Home: The Ashford House (with Tobin, Pip)", "No bed of their own yet", "Sleeping at the garrison" or "Lodging in the tavern's guest rooms"; the list says "Looking for a home"; the news starts with households short of room ("The Reed family needs a bigger house (4 people, 2 beds).").
- **Journal:** the About page has "Home: <house>".
- **Conversation:** greetings and chat draw on `home.*` pools by situation: just moved in (`new`), a partner just moved in (`partner_moved`), a new baby's bed (`newborn_bed`), a neighbor's bed empty after a death (`vacant`), too little room (`crowded`), no home (`homeless`), otherwise `mine` or `shared`. `{house}` is the house's name. Children of a crowded household use `baby.notice.house`.
- **Notice board:** a household short of room posts at most one "We need a bigger house" notice (`Notice.HOUSE`, up 7 days; text from `notice.house` with `{name}`, `{job}`, `{count}` beds, `{people}`). It is ready to turn in, at the board or to the poster, once their household lives in a house a player built; the reward is emeralds and a carpenter's gift. A notice nobody took comes down when the household finds room.
- **Pets:** while their resident sleeps, a cat or dog lies on the floor beside the foot of their bed (`Homes.bedside`), slipping past a closed door if it must.
- **Knockouts:** once the apothecary has dressed a patient's wounds, they are helped to their own bed if it is within 48 blocks, loaded and free, otherwise onto the nearest free apothecary cot near the apothecary's workstation, otherwise they stay where they fell. `KnockoutState.bed` keeps them there across reloads; reviving them gets them out of bed.
- **Deaths:** the bed is freed and a `Vacancy` recorded (see above).

## Extension points

These exist and are documented for later features; nothing calls them yet.

| For | API |
|---|---|
| Inviting the player to dinner at home | `Homes.houseOf(origin, village, resident)`, `Homes.hearth(level, house)`, `Homes.name(...)` |
| A resident moving to another village | `Homes.vacate(origin, village, resident, name, "moved")`, `Homes.claim(fromLevel, fromVillage, toLevel, toVillage, resident, name)` |
| Mourning or a memorial | `HousingIndex.vacated()` |
| Deeds (theft, breaking someone's bed, door or workstation) | `HouseBounds.current().houseAt(level, pos)` and `owners(level, pos)` |

## Saves

`villagefriends:housing` (a `HousingBook` with `format` 1; a newer format is refused rather than misread) on the level that records the village, next to `villagefriends:societies`. An absent attachment is an empty book; a village builds its index the first time one of its residents loads. New optional fields: `KnockoutState.bed`, the plaque's `house` and `name` NBT, and the plaque's `mount` blockstate property (default `wall`). There is no migration code: the user starts a new world for 2.24.

## Verification

- `gradlew.bat test --tests dev.villagefriends.HousingAssignmentsTest` (households, partners, children, newborns, quarters/barracks/inn and overflow, player houses and Private, determinism under shuffling, stability, deaths and vacancies, the cursed week, broken beds, codec round-trip, empty book, format guard), `FloodFillTest`, `HouseCatalogTest` (every bed template has `use`, `bed_facing`, `bed_room`; every bed is inside its room; every home has a plaque; rotations against hand-computed points; names).
- `gradlew.bat runClientGameTest -Ptests=HomesGameTest -PtestHeap=2560m`: a plaqued player house and a homeless couple moving in, the readout, a hole in the roof and a too-big hall, a broken bed, a newborn's bed, a knocked-out resident helped into their bed with their cat at the bedside, a death's vacancy, a homeless newcomer's notice and the Ledger, save and reload, Private on and off, all five village types read from their structures and checked block by block, and bedtime in a natural seed-1 plains village (every sleeper in their own bed, partners in one room). Screenshots `homes-*` in `build/run/clientGameTest/screenshots`.
