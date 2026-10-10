# Resident animation packs

Residents choose what to do from moment to moment. Standing residents fidget, practice their trade or hobby, chat with a neighbor beside them, greet a player who walks up, gesture while you talk with them, and react to jokes, gifts, trades, hearts, anger, fear and harm. Every one of those motions is a **clip** in an **animation pack**. The first pack, **Village Life**, ships with the mod.

Packs are client resources. A resource pack can add new packs, replace the bundled one, or switch individual clips off. Packs only describe motion; the director in `ResidentLife.java` decides when each clip plays. Nothing about animation is saved in worlds or sent to the server.

## Village Life (pack 1)

The pack grew in 2.15.0 from 99 to 349 clips: three or more work motions for every profession, three hobbies per personality, more everyday moments, greetings, conversation gestures, neighbor chats and reactions, thunder, dawn and dusk, and twice as many children's games.

462 clips (453 distinct motions; a few serve two situations). Version 2.20 added eleven birthday-party clips, 2.21 twenty-four for playing with pets, 2.22 thirty-seven for children's games, 2.27 twelve for eating a meal at home standing up (Hearth & Harvest), and 2.28 nineteen for fishing from a dock or the water's edge (Tall Tales Fishing).

| Situation | Clips |
|---|---|
| Everyday idles | looks around, shifts weight, big stretch, yawns, scratches head, crosses arms, hands on hips, rocks on heels, hums a tune, dusts off sleeves, rolls neck, wipes brow, rubs hands together, kicks a pebble, sneezes, pats pockets, shrugs, side stretch, taps foot, watches the sky, cracks knuckles, checks fingernails, adjusts collar, tucks hair behind an ear, brushes off a shoulder, leans back against a wall, stomach growls, scratches an itch on the back, swats away a bee, rubs an itchy nose, blows a hair strand off the face, rolls the shoulders, touches toes, squints at the sun, daydreams, deep sigh, has the hiccups, wiggles a finger in an ear, checks a boot sole, stamps mud off the boots, twirls a lock of hair, fans self on a hot day, coughs into an elbow, arm circles, shuffles feet restlessly, drums fingers on a folded arm, waves to a neighbor across the way, catches a falling leaf, balances on one leg, points up and counts the clouds |
| Hobbies, three per personality | **warmhearted**: kneads dough, knits a scarf, feeds the birds; **thoughtful**: reads a book, mulls it over, reads a letter; **playful**: conducts a tune, juggles three balls, dances a little jig; **adventurous**: scouts the horizon, peers through a spyglass, shadowboxes; **meticulous**: inspects a trinket, sweeps the step, tallies a list; **steadfast**: tends the soil, splits firewood, hauls two buckets of water; **reserved**: casts a fishing line, sips tea, skips a stone; **imaginative**: frames the view, shapes clay, acts out a tale; **pragmatic**: whittles wood, weaves a basket, mends a fence; **curious**: stargazes, peers through a lens, tinkers with a gadget; **protective**: sands a plank, practices a fighting stance, keeps watch; **gentle**: smells a flower, pets a cat, waters the flowers |
| Work for every profession | **armorer**: hammers at the anvil, polishes a breastplate, taps in rivets, quenches a piece in the trough; **toolsmith**: hammers at the anvil, grinds a blade on the treadle wheel, files an edge, tests a tool's heft; **weaponsmith**: hammers at the anvil, sights down a blade, whets a blade, pumps the bellows; **mason**: hammers at the anvil, chisels stone, trowels mortar and sets a brick, checks a plumb line; **carpenter**: hammers at the anvil, saws a plank, measures in hand spans, planes a board; **farmer**: hoes the rows, broadcasts seed, harvests with a sickle, hoists a sack onto the shoulder; **fisherman**: mends a net, reels in a catch, untangles a line; **shepherd**: stitches cloth, shears a sheep, calls the flock, leans on a crook; **leatherworker**: stitches cloth, stretches a hide, punches holes with an awl, burnishes an edge; **butcher**: chops vegetables, hones a knife on a steel, cleaves a joint, wraps and ties a parcel; **cartographer**: writes notes, unrolls a map and studies it, walks dividers across a chart, takes a compass bearing; **librarian**: writes notes, shelves a book up high, dusts the shelves, sorts a stack of books; **cleric**: prays, raises a hand in blessing, swings a censer, rings a handbell; **fletcher**: sights down an arrow, fletches an arrow, rolls an arrow to check it is true, strings a bow braced against the foot; **knight**: stands guard, runs a sword drill, drills shield blocks, stretches in lunges, kneels and pledges, rests both hands on the pommel, whets the sword with a stone, checks the blade for nicks, salutes with the sword into a high guard, and holds the line with sword raised while mustered for a raid; **archer**: sights down an arrow, stands guard, practices the draw, tests the wind, nocks an arrow from the quiver, plucks the bowstring and listens, holds a full draw on the horizon, shades the eyes and scans the dark, flexes the bow limb, waxes the bowstring, and waits with an arrow on the string while mustered for a raid; **cook**: chops vegetables, stirs the pot, tastes from the spoon, sprinkles a pinch of salt, tosses the pan; **tavern keeper**: stirs the pot, pours a drink, polishes a mug, wipes the counter, balances a tray overhead; **apothecary**: stirs the pot, grinds with mortar and pestle, measures drops from a vial, sniffs a potion and recoils; **painter**: paints broad strokes on a canvas, mixes colors on a palette, measures the subject with a thumb; **bard**: strums a lute, plays a flute, sings a ballad; **tailor**: stitches cloth, measures with a tape, cuts cloth with shears, threads a needle; **scholar**: writes notes, polishes spectacles, has a eureka moment, reads down an unrolled scroll; **unemployed**: twiddles thumbs, counts coins, sighs and slumps, whistles while waiting; **nitwit**: twiddles thumbs, does a silly dance, marvels at their own hands, stumbles and recovers, loses count on their fingers |
| Greetings | waves hello, bows politely, nods hello, salutes, waves excitedly, tips a hat, curtsies, casual salute, hand on heart, opens arms in welcome, small shy wave, beckons you over, raises a palm, bows with a flourish, double-takes and waves, fist-to-chest salute, jumps and waves, peeks out and waves, bounces with excitement |
| Talking with you | shrugs, explains, gestures with both hands, points to self, nods along, thinks it over, tilts head, counts on fingers, chuckles, gasps, jabs a finger for emphasis, speaks from the heart, thumbs back over the shoulder, shows how big it was, whispers behind a hand, taps the temple knowingly, waves it off, palms up: why?, rubs the chin thoughtfully, proudly thumbs own chest, sweeps an arm across the horizon, steeples the fingers, flaps both hands excitedly, points right at you |
| Chatting with a neighbor | speaking: explains, gestures with both hands, counts on fingers, tells a story, points somewhere, gossips behind a hand, acts it out, complains with hands on hips, laughs at own joke, draws a shape in the air, pats their shoulder, the fish was THIS big, rants and waves the arms, confides with a sigh, bounces with excitement; listening: nods along, listens politely, chuckles, listens with arms folded, gasps, listens with chin in hand, squints skeptically, leans in curiously, slaps a knee laughing, rolls a hand: go on, stifles a yawn, winces in sympathy, clasps hands in delight, tsk-tsks, scratches head in puzzlement |
| Reactions | **a joke**: belly laugh, giggles, slaps a knee laughing, snorts with laughter, wheezes with laughter, shakes with silent laughter, points and laughs; **a loved gift**: cheers, hugs the gift, jumps for joy, spins with joy, happy shimmy, gasps with joy, raises the gift like a trophy; **a gift**: bashful thanks, grateful nod, bows with a hand on the heart, two-handed handshake, tips their hat, says you shouldn't have, presses the gift to their heart; **a refused gift or trade**: shakes head, wags a finger, crosses arms in an X, pushes it back, turns up their nose, hands up: not for me, shakes head apologetically; **happy sparkles**: cheers, claps, fist pump, hops and claps, thumbs up, wiggle dance, beams with arms wide open, skips in place; **hearts**: bashful thanks, lovestruck, swoons with hands on cheeks, blows a kiss, heart flutters, dreamy sigh, shy toe twist; **angry clouds**: huffs, shakes a fist, stomps both feet, rants and flails, points and scolds, gives the cold shoulder, shakes with clenched fists; **raid sweat**: nervous glances, bites their nails, wrings their hands, glances over a shoulder, tugs at a sweaty collar, knees knocking; **harm**: flinches, staggers, clutches a hurt arm, doubles over winded, hops on one foot clutching a toe |
| Weather and time of day | hunches in the rain, catches raindrops, shakes off the rain, shivers, shelters head from the rain, wrings out a sleeve, splashes in a puddle, looks glumly up at the clouds, jumps at a thunderclap, covers ears in the thunder, stamps feet to keep warm, hugs self against the cold, blows into cupped hands, rubs sleepy eyes, greets the morning sun, nods off standing up, wishes on a star, watches the fireflies |
| Birthday parties | **guests at the party**: claps along, raises a cup in a toast, sways to the music, dances a jig, laughs, waves both arms in a cheer, hums along; **children at the party**: bouncy hops with flapping arms; **the guest of honor**, all day: makes a wish and blows out the candles, bows thanks with a hand on the heart, beams and rocks on their heels |
| Children | hops, twirls, plays airplane, peekaboo!, watches a bug, wants to play tag, skips rope, plays hopscotch, spins until dizzy, rides a hobby horse, builds a sandcastle, blows a dandelion, plays at swords with a stick, pretends to be a monster, plays pat-a-cake, tosses a ball up and catches it, counts for hide-and-seek, throws a stomping tantrum, measures their height, flaps like a bird, makes silly faces, marches like a soldier |
| Pets | coaxes a stray with a treat, takes the stray home, sighs as the stray backs away, pats their knees: come here!, claps for the pet, laughs with hands on knees, watches the cat fondly; **dogs**: teases with a stick, throws the stick, watches the dog run, takes the stick back, pats the dog's head, rubs the dog's belly, holds up a treat: sit!, tosses the treat, shakes the dog's paw, twirls a finger: spin!, tags the dog: you're it!; **cats**: dangles a bit of string, strokes the cat, scratches the cat's chin, swishes a feather, offers a fish, pats the cat gently |
| Fishing (`angling`) | **casting**: casts the line overhead, flicks a sidearm cast; **waiting**: waits for a bite, glances along the bank, tugs the hat and scratches the head, stretches the free arm, yawns over the water, taps a foot, jiggles the rod tip to tempt a fish; **a bite**: jolts at the bite, leans in and grips the rod with both hands; **reeling in**: hauls back and reels in, cranks the reel with the rod tip high, fights the fish side to side; **a catch**: holds the catch up and admires it, shows off the catch, weighs it in hand and nods; **the one that got away**: slumps as the line goes slack, shrugs it off |
| Games together (`play`) | tag, hide-and-seek, ring-around-the-rosie, follow the leader (six copied moves), catch with a leather ball, and following a player around: 37 clips, listed in [PLAYTIME.md](PLAYTIME.md#animations) |

## How the director chooses

Each resident is ticked on the client. When they have stood still for a second and their last clip has finished, they rest for a moment (shorter for lively personalities and children), then pick a clip for the situation:

| Trigger | When |
|---|---|
| `idle` | Standing around: everyday idles, work, hobbies, weather and children's play all compete by weight. |
| `chat_speak`, `chat_listen` | Another resident stands within about three blocks in front of them. Partners take turns speaking and listening every few seconds. |
| `greet` | A player who was away walks up within five and a half blocks in front of them (once a minute at most), or a conversation opens. The head turns to the player. |
| `talk` | The player has this resident's conversation window open. |
| `laugh`, `delighted`, `thanks`, `decline` | Conversation outcomes: a joke, a loved gift, an accepted gift, a declined gift. `decline` also plays when a resident refuses to trade. |
| `happy`, `love`, `angry`, `nervous` | Vanilla villager events: happy sparkles, hearts, angry clouds, raid sweat. |
| `hurt` | The resident takes damage. |
| `pet` | Playing with their cat or dog, or befriending a stray: the server says which part of the game they're on (`play:<phase>`, with `pet:cat` or `pet:dog`). See [PETS.md](PETS.md). |
| `angling` | Fishing from a dock or the water's edge: the server says which part of it they're on (`angling:<phase>`: `cast`, `wait`, `bite`, `reel`, then `catch` or `lost`), a new clip from the same part starts whenever one ends (so the long wait loops through its variants), and a change of part cross-fades. |
| `play` | A child's part in a game changes, and again each time the clip ends while it lasts (throws, falls, leader moves and the like play once). See [PLAYTIME.md](PLAYTIME.md). |

Reactions play on a second layer and briefly replace the current activity. While walking, reactions keep their upper body and leave the stride alone; activity clips fade out when a resident starts moving.

Clips are eligible by **tags** describing the resident and the moment:

| Tag | Meaning |
|---|---|
| `adult`, `child` | Age. |
| `job:<profession>` | `job:farmer`, `job:knight`, `job:none`, `job:nitwit`... Also `smith` for armorer/toolsmith/weaponsmith and `guard` for knight/archer. |
| `personality:<id>` | The resident's personality from the content pack (`warmhearted`, `playful`...). |
| `morning`, `day`, `evening`, `night` | Overworld time. |
| `rain`, `thunder`, `cold` | Rain falling on the resident, a thunderstorm, a snowy biome. |
| `holding`, `social` | Something in the main hand; a chat partner nearby. |
| `routine:<part>` | The part of their day (`routine:work`, `routine:party`...). Work clips are boosted during working hours, hobby clips during free time, and party clips five times while a birthday party is on. |
| `birthday` | It's this resident's birthday (they wear the party hat). |
| `game:<game>`, `game:<game>:<role>`, `moving` | A child's part in a game (`game:tag:it`, `game:catch:throw`, `game:follow_the_leader:do:hop`...), and being on the move. |

A resident never repeats their last two clips if anything else fits. About one resident in nine is left-handed and mirrors one-handed gestures.

## File format

Packs live at `assets/<namespace>/resident_animations/<pack>.json`. The bundled file is `assets/villagefriends/resident_animations/village_life.json`; a resource pack with a file at that path replaces it. A pack's clips are named `<pack>:<clip>` (`village_life:yawn`); packs from other namespaces are named `<namespace>.<file>`. Later packs replace clips with the same name. Use F3+T to reload. A pack that fails validation is skipped and named in the log; the others still load.

```json
{
  "format": 1,
  "name": "My Pack",
  "description": "Optional.",
  "disable": ["village_life:sneeze"],
  "clips": [
    {
      "id": "polite_wave",
      "name": "Polite wave",
      "trigger": "greet",
      "length": 2.0,
      "weight": 3,
      "require": ["adult", "personality:reserved|personality:gentle"],
      "avoid": ["rain"],
      "boost": {"morning": 2},
      "blend": [0.25, 0.35],
      "mirror": "hand",
      "items": "keep",
      "tracks": {
        "right_arm.rot": [[0, 0, 0, 0], [0.4, -20, 0, 120], [1.2, -20, 0, 130], [2.0, 0, 0, 0]],
        "head.rot": [[0, 0, 0, 0], [0.6, 10, 0, -6], [2.0, 0, 0, 0]],
        "eyes.lid": [[0, 0], [0.5, 0.3], [2.0, 0]]
      }
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `format` | Always `1`. |
| `disable` | Clip names from other packs to switch off. |
| `id` | Lowercase letters, digits and underscores. |
| `trigger` | One of the triggers above (default `idle`). |
| `length` | Seconds, up to 30. |
| `weight` | Relative chance against other eligible clips (default 1). |
| `require` | Every entry must match; `a|b` matches either tag. |
| `avoid` | Any matching tag rules the clip out. |
| `boost` | Weight multipliers for matching tags. |
| `blend` | Seconds to fade in and out (default 0.25, 0.35). |
| `mirror` | `hand` mirrors for left-handed residents (default), `free` also mirrors at random, `never` keeps it as written. |
| `items` | `keep` (default) leaves an arm that holds an item in its vanilla pose; `override` animates it anyway, so a smith's hammer swings. |

**Tracks** are named `<bone>.rot`, `<bone>.pos`, `eyes.lid` or `eyes.look`. Keys are `[seconds, x, y, z]` (`[seconds, value]` for `eyes.lid`, `[seconds, x, y]` for `eyes.look`) with strictly increasing times inside the clip. Values between keys follow smooth monotone curves: they never overshoot a key and hold still between equal keys. Start and end every track at zero so clips blend cleanly.

| Bone | Pivot |
|---|---|
| `head`, `body`, `right_arm`, `left_arm`, `right_leg`, `left_leg` | Their own joints. |
| `waist` | Bends the body, head and both arms together at the hips, so bows keep the feet planted. Rotation only. |
| `root` | Turns the whole resident about the feet; `root.pos` lifts or lowers them (a hop). |

Rotations are degrees added to the live pose (vanilla look direction, gait and breathing), in Minecraft's model space: a negative `x` raises a limb forward (−90 points it ahead, −180 straight up), while a positive `x` tips the head down and bends the waist forward. For the right arm and leg, positive `z` lifts the limb outward; for the left side, negative `z` does. Once an arm is raised above the shoulder, `z` tips it the other way, so a V overhead is easiest as a side raise (`[x≈-10, 0, ±160]`). Positions are model pixels (`y` negative is up, `z` negative is forward), written for an adult; children scale them to their size. `eyes.lid` closes the eyes from 0 to 1 on top of natural blinking; `eyes.look` moves the irises (`x` positive toward the resident's left, `y` positive down), kept inside the eye whites.

## Authoring Village Life

The bundled pack is written in Python with `tools/animations/kit.py`, which uses mirror-friendly conventions (both arms lift outward with positive roll) and converts to model space. Never hand-edit the compiled JSON.

```text
python tools/animations/animations.py             # compile tools/animations/village_life/*.py
python tools/animations/animations.py --check     # validate and confirm the JSON is current
python tools/animations/animations.py --list      # every clip, its trigger and length
python tools/animations/preview.py sheet --clips yawn,cheer --frames 6 --scale 6   # offline poses
python tools/animations/vlcheck.py tools/animations/village_life/trades.py --sheet out.png --clips a,b
                                                  # check and preview one module on its own
gradlew.bat runClientGameTest -PanimationPack     # in-game checks and a still of every clip
gradlew.bat runClientGameTest -PanimationVideo    # 30 fps showcase frames (development only)
python tools/animations/film.py                   # titles, crossfades and an H.264 MP4
```

| Module | Clips |
|---|---|
| `everyday.py`, `moments.py` | Everyday idles anyone does while standing around. |
| `hobbies.py`, `pastimes.py` | Three hobbies for each personality. |
| `work.py`, `trades.py`, `crafts.py`, `guards.py` | Work: vanilla professions in `trades.py`; Village Friends professions, carpenters, the unemployed and nitwits in `crafts.py`; knights and archers with the sword or bow in hand in `guards.py`. |
| `social.py`, `company.py`, `chatter.py` | Greetings, talking with you, and neighbors chatting. |
| `reactions.py`, `feelings.py` | Reactions to jokes, gifts, refusals, vanilla events and harm. |
| `weather.py`, `skies.py` | Rain, thunder, cold, dawn and dusk. |
| `children.py`, `playtime.py` | Children's games. |
| `pets.py` | Playing with a cat or dog and befriending a stray (`pet` trigger). |
| `party.py` | Birthday parties: guests and children at the party, and the guest of honor. |
| `games.py` | Games children play together and following a player (`play` trigger). |
| `meals.py` | Eating a dish at home, standing (`dining:eat` with `food:<kind>`, then `dining:done`; never while `seated`, where the Tavern pack's dining clips play). See [HEARTH_AND_HARVEST.md](HEARTH_AND_HARVEST.md). |
| `angling.py` | Fishing (`angling` trigger with `angling:<phase>`). The rod is in the right hand (the fish during `catch`), so no clip mirrors and the rod arm is written with `held()` as the total angle it reaches over vanilla's held-item pose; `rod()` keeps the rod still while the waist leans. |

Weights keep each resident's trade and hobbies visible among the everyday idles: work clips weigh 3–6 (the two raid-muster clips, which require `routine:defend`, weigh 40 so mustered guards mostly stand ready), hobbies 3–4, everyday idles 1–5 (most of the newer moments about 1), and weather clips only compete when their weather applies. Every greeting requires an age (`adult`, `child` or `adult|child`). Clip names never contain commas.

`-PanimationVideo` takes `-PfilmScenes=gallery,village` and `-PfilmStride=15` (every fifteenth frame, for checking composition). It builds a procedural village on a superflat world, stages residents around the fountain and steps a frozen world one tick per frame, rendering between ticks, so the footage is smooth and repeatable.
