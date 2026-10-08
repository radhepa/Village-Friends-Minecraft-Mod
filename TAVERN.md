# The tavern: lunch, supper and evenings at The Hearth

Status: **plan** (2026-10-08). Branch `tavern`, worktree `.claude/worktrees/tavern`. This file becomes the feature's documentation once it ships, like VILLAGE_DAYS.md.

## Where we are today

Mapped with the knowledge graph (`graphify query "tavern inn meals"`, `graphify path "Routine" "ResidentRoutines"`) and by reading the code:

- `Routine` already has three tavern parts of the day: `LUNCH_TAVERN` (a third of adults, fixed per person), `TAVERN` evenings (a third of nights, everyone on Market Day) and the bard's `PERFORM`. The tavern keeper works 11:00–19:45 and is a night owl.
- `ResidentRoutines.steer` walks those residents to within five blocks of the nearest tavern keeper station (drinks barrel or tap stand) and then they **just stand there**. Nobody sits, eats, drinks or talks at a table. DEVELOPMENT.md lists seating as future work.
- The plains tavern ("The Hearth", `tavern()` in `buildings/civic.py`) is 17×21 with nine seats: stair chairs at fence-and-pressure-plate tables, two benches on the terrace, a bar at the back, a fireplace, the cook's kitchen wing and two guest rooms. A typical village has 28–54 residents (median 38), so it is far too small for a lunch crowd, let alone Market Day.
- The unmerged `village-biomes` worktrees have desert, savanna, snowy and taiga taverns built the same way (stair chairs, fence tables, a tap stand and drinks barrel).
- Food and drink already exist: Mug of Cider and Steaming Coffee Mug (poured at the barrel and tap stand, whose stock the keeper refills), Fresh Village Bread and Hearty Stew (the cook's dish of the day at the kitchen stove).
- Residents can't play animations while riding anything (`ResidentLife.canAct`, `ResidentAnimation.canAnimate`), and the routine stops for passengers.

## What residents will do

1. **Go at the right times.** Lunch at the tavern on some days (habit plus a daily roll), **supper at the tavern** (new), evenings for a drink, the odd afternoon pint on their hobby time, and most of the village on Market Day evening. Social personalities go more, reserved ones less. Rain drives the bell's lunch crowd into the tavern.
2. **Find a seat with their people.** Each arrival picks a seat by who is already sitting at each table: partners, family and best friends pull them in, rivals push them away, reserved residents like a quiet corner, the cold-blooded like the hearth, and fair weather fills the terrace. When every seat is taken they stand at the bar, and when that is full they mingle in the room.
3. **Sit down for real.** A resident at their seat sits on it (an invisible seat entity they ride, so vanilla handles the pose, pushing and saving), facing the table.
4. **Order and be served.** Diners wait (rubbing their hands, craning for the keeper). The tavern keeper picks the order up at the bar and carries it to the table, plate in hand. Lunch and supper are the cook's dish of the day when the cook is working (stew, bread, and the new **Ploughman's Lunch**, **Shepherd's Pie** and **Apple Tart**), drinks come from the barrel and tap stand **and use up their stock**, which the keeper refills. With no keeper on duty, patrons help themselves after a moment.
5. **Eat and drink.** The dish sits on the table in front of them (whatever table it is: stair-chair taverns too) and moves to their hand for each bite or sip. Spoonfuls of stew, tearing bread, a forkful of pie, blowing on hot coffee, a toast, clinking mugs, patting a full belly, peering into an empty mug.
6. **Talk to friends.** Tablemates take turns speaking and listening with seated gestures, turn their heads to each other, laugh and slap the table. Sharing a meal counts as extra time together in the village's relationship model, and the usual chat bubbles show how they feel about each other.
7. **Enjoy the place.** Warm their hands at the hearth, look up at the beams, lean back, doze off late in the evening, and when the bard performs on the tavern's little stage, sway, clap and tap along.
8. **Leave when the hour is up**, stand up and head back to work or home.

The tavern keeper works the bar, serves, and wipes the tables between customers; the cook gets an evening shift for supper. Players can sit on the new chairs, stools and benches too.

## How it fits into the code

New package `dev.villagefriends.tavern` keeps almost everything out of files the other sessions are editing.

| Piece | Kind | Job |
|---|---|---|
| `Patronage` | pure, unit-tested | Who goes to the tavern when (lunch, supper, evening, afternoon pint), seat scoring from relationships and personality, meal timings, the menu |
| `TavernSurvey` | world | Finds a tavern's building (its structure piece from `StructureManager.getStructureWithPieceAt`, so it works for every village type; a 10-block box around the keeper's station for player-built taverns) and lists its seats, tables, bar, hearth, stage and standing room. Cached per tavern, refreshed every minute |
| `Taverns` | world, server tick | Seat claims, the order queue, table service by the keeper, each patron's visit (arrive, sit, wait, eat, linger, leave), self-service when no keeper is on duty |
| `Seat` | entity `villagefriends:seat` | Invisible, saved with its rider, discarded when empty; ejects a rider who panics, is hurt, knocked out, recruited or trading |
| `TavernBlocks`, `TavernItems` | registry | Furniture and meals, registered from one `Taverns.register()` call |
| `TavernClient` (client) | renderer hooks | Seat renderer, the dish on the table or in hand, seated animation tags |

Attachments: `villagefriends:tavern` (synced string, e.g. `eat:villagefriends:hearty_stew`, `drink:villagefriends:mug_of_cider`, `wait`, `done:…`, `carry:…` for the keeper) drives animation tags and props. Whether someone is seated comes from their vehicle.

Hooks in shared files are one or two lines each: `Taverns.register()` in `VillageFriends`, `TavernClient.register()` in `VillageFriendsClient`, the tavern case of `ResidentRoutines.steer`, the passenger check in `ResidentRoutines.update`, the prop hook in `ResidentRenderer`, and seated support in `ResidentLife`, `ResidentAnimation` and `ResidentPoser`.

### The day (Routine)

| Who | Change |
|---|---|
| Adults | Lunch at the tavern by habit and a daily roll (tavern regulars about 70% of days, others about 15%), from 11:15 to grab a table. New block **`SUPPER_TAVERN`** "Supper at the tavern" (17:15–18:30) about one evening in five, more for warmhearted and playful residents, nearly half on Market Day. Evenings at the tavern stay about one in three. Market Day evening goes from everyone to about two in three (the rest stay home), because no building holds a whole village. |
| Rain | Lunch at the bell becomes lunch at the tavern. |
| Tavern keeper | Works 11:00–21:00 (was 19:45) for the evening crowd. |
| Cook | A supper shift 16:00–19:00 at the kitchen stove. |

### Seats and tables

Recognized seats: the new Tavern Chair, Bar Stool and Fireside Armchair, the existing Village Bench and Campfire Bench, and bottom straight stairs with a table in front of them (the way every existing tavern builds chairs). Tables: the new Tavern Table, any fence topped with a pressure plate or carpet, and the bar counter for stools. Seats next to a lit fire are hearth seats; seats under open sky are terrace seats (skipped in rain).

### Animations: a new "Tavern" pack

`tools/animations/tavern/*.py`, compiled by the same `animations.py` to `resident_animations/tavern.json` (separate from village_life.json, so the two packs never conflict). New tags: `seated`, `tavern`, `dining:wait|eat|drink|done|carry`, `food:stew|bread|pie|platter|tart`, `drink:cider|coffee`, `music` (a bard performing nearby), `hearth`. While seated only clips that require `seated` play for idles and chats; reactions use seated versions where they exist, and legs and root never move.

About fifty clips:

| Group | Clips |
|---|---|
| Seated idles | settle in, look around the room, admire the beams, lean back and stretch, hands behind the head, chin in hand, drum fingers on the table, arms folded, yawn, doze off (late), warm hands at the hearth |
| Waiting | rub hands, crane for the keeper, tap a spoon |
| Eating | spoon stew (and blow on it), tear and bite bread, fork of pie, ploughman's bites, nibble a tart, savor with eyes closed, wipe mouth, pat a full belly |
| Drinking | sip, big gulp, blow on coffee, raise a toast, clink mugs with a tablemate, swirl and peer in, peer into an empty mug |
| Seated chat | lean in to tell it, story with the mug, point across the room, count on fingers; nod, laugh and slap the table, chin in hand, lean back skeptical |
| Seated reactions | wave from the seat, raise the mug to you, belly laugh, clap |
| Music | sway, clap along, tap the table (seated and standing) |
| At the bar | lean on the counter, wave for the keeper, drink and toast standing |
| Staff | keeper wipes a table, rings last orders; bard bows to the room |

### Blocks and items

- **Tavern Table** (trestle style, joins up into long tables), **Tavern Chair** (spindle back), **Bar Stool**, **Fireside Armchair** (upholstered, by the hearth). Models from a design program `tools/tavern/furniture.py` built on the workstation `Model` kit, vanilla wood textures plus painted cloth; players can sit on every one of them.
- **Ploughman's Lunch**, **Shepherd's Pie**, **Apple Tart**: food items with authored 16px sprites (`tools/tavern/sprites.py` on `item_sprites.raster`). They join the cook's dish-of-the-day rotation at the stove.

### The Hearth, rebuilt

`tavern()` becomes 17×29: a pergola beer garden at the front (three tables), a common room with a big hearth and two armchairs, two long tables and two square tables, a bar with five stools along the east wall, a bard's stage corner, the kitchen wing behind with a serving hatch, guest rooms upstairs, and a yard. About 30 seats plus bar standing room. The lot contract (entrance at `[8,1,0]`, ≤ 8 either side) and the profession stations and residents stay. The biome taverns keep their designs and work through the survey.

### Dialogue

`tools/dialogue/lines/tavern.txt` (a new file): greetings for `supper_tavern`, lines about the food, the keeper's and cook's work at the tavern, and a tavern offer from the keeper ("This one's on the house").

## Verification

- `RoutineTest` (supper at the tavern, lunch rolls, the cook's and keeper's new hours, rain moving lunch indoors), `PatronageTest` (seat choice, attendance rates, menus).
- Client game test `TavernGameTest` (`-Ptests=TavernGameTest`): builds The Hearth on a superflat world with a keeper, cook and a dozen residents, runs lunch and an evening, checks that residents sit, are served and eat, that seats are released when they leave, and takes screenshots. Small test groups and `-PtestHeap=2560m`, since memory is tight.
- `-PvillageGallery -Pgallery=tavern` for the building, `python tools/village_design/simulate.py` to make sure the bigger lot never knocks a required building out.

## Order of work

1. Core: `Seat`, `TavernSurvey`, seating and leaving, Routine attendance. Residents sit down at the existing tavern.
2. Meals: the `tavern` attachment, menu, table service, drink stock, props on tables and in hands.
3. The Tavern animation pack and seated support in the director and poser.
4. Furniture, meal items and sprites, the rebuilt Hearth.
5. Dialogue, docs, tests, graph refresh.

## Not touched

- The quest and notice board (being built in another session).
- The biome villages' tavern designs (on the unmerged `village-biomes` branch).

## Merge notes

`birthdays-and-quests` also edits `Routine.java` (adds `PARTY` at the end of `Block`), `ResidentRoutines.java`, `VillageFriends.java`, `animations.py`, the dialogue compiler and the compiled `village_life.json` and `dialogue.json`. This branch adds `SUPPER_TAVERN` beside `SUPPER` rather than at the end, keeps its animations in a separate pack and its lines in a separate file, and recompiles the dialogue bank after merging.
