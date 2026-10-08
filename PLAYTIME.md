# Children at play

Village children play together. During their free time (the "Playing" parts of their day, playing in the snow or rain, and Market Day) a child first plays on their own the vanilla way: running about, jumping on beds, chasing other children. After a while they get **bored**. A bored child then joins a game already going nearby, rounds up the children around them for a new one, or, now and then, goes to see what a nearby player is up to and **follows them around**.

## When children get bored

| Personality | Plays alone for about |
|---|---|
| playful, adventurous | 20 s |
| curious, imaginative, warmhearted | 30 s |
| reserved, meticulous, thoughtful | 55 s |
| everyone else | 40 s |

After a game or a follow, a child takes a 25–70 second breather before boredom starts building again.

A bored child picks the first of these that fits:

1. **Join in.** A game with room within 18 blocks lets them in: tag at any time, hide-and-seek while the seeker is still counting, ring-around-the-rosie between rounds, follow the leader between moves, and catch while the ball is being held (up to three players).
2. **Follow a player.** If a player they can see is within 12 blocks, they may tag along instead of starting a game. Curious children do this most often (50 in 100), the reserved hardly ever (6 in 100). With nobody else to play with, every child is 30 points more likely to. At most three children follow one player.
3. **Start a game** with up to five other free children within 16 blocks.
4. With nobody around, they try again a little later.

## The games

Groups choose a game by headcount, weighted by what each child likes. The game they just played is a quarter as likely to come up again. Each game lasts its own length plus up to half again.

| Game | Players | Length | Favored by |
|---|---|---|---|
| **Tag** | 2–6 | 2 min | playful, adventurous |
| **Hide-and-seek** | 2–6 | 3 min | imaginative, curious, reserved, playful |
| **Ring-around-the-rosie** | 3–7 | 75 s | warmhearted, gentle, playful |
| **Follow the leader** | 3–6 | 100 s | steadfast, protective, imaginative |
| **Catch** | 2–3 | 100 s | pragmatic, steadfast, adventurous |

**Tag.** Whoever is "it" counts to three, then chases the nearest child. Runners scatter away from "it" inside a 12-block field and stop to taunt when "it" is far off. A tag swings the tagger's arm, pops a "!" over the tagged child, and the tagged child counts to three before giving chase. There are no tag-backs for four seconds.

**Hide-and-seek.** The seeker walks to home base (the middle of the group), turns away from where everyone is going and counts for 11 seconds with eyes covered. The others pick hiding places 6–16 blocks out, preferring spots with something between them and home base: walls, houses, trees, a roof overhead. Every place is checked to be reachable. They tiptoe there and crouch, giggling and peeking out. "Ready or not": the seeker wanders toward hiding places (and now and then somewhere nobody is), peering about. A child is found when the seeker can see them up close, or by luck a bit further off. The seeker points ("Found you!"), and found children go back to home base and watch. Anyone still hidden after 75 seconds wins and cheers. The first child found counts next round.

**Ring-around-the-rosie.** The children find an open patch, join hands in a ring (wider for more children) and skip round it together for about a lap. Then they **all fall down**, laughing on the grass, get up and go round the other way. Three rounds.

**Follow the leader.** The leader marches off to waypoints around the playground, and the others follow in a line, each a pace behind the one in front. Now and then the leader stops and shows a move: bunny hops, star jumps, a spin, flapping like a bird, stomp stomp clap, or a salute. The line copies it one child after another down the line. Every 30 seconds the leader goes to the back and the next child leads.

**Catch.** Two or three children spread out around a leather ball. Whoever holds it looks round, picks someone and throws it overhand. The ball flies in an arc (thrown at 0.6 s, landing 0.8 s later) and is passed round in turn; with three, sometimes to whoever isn't expecting it. About one catch in seven is fumbled: the ball bounces past, the catcher clutches their head, laughs and runs to pick it up.

## Following a player

A curious child tags along 2.6 blocks behind a player (a bit further back for the second and third child), tiptoeing when the player walks and hurrying when they sprint. When the player stops, the child stops too and watches closely, leans in for a better look or wonders what they're doing, now and then with a "?" or a light bulb.

**When the player turns round and looks at them, they freeze and act innocent:** hands behind their back, looking up and rocking on their heels, or suddenly very interested in the sky, with a blush or a nervous sweat. As soon as the player looks away, they carry on following.

They wave bye-bye and go back to playing after 40 seconds to two minutes. They also stop if the player gets more than 22 blocks away, sprints off (they look glum about it), or leads them more than 44 blocks from their village.

## When games stop

A game ends, and vanilla takes over again, when:

- its time is up, or too few children are left to play it;
- free time ends: lessons, lunch, supper, a storm, or rain for children who don't like it;
- a monster comes within 16 blocks or the village is raided (the children panic and run as usual);
- a child is hurt, knocked out, falls asleep, grows up or is recruited (that child leaves; the rest carry on if enough remain).

Games aren't saved. A game in progress simply stops when the world closes.

## The leather ball

**Leather Ball** (`villagefriends:leather_ball`) is a new item in the Supplies tab, stacks to 16. It's the ball the children throw in catch, drawn in the holder's hand and in flight between children. Its sprite comes from `python tools/playground/sprites.py` (`--check`, `--preview`).

## How it works

- `play/Games.java` is pure and unit-tested (`PlayTest`): the games, who likes what, choosing a game, boredom, curiosity, how long things last, the leader's moves, and the state strings.
- `play/Playground.java` runs it in the world. `ResidentRoutines` calls `Playground.update` once a second for every resident; a child in a game or following a player is driven every tick by their session (tag, hide-and-seek, ring, follow the leader, catch, curious), and their brain rests meanwhile (one line in `VillagerCompanionMixin`). Sessions live in memory only.
- Each child's part is shared with clients through the synced attachment `villagefriends:play`: `tag:it`, `hide_and_seek:hidden`, `ring:fall`, `follow_the_leader:do:star`, `catch:throw:<entity id>[:miss]`, `curious:caught`... `Games.doing` turns it into the status line ("Playing tag", "Hiding", "Following you around").
- On the client, `PlaytimeClient` adds the animation tags and draws the ball. The director in `ResidentLife` plays a `play` clip each time a child's part changes and repeats clips while it lasts. Throws, falls, found, tagged, fumbles, wins, goodbyes and leader moves play once. Play clips run on the reaction layer, so they keep the upper body while the child runs.

## Animations

37 clips in `tools/animations/village_life/games.py` (Village Life now has 431), using the new `play` trigger. Tags are `game:<game>`, `game:<game>:<role>`, the full state for leader moves, and `moving` while the child is on the move:

| Game | Clips |
|---|---|
| Tag | counts to three, chases with arms out, looks for someone to tag, runs away squealing, can't catch me! |
| Hide-and-seek | counts with eyes covered, tiptoes off to hide, giggles in hiding, peeks out from hiding, searches high and low, peers behind things, found you!, aww found!, waits at home base, wins hide-and-seek |
| Ring-around-the-rosie | skips round in a ring holding hands, all fall down! |
| Follow the leader | marches proudly; moves: bunny hops, star jumps, spins round, flaps like a bird, stomp stomp clap, salutes smartly |
| Catch | ready to catch, holds the ball and picks someone, throws the ball, catches the ball, fumbles the catch |
| Following a player | tiptoes after you, skips along behind you, watches you closely, leans in for a better look, wonders what you're doing, acts innocent, is suddenly very interested in the sky, waves bye-bye |

Leader moves must keep the lengths in `Games.Move` (ticks / 20). The throw releases at `Playground.RELEASE` and the catch lands at `RELEASE + FLIGHT`. `PlayTest` checks both, and that every part of every game has a clip.

## Verification

- `gradlew test` (`PlayTest` and the animation pack tests).
- `python tools/animations/games_preview.py` writes a looping animated WebP of every game clip to `build/previews/games/`. Clips used while running are shown over a stand-in running gait, since in game the walk drives their legs.
- `python tools/animations/animations.py --check`, `python tools/animations/vlcheck.py tools/animations/village_life/games.py --sheet build/previews/games.png`.
- `gradlew runClientGameTest -Ptests=PlaygroundGameTest` plays every game with four children on a playground with walls. It checks roles, hiding, the ring, copied moves, the ball in flight, a child following and freezing when looked at, games stopping for a monster, and bored children starting something on their own. Screenshots are `playground-*`.
