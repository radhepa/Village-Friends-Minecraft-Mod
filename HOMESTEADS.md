# Homesteads

Not everyone lives in a village. Out in the wild, well away from any town, you can come across five kinds of small homestead, each with its own people, its own look and its own way of talking:

| Homestead | Who lives there | Trade | Where it turns up |
|---|---|---|---|
| **The farmstead** (`homestead_farmstead`) | A husband and wife farming on their own: a fieldstone-and-plaster farmhouse with a porch, a field of wheat and carrots with a scarecrow, a hen run and coop, a kitchen garden, a well, a haystack and the farm cat | He farms (composter by the field gate); she keeps the house and the hens (kitchen stove) | Plains, sunflower plains, meadows, forests, birch and flower forests |
| **The pariah's house** (`homestead_pariah_house`) | Someone cast out of their village years ago, once a respected councillor. A fine stone-and-timber house gone to seed: holes in the slate, a broken window and a boarded one, a dry basin whose statue is gone, a dead tree, a fallen yard wall and a sign on the gate: *Turn back. No visitors. No pity.* Inside, one armchair by the fire and a long table with a single chair | None | Plains, meadows, forests, dark forests, birch forests, taiga |
| **The shepherd's fold** (`homestead_shepherd_fold`) | A hill shepherd and the flock: a dry-stone bothy with a hay ridge, a round sheepfold with six sheep, a water trough, a fleece line and a lookout rock | Shepherd (loom) | Meadows, plains, windswept hills, cherry groves, taiga, snowy plains |
| **The herbalist's cottage** (`homestead_herbalist_cottage`) | A hedge-herbalist the villages call a witch and visit after dark: a crooked mud-brick cottage under a steep, mossy roof, a cauldron over the fire, herbs and roots hanging from the rafters, a fenced herb garden, sweet berries, a beehive and a fairy ring of mushrooms | Apothecary (alchemical press) | Forests of every kind, taiga, swamps |
| **The old watchtower** (`homestead_watchtower`) | An old soldier keeping a watch nobody ordered: a three-storey stone tower with a crenellated deck, a brazier and a flag, stairs all the way up, the old curtain wall fallen around it, a target and butts in the yard | Archer (archery target) | Plains, meadows, savannas, windswept hills, taiga, snowy plains, forests |

Find one with `/locate structure #villagefriends:homesteads`, or a kind with `/locate structure villagefriends:homestead_watchtower`. They generate in newly generated chunks only.

## Their lives

- **They belong to no village.** Homestead folk never join a village's census, news, housing, notice board or birthdays, and their nameplate names their home instead: *Edwin Hale of Cloverbrook Farm*, *Ada Moss of Windy Fold*. The pariah belongs nowhere: *Corvin Vane, the Outcast*.
- **Who they are fits how they live.** The farmstead couple are always a man and his wife and share one family surname; the farmer is Steadfast and his wife Warmhearted, the pariah Reserved (and dislikes bells), the shepherd Curious (a stargazer), the herbalist Meticulous and the veteran Protective. They take their biome's villager type.
- **Their day has no tavern, bell or market in it.** Lunch and supper are at home and the evening is by their own fire; the hours a villager would spend with the neighbors or at the market go to the farm or the flock, or to their own pursuits. Their window says what they're doing in their own terms: *Mending the old house*, *Tending the flock*, *Brewing remedies*, *Keeping the watch in the storm*.
- **They stay near home.** Someone who wanders more than 26 blocks from the middle of their homestead turns back for their own bed.
- **The veteran keeps the watch.** Every night from half past eight until midnight, whatever the weather, they walk slowly from corner to corner round the tower, stopping at each to look out (with their bow, as an archer would). Some nights they keep the watch until dawn.

## What they say

Each role has its own dialogue, about 1,290 lines in all, and talks **only** from it, on every topic: greetings (for strangers and friends, by time of day and weather), "How's your day?" (with lines for newcomers, close friends, memories of the life before and late-night thoughts), work, adventures, jokes, news and "Anyone special?", plus reactions to you (hurt, hungry, soaked, out after dark) and to what you're holding.

- **The pariah** is mostly scornful: of the village that cast them out, of pity, of visitors (you included). They talk about the council seat they lost, the vote, and old friends who looked at their boots: Aldous, their oldest friend; Merrit, the rival who took the seat; Wenna, who kept their chair by the tavern hearth; Tobin, the clerk they trained, who cast the last vote. What they were accused of is never told. As you become friends they get more honest, never soft. They never ask you questions or offer you anything.
- **The farmstead couple** talk about the farm, the weather and the harvest, the village they left, the hens (Duchess, Pudding and Nettle), Barnaby the scarecrow, and each other, by name (`{partner}`) and as "my husband" or "my wife" (`{spouse}`). If one of them is gone, the other still has plenty to say.
- **The shepherd** names every sheep (Bramble, Old Hob, Thimble, Moss, Dulcie and Pickle), reads the clouds and the stars, and finds people at market too loud.
- **The herbalist** is wry and knowing: the villages call them a witch and come to the back door at night for remedies. They learned from old Sorrel, who lived in the cottage first.
- **The veteran** remembers the Lantern Company, Captain Varre, the siege of Harrowmere, the Greywater crossing and the friends they lost; they keep the brazier lit for stragglers.

Placeholders that only homestead lines use: `{place}` (their homestead's name) and `{spouse}`. `{village}` is the nearest village they could know of, or "the village". Homestead folk are never asked village questions ("Is {village} the first village you've visited?").

## How it works

- **Templates** are designed in `tools/village_design/buildings/homesteads/<name>.py` (shared helpers in `common.py`) and written to `tools/village_blueprints/homesteads/<name>.json` by `python tools/design_village.py homesteads/<name> --preview`. Each has one `villagefriends:homestead_start` jigsaw (`up_north`, at Y=1, near the middle of the footprint), and its residents carry entity tags: `villagefriends.dweller.<role>`, plus `villagefriends.gender.male|female` where it matters.
- **Placement** is `tools/homesteads.json`: each homestead's biomes, weight and roles, the shared terrain survey and the structure set `villagefriends:homesteads` (random spread, spacing 16 chunks, separation 6, at least 10 chunks from any village). Each homestead is a `villagefriends:village` structure of depth 1 (its one jigsaw leads nowhere; at depth 0, 26.3 places nothing at all), so it gets the village survey (flat, dry, its own biome), sits at the median ground height, and keeps wild trees out of its yard. `python tools/create_village_structures.py` writes the structures, pools, biome tags, the set and the tag `#villagefriends:homesteads`, and checks every homestead's anchor and residents against `homesteads.json`. The catalog marks the templates `use: homestead`, so village housing never reads them.
- **Settling in** (`dev.villagefriends.homestead.Homesteads.settle`, on load): a tagged villager gets the `villagefriends:dweller` attachment (`Dwelling.Dweller`: role, own name, place, homestead id, its middle), a personality and gender to suit, one surname per couple (with a shared complexion, so the name pools stay right), their biome's villager type and their nameplate. `VillageSettlements.identify` skips them.
- **Rules** are pure in `Dwelling` (unit-tested in `HomesteadTest`): roles, place names, nameplates, `adjust` (the day without village places, and the veteran's watch) and `doing`. `ResidentRoutines` applies `plan`, `steer` (the tether and the watch) and `doing`.
- **Talk:** `TalkWorld.context` adds `dweller`, `place`, `village`, `partner` and `spouse`; `Talk.pools` sends a dweller to `<role>.*` pools only; `NarrativeEngine.conversation` uses those lines for every topic, news and heart included. Dialogue lives in `tools/dialogue/lines/homesteads-<role>.txt`.

## Add or change a homestead

1. Edit its design (or add `buildings/homesteads/<name>.py` with `DESIGNS = {'homesteads/<name>': ...}`), with one `start(...)` and its residents placed with `dweller(...)`.
2. `python tools/design_village.py homesteads/<name> --preview` and look at `build/previews`.
3. Add or update its entry in `tools/homesteads.json` (biomes, weight, roles), then `python tools/create_village_structures.py --check` and `python tools/create_village_structures.py`.
4. A new role needs a `Dwelling.Role` (personality, place names), a dialogue file with every pool `DialogueBankTest.homesteadFolkHaveSomethingToSayOnEveryTopic` lists, and `python tools/dialogue/dialogue.py`.
5. `gradlew.bat runClientGameTest -Ptests=HomesteadGameTest` places every homestead with `/place structure`, checks its residents and talk, and saves screenshots `homestead-<name>-1/2` under `build/run/clientGameTest/screenshots`. To look at them in the gallery: `-PvillageGallery -Pgallery=homesteads/farmstead,homesteads/watchtower`.
