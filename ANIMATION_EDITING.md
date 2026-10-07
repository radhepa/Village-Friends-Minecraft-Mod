# Resident movement, animation packs and eyes

Walking, idling, gestures and facial presentation live in the resident renderer. They do not change AI, hitboxes, movement speed, professions or saved appearances. Two layers make residents feel alive:

1. **Always-on motion** (`ResidentAnimation.java`): individual gaits, breathing, a slow weight shift from hip to hip, a head that keeps drifting between the AI's look targets, a forward lean when hurrying, blinking and glances.
2. **Animation packs** (`ResidentLife.java`, `ResidentPoser.java`): authored clips the resident chooses for themselves: idles, work, hobbies, chats, greetings and reactions. Read [ANIMATION_PACKS.md](ANIMATION_PACKS.md) for the clip list, the director's rules and the pack format.

## Gaits

`src/main/java/dev/villagefriends/ResidentMotion.java` defines six gait styles. A resident's UUID selects its gait and small cadence/timing differences, so changing jobs or reloading a world keeps the same movement identity. Gaits are independent of complexion and clothing. `ResidentAnimation.java` applies these parameters to both `ResidentModel` and `ResidentArmorModel`, preventing armor from walking out of alignment.

Keep the walk itself small: gait sway is under two degrees; torso twist is about 1.5 degrees; the strongest step lift is less than one model pixel. Idle feet stay planted (the weight shift only rolls the hips and legs sideways). Active item-use, attacks, seats, water, airborne, crouching, sleeping and death poses retain their vanilla body animation. Children use the existing baby transformer and slightly quicker, shorter strides.

## Animation packs

`ResidentLife` is a client-side director per resident. It runs on client ticks (and holds still when the world is frozen with `/tick freeze`), picks clips with `AnimationLibrary.pick` and fills two layers of the render state each frame: an activity (idle, work, chat, talk) and a reaction (greet, laugh, gift, hurt...). `ResidentPoser` then adds the sampled clips to the live pose in this order: limb and head rotations, the waist (which bends the body, head and arms together around the hips), then the root (which pivots the whole resident about the feet). Both the resident and armor models call the same code, so armor never separates from a pose. An arm holding an item keeps its vanilla pose unless the clip says otherwise; while walking, reactions leave the stride alone.

Rules worth keeping when editing clips or the poser:

- Clips start and end at rest; reactions blend in quickly, activities fade out when a resident starts walking.
- Positions are written in adult pixels and scaled for children.
- Posing allocates nothing per frame and never touches textures.
- The resident's personality reaches the client through the synced `villagefriends:temperament` attachment so body language matches the Journal; the conversation window's portrait plays the same clips as the resident in the world.
- Conversation outcomes are cued from `FriendshipScreen` (joke, gift accepted/loved/declined); vanilla villager events (hearts, angry clouds, happy sparkles, raid sweat) arrive through `VillagerEventMixin`.

## Eyes

`ResidentModel.java` adds two small eye patches beneath the volumetric hair. Each patch samples the original skin's eye white, iris and complexion directly from the native face UVs: whites at `(9,12)` and `(14,12)`, irises at `(10,12)` and `(13,12)`, eyelids at `(12,12)`. Upper and lower lids meet at the center; a tiny closed-eye crease samples the existing facial shade at `(11,14)`. These coordinates are preserved in the new body-only texture atlas. Resource packs that move the eye line should also update these coordinates and patch placement. Pupils remain within the existing two-pixel-wide, one-pixel-high eye regions.

Blink timing comes from `ResidentMotion.blink`: about 0.2 seconds per blink, an individual interval of roughly five to eight seconds, varied timing within each cycle and occasional double blinks. There are no random draws, timer allocations, extra skin images or texture uploads per frame. Sleeping and dying residents have closed eyes. Clips can squint or close the eyes (`eyes.lid`, combined with blinking) and redirect the gaze (`eyes.look`), always inside the eye whites. `ResidentRenderer` supplies small pupil offsets toward the camera within six blocks and a front-facing cone; while greeting or talking, the head also turns toward the player.

## Verification

Build with `build.ps1`. Run focused native verification with the existing Java 25 environment:

```text
gradlew.bat runClientGameTest -PanimationsOnly
gradlew.bat runClientGameTest -PanimationPack
```

`-PanimationsOnly` renders the six walking styles at two sample moments, a close eye gallery and the actual conversation portrait, and exercises pathfinding-driven walking, armor alignment, special poses, children, helmets, texture-cache behavior and reload. `-PanimationPack` checks every clip's armor parity and planted feet, held items, mirroring, eyes and children, then drives real residents through idles, a neighbor chat, a greeting, a conversation (talking, a joke, a loved and a disliked gift), vanilla events, harm, a refused trade and a frozen world, and captures a still of every clip. Preview screens and test classes stay outside the release JAR.
