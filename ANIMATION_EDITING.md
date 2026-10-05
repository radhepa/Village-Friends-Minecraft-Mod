# Resident movement and eyes

Walking and facial presentation live in the existing resident renderer. They do not change AI, hitboxes, movement speed, professions or saved appearances.

`src/main/java/dev/villagefriends/ResidentMotion.java` defines six gait styles. A resident's UUID selects its gait and small cadence/timing differences, so changing jobs or reloading a world keeps the same movement identity. Gaits are independent of complexion and clothing. `ResidentAnimation.java` applies these parameters to both `ResidentModel` and `ResidentArmorModel`, preventing armor from walking out of alignment.

Keep movement small: gait sway is under two degrees; torso twist is about 1.5 degrees; the strongest step lift is less than one model pixel. Idle feet stay still. Active item-use, attacks, seats, water, airborne, crouching, sleeping and death poses retain their vanilla body animation. Children use the existing baby transformer and slightly quicker, shorter strides.

`ResidentModel.java` adds two small eye patches beneath the volumetric hair. Each patch samples the original skin's eye white, iris and complexion directly from the native face UVs: whites at `(9,12)` and `(14,12)`, irises at `(10,12)` and `(13,12)`, eyelids at `(12,12)`. Upper and lower lids meet at the center; a tiny closed-eye crease samples the existing facial shade at `(11,14)`. These coordinates are preserved in the new body-only texture atlas. Resource packs that move the eye line should also update these coordinates and patch placement. Pupils remain within the existing two-pixel-wide, one-pixel-high eye regions.

Blink timing comes from `ResidentMotion.blink`: about 0.2 seconds per blink, an individual interval of roughly five to eight seconds, varied timing within each cycle and occasional double blinks. There are no random draws, timer allocations, extra skin images or texture uploads per frame. Sleeping and dying residents have closed eyes. `ResidentRenderer` supplies small pupil offsets toward the camera within six blocks and a front-facing cone; these eye movements do not turn the resident's AI or body.

Build with `build.ps1`. Run focused native verification with the existing Java 25 environment:

```text
gradlew.bat runClientGameTest -PanimationsOnly
```

The test renders the six walking styles at two sample moments, a close eye gallery and the actual conversation portrait, and exercises pathfinding-driven walking, armor alignment, special poses, children, helmets, texture-cache behavior and reload. Preview screens and test classes stay outside the release JAR.

