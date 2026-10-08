# The tavern: lunch, supper and evenings at The Hearth

Version 2.19 makes the tavern a place residents actually use. Their day takes them there for lunch, for supper and for an evening out; they find a seat with the people they like, sit down, are served by the tavern keeper (and the cook, at mealtimes), eat and drink course by course, talk across the table, warm their hands at the fire, listen to the bard, and get up again when their hour is over. The plains tavern, The Hearth, was rebuilt for it.

Before 2.19, residents with a tavern part of their day walked to within five blocks of the keeper's barrel and stood there; nobody sat, ate or drank.

## Where things live

| Piece | Code |
|---|---|
| Who goes when (pure, unit-tested) | `routine/Routine.java`: `tavernLunch`, `tavernSupper`, `tavernNight`, `afternoonPint`, `sociable`, the `SUPPER_TAVERN` block, `atTavern` |
| Seat choice, the menu, meal timings (pure, unit-tested) | `tavern/Patronage.java` |
| Reading a tavern's building | `tavern/TavernSurvey.java` |
| Running the tavern: seats, orders, table service, leaving | `tavern/Taverns.java` (one `Taverns.register()` call from `VillageFriends`) |
| Sitting | `tavern/Seat.java` (entity `villagefriends:seat`) |
| Furniture and meals | `tavern/TavernBlocks.java`, `tavern/TavernItems.java`; models from `tools/tavern/furniture.py`, sprites from `tools/tavern/sprites.py` |
| Client: dishes on tables and in hands, animation tags | `client/TavernClient.java`, hooks in `ResidentRenderer`, `ResidentLife`, `ResidentAnimation`, `ResidentPoser` |
| Animations | `tools/animations/tavern/*.py` compiled to `resident_animations/tavern.json`; seated previews with `tools/animations/tavern_preview.py` |
| The building | `tavern()` in `tools/village_design/buildings/civic.py` |
| Supper dialogue | `tools/dialogue/lines/tavern.txt` |

`ResidentRoutines` calls `Taverns.update` once a second for every resident; while their part of the day is at the tavern it takes over from the old "walk to the barrel" steering, and when it isn't it stands them up and gives their seat back.

## The day

| Who | When |
|---|---|
| Lunch | A third of adults are tavern regulars who lunch there about 70% of days; the rest go about one day in eight. Sociable personalities go more often, reserved and meticulous ones less, and Market Day adds 15 points. Tavern lunches start at 11:15, a quarter of an hour early, to get a table. |
| Supper | **New part of the day, "Supper at the tavern"** (`SUPPER_TAVERN`, 17:15–18:30): about one evening in five, nearly half on Market Day. |
| Evenings | About one evening in three (two in three on Market Day; it used to be everyone, which no building could hold). Night owls stay latest. |
| Afternoons | Now and then a free afternoon becomes a drink at the tavern. |
| Rain | Lunch at the bell moves into the tavern, and the warmest-hearted neighbors wait out a wet afternoon there instead of at home. |
| Tavern keeper | Works 11:00–21:00 (was 19:45). |
| Cook | Comes back to the kitchen at 16:00 for the supper service and eats late at home. |
| Bard | Plays the tavern's stage 18:00–20:15, then stays for a drink. |

Children don't go to the tavern.

## A visit

1. **A seat.** On arrival a resident scores every free seat (`Patronage.score`). Partners, family and best friends at a table pull them in; rivals push them away; friendly residents like a busy table and reserved ones a quiet one; the hearth draws people on cold nights and in the evening; the terrace fills on fine lunch hours and is closed in rain and snow; diners would rather have a table than a bar stool, while a quiet drinker likes the bar. With every seat taken they stand at the bar, and in a packed house they find a bit of floor. Someone who can't find a way to their chair within fifteen seconds picks another.
2. **Sitting down.** At their chair they ride an invisible `Seat`, so vanilla gives them the sitting pose, keeps them from being pushed around and saves them with it. They perch a little forward, square to the table; their head is free to look around. A seat stands its resident up if they are hurt, frightened (panic, raids, hiding), knocked out, recruited as a companion, or their hour is over.
3. **Ordering.** A moment after sitting down they order (`Patronage.order`): at lunch the cook's dish of the day, then a drink; at supper the next dish in the rotation, a drink, and sometimes an apple tart; in the evening drinks, now and then with a tart. With nobody at the stove, lunch is a cold ploughman's.
4. **Service.** The tavern keeper goes to the bar (the drinks barrel for cider, the tap stand for coffee), serves anyone waiting at the counter straight away, then carries a tray of up to three orders out to tables close together, nearest first. While the stove is lit, the cook brings food out from the kitchen the same way. Drinks come out of the barrel's and tap stand's own stock, which players see go down; a keeper taps a fresh barrel when one runs dry. With no staff on duty, patrons help themselves after a few seconds; anyone kept waiting by a busy keeper (20 seconds at lunch, 30 at supper, 45 in the evening) fetches it themselves.
5. **Eating and drinking.** The dish sits on the table in front of them (whatever table it is: a Tavern Table, a fence with a pressure plate, a bar counter) and moves to their hand for each bite or sip. A meal takes 18–28 seconds, a mug 25–45; between courses they talk. You hear the odd bite and sip, and see crumbs.
6. **Afterwards.** An empty bowl or mug stays on the table until they order again or leave. When a table empties, the keeper comes over and wipes it down when nobody is waiting.

The bard performs from the stage (a note block or jukebox in the tavern; otherwise by the bar), one song after another; patrons nearby get the `music` tag and sway, clap and tap along.

What each patron is doing is shared with clients as the synced attachment `villagefriends:tavern` (`wait`, `eat:<item>`, `drink:<item>`, `done[:<leftover>]`, `carry:<item>` for staff, `wipe`). The conversation window's status line shows it ("Supper at the tavern · eating shepherds pie"). Everything else is kept in memory; a resident who was seated when the world was saved keeps their seat and simply orders again.

## Which buildings count

`TavernSurvey` reads the building around the keeper's station: the village structure piece it stands in (so taverns of every village type, including the desert, savanna, snowy and taiga taverns on the `village-biomes` branch, work without changes), or a box 14 blocks around the station for a tavern players built themselves. It is surveyed when first visited and again every minute.

- **Seats:** Tavern Chair, Bar Stool, Fireside Armchair, Village Bench, Campfire Bench, and any bottom straight stair with a table in front of it (the stair chairs every village building has). A seat needs open space above it.
- **Tables:** Tavern Tables and fences topped with a pressure plate or carpet; adjacent ones make one long table. A stool's table is the bar counter in front of it: anything solid to about waist height with nothing (or a slab) on top.
- **Hearth seats:** within four blocks of a lit campfire or fire. **Terrace seats:** under open sky.
- **Standing room:** free floor under a roof within seven blocks of a keeper's station, beside a counter, a little apart.
- **The stage:** the first note block or jukebox in the building.

Players can sit on every seat too: use one with an empty hand (sneak to get up). Ordinary staircases are left alone, since a stair only counts with a table in front of it.

## The Hearth, rebuilt

17 wide and 29 deep (was 21), facing the town square:

- **Beer garden** (front): a plank deck under a pergola with lanterns and azalea, two trestle tables with benches (8 seats).
- **Common room:** the fireplace on the west wall with two Fireside Armchairs and a settle (4 hearth seats), two long tables of three Tavern Tables with chairs down both sides (12), a square Tavern Table and an old fence table (8), the bar along the east side with five Bar Stools and room to stand between them, and the bard's dais by the door with its note block. Lanterns, a chandelier, rugs, banners, kegs and hanging herbs.
- **Behind the bar:** the keeper's well with the tap stand and drinks barrel, kegs, shelves and a serving hatch to the kitchen.
- **Kitchen wing:** the cook's stove, smoker, prep table, pantry and a back door to the yard.
- **Upstairs:** two guest rooms with two beds each.

37 seats in all, 10 of them by the fire. The village simulation over 300 seeds still never misses a required building.

## Furniture and food

| Block | |
|---|---|
| Tavern Table | Dark oak trestle table on a centre post; a row of them makes one long board. Dishes sit on its top (14/16). |
| Tavern Chair | Spruce, spindle-backed. |
| Bar Stool | Round seat on a post with an iron foot ring; turns to the counter beside it. |
| Fireside Armchair | Deep red, buttoned and brass-tacked, for the hearth. |

`facing` is the way the sitter faces, like the Village Bench. Recipes: tables (slabs, fence, planks; makes 2), chairs (planks and sticks; makes 2), stools (a slab and sticks), armchairs (wool, red dye or red wool, planks).

| Meal | |
|---|---|
| Ploughman's Lunch | Bread, cheese, an apple and a pickle on a board (7 hunger). Bread, an apple and a beetroot. |
| Shepherd's Pie | Lamb and mash in a terracotta dish (9). Cooked mutton, a baked potato and a carrot. |
| Apple Tart | A lattice-top tart (5). An apple, sugar, wheat and an egg. |

The cook's dish of the day at the kitchen stove now rotates through hearty stew, shepherd's pie, fresh bread and a ploughman's lunch, the same dish the tavern serves for lunch that day.

## Animations: the Tavern pack

A second bundled pack, 67 clips, authored in `tools/animations/tavern/` (`seated.py`, `dining.py`, `chat.py`, `bar.py`) and compiled by `python tools/animations/animations.py` beside Village Life.

| Group | Clips |
|---|---|
| Seated idles | settles into the seat, looks around the room, admires the beams, leans back and stretches, hands behind the head, chin in hand, drums fingers on the table, arms folded, yawns, dozes off, warms hands at the fire |
| Waiting | rubs hands hungrily, cranes over the shoulder for the keeper, taps a spoon |
| Eating | spoons up stew and blows on it, tears and bites bread, a forkful of pie, picks at a ploughman's, nibbles a tart, a hearty mouthful, savors a bite with eyes closed, wipes the mouth |
| Drinking | sips, a big gulp, blows on hot coffee, raises a toast, clinks mugs with a tablemate, swirls and peers in |
| Afterwards | pats a full belly, peers into an empty mug, pushes the plate away |
| Seated chat | leans in to tell it, tells a story with both hands or waving the mug, points across the room, counts on fingers, whispers across the table; nods along, laughs and slaps the table, chin in hand, leans back skeptical, gasps, listens over the mug |
| Seated talk and reactions | explains, nods, shrugs, taps the table for emphasis; waves, nods hello, raises the mug to you; belly laughs, giggles, claps, bows with a hand on the heart |
| Music | sways, claps along, taps the table in rhythm (seated and at the bar) |
| At the bar | leans on the counter, waves for the keeper, sips, toasts |
| Staff | the keeper wipes down a table and rings last orders; the bard bows to the room |

New tags: `seated`, `tavern`, `dining:wait|eat|drink|done|carry|wipe`, `food:stew|pie|bread|platter|tart`, `drink:cider|coffee`, `music`, `hearth`; a drink in hand at the bar counts as `holding`.

How seated clips play:

- Sitting residents keep vanilla's riding pose for their legs; clips add to the arms, body, waist, head and eyes, and leg and root tracks are ignored.
- While `seated`, idles, chats and talk only use clips that require `seated`; reactions use a seated clip when one fits and otherwise play upper body only.
- Clips that require `dining:eat` or `dining:drink` take the dish into the hand (the left one for left-handed residents) and must use `items: override`.
- Seated neighbors talk to whoever sits beside them as well as across, and turn their heads to each other.
- Diners chat less while their food is in front of them.

## Verification

- `gradlew test`: `RoutineTest` (tavern lunches, suppers and evenings at sensible rates, sociable versus reserved, the keeper's, cook's and bard's hours, rain moving lunch indoors, no children), `PatronageTest` (seat choice, the menu course by course, leftovers and timings), `TavernPackTest` (seated filtering, no leg tracks, diners mostly eat) and `AnimationPackTest` (both bundled packs).
- `gradlew runClientGameTest -Ptests=TavernGameTest` places The Hearth on a flat world with a keeper, a cook and eighteen residents. On a Market Day evening they find seats and are served; the client draws them seated with their dish. A player sits on a chair and gets up. At bedtime every seat is given back; the next lunch is the dish of the day. Screenshots are named `tavern-*`.
- `gradlew runClientGameTest -Ptests=TavernVillageGameTest` generates a whole village and checks its residents fill the tavern on Market Day evening, inside a building found through its structure piece (`tavern-village-*`).
- `python tools/tavern/furniture.py --check`, `python tools/tavern/sprites.py --check`, `python tools/animations/animations.py --check`, `python tools/dialogue/dialogue.py --check`, `python tools/create_village_structures.py --check`.
