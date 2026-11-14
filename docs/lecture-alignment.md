# Lecture alignment of the implemented homework

This covers the existing systems and the changes made in this chat. Gameplay runs in saved Unreal Blueprints. Python is used outside the game to call editor MCP tools and record checks.

## Requirements and corrections

The assignment supplies the required behavior. The user's 14 November clarification supersedes the stale PDF ranges: use X [-1000,1000] and Y [-2000,2000]. The placed SpawnManager's original overrides were restored. Actor Z still equals manager Z; grounding adjusts child components instead of changing the spawn transform.

| Work | Lecture or assignment basis | Implementation |
| --- | --- | --- |
| Shared pickup behavior, three mesh variants | Blueprints Introduction, slides 5-8: components, functions/events, inheritance and class roles | Existing `BP_CollectibleBase` with Coin, Gem and Potion children. No separate gameplay scripts per item type. |
| Random spawning and configurable parameters | Assignment 01; Data Structure, Blueprint Animations Intro, slides 5-13 and 18: arrays and class references | Existing spawn function, random class array, exposed count/bounds/score variables. Existing loop retained. |
| Player stores accumulated score | Assignment 01; Interactions in Blueprints, slide 3: functions and references | Existing `AddScore` updates `TotalScore` and broadcasts `OnScoreChanged`. Score ownership remains in the player. |
| Score UI notification and Print String | Assignment 01; Interactions in Blueprints, slide 14: event dispatchers and loose coupling | `WBP_ScoreHUD` binds to the player dispatcher, updates its Text Block and prints the new total. It unbinds its listener on Destruct. The controller creates the widget once, preserving its original input/touch setup. |
| Grounded meshes and reachable pickup collision | AI for NPCs & Dynamic Animations, slides 9-12: line trace; Character, Physics & Input, slides 21-28: collision; Blueprint functions and component hierarchy | Base `PlaceOnGround` traces down once at BeginPlay. Mesh bounds place the visible bottom just above the hit surface. Mesh and sphere share a stable Scene Component root, so the actor's required Z stays unchanged. Child trace defaults match the base. |
| E interaction | Character, Physics & Input, slides 5-13: Enhanced Input actions and mapping contexts | Boolean `IA_Interact` maps to E in `IMC_Default`. The character uses Started and inspects overlapping door actors when pressed. |
| Door proximity and player validation | Assignment 01; Interactions in Blueprints: references, casting and validations; Character, Physics & Input: overlap collision | A Box Collision defines the interaction area. `TryOpen` checks player identity and actual overlap; entering alone does not open the door. No persistent nearby-door reference is needed. |
| Smooth opening by 90 degrees | Assignment 01; AI for NPCs & Dynamic Animations, slides 15-24: rotation, interpolation and Timeline | A real Blueprint Timeline drives hinge rotation from the closed pose to `OpenAngle`, using normalized playback position as interpolation alpha. Angle defaults to 90 degrees and duration to one second. Opening/open flags prevent accumulated rotation or restart loops. |

The small UMG widget is the presentation container for the assignment's requested UI notification. Its gameplay communication uses the lecture's event-dispatcher pattern; it does not poll score every frame or maintain another total.

The ground adjustment uses component bounds to account for different Fab mesh pivots and scales. A one-centimeter clearance prevents surface intersection. Trace height, depth and clearance are exposed parameters. The trace runs at spawn, not on Tick.

## Editor tooling and verification

- Epic's bundled MCP, Blueprint and widget toolsets are enabled for the Editor target only.
- `tools/unreal_mcp.py` is a local editor client; no Python gameplay or C++ gameplay module was added.
- Temporary input-test Blueprints injected Enhanced Input for Play verification without operating the user's keyboard. These fixtures were removed before final delivery.
- Test code and scratch schemas under `Saved/Automation` are not project gameplay and are ignored by Git.
- Final observations and limitations are recorded in `docs/progress.md` and `docs/evidence/`.

NPCs, weapons, combat, multiplayer services, new animation systems, persistence and purchases were not added to this homework.
