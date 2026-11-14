# Assignment 01 completion

Status: COMPLETE

Scope: complete the previously identified homework gaps using the adapted feature protocol once engine installation and project startup are verified. The user requested the protocol adaptation on 14 November 2026. Implementation details and the original static audit are in `HOMEWORK_REVIEW.md`.

## Professor clarification

On 14 November 2026 the user confirmed that the professor changed X to [-1000,1000] and Y to [-2000,2000] but did not update the PDF. Preserve the placed manager's original overrides and verify against these corrected bounds. The earlier attempt to reset them to the PDF values has been reversed.

## Required behavior

Spawn 100 random collectible actors from three different types/meshes. Use world X [-1000,1000], world Y [-2000,2000] and manager Z; assign each an integer score [10,100]. Player overlap awards points once and destroys the collectible. Keep the accumulated score in the player, notify UI through an event dispatcher, and print the updated total using Print String. A nearby player pressing E opens a door by 90 degrees using a Timeline.

The assignment's submission date is 16 November 2026. Functionality and code quality each account for half of its grading. Do not expand this task to combat, NPCs or a full game.

## Ownership and expected assets

| System | Owner / assets |
| --- | --- |
| Score state and update | Existing `BP_ThirdPersonCharacter.TotalScore`, `AddScore`, `OnScoreChanged` |
| Score presentation | New `WBP_ScoreHUD`; existing player controller creates it once |
| Collection | Existing `BP_CollectibleBase`; Coin/Gem/Potion children configure meshes |
| Spawn configuration | Existing `BP_SpawnManager`, its class array and exposed variables |
| Interaction input | New `IA_Interact` Boolean action mapped to E in existing `IMC_Default`; character requests interaction |
| Door state/animation | New `BP_InteractiveDoor`: area trigger, hinge Scene Component, Movable mesh and Timeline |
| Placement | Existing `Lvl_ThirdPerson`; save corresponding external actor packages if changed |

Preserve current working movement/camera input, touch-controller setup and Fab asset references. Fix only verified defects needed for this assignment.

## Part 0: installation and baseline

- Verify the installation gate in `docs/WORKFLOW.md` for the approved 5.8.4 build.
- Open the existing project and its default level without silently changing engine association or rendering options.
- Inspect the real collectible and score graphs, manager instance overrides and existing level placement.
- Compile relevant existing Blueprints and record initial Output Log errors/warnings.
- Run a short baseline Play. Inspect the initial actor count before collection; begin outside the spawn area or use an isolated test setup if necessary. Do not save diagnostic setup into the final level.

Checks: installation complete; project/map loads; baseline behavior and errors documented.

Result: PASS. Approved Unreal 5.8.4 installation and the tracked project/default map were verified through native MCP and Play.

## Part 1: score notification and HUD

- Preserve a single score-update path: AddScore updates TotalScore then broadcasts the new total.
- Create the HUD once after the controlled pawn is available. Bind its listener once and initialize its text from the player's current score.
- On each dispatcher callback, update the visible score and call Print String with the new total.
- Give the listener a teardown owner. Ensure restart/recreation does not duplicate bindings.

Acceptance checks:

1. Fresh Play displays score zero.
2. Collect one inspected object: actor disappears and score increases by exactly its Score.
3. HUD changes through the dispatcher and Print String shows the updated total once.
4. Collect several more: the accumulated sum is correct, with no duplicated awards.
5. Restart Play: score initializes cleanly, one widget and one callback per pickup.
6. Affected Blueprints compile and no new attributable runtime warnings/errors appear.

Result: PASS. Fresh Play initializes zero; Coin, Gem and Potion each remove one object and update player/HUD totals correctly (82, 151, 205). Dispatcher binding, Print String and teardown are implemented. See `docs/progress.md` and evidence JSON.

## Part 2: interactive hinged door

- Build the door with a hinge at its edge, a Movable mesh and a Pawn-overlap interaction area.
- Map E with Enhanced Input and handle one Started action per press.
- Query overlapping door actors when interaction starts, avoiding a persistent nearby-door reference.
- Revalidate proximity inside the door's interaction event.
- Animate from captured closed rotation to closed rotation plus 90 degrees using a Blueprint Timeline and normalized playback time as the interpolation alpha. Expose angle and duration with rubric-compatible defaults.
- Set rotation from the Timeline alpha; do not repeatedly add rotation per frame. Closing is optional.
- Place and save the door in the default level.

Acceptance checks:

1. E outside the area does nothing.
2. Entering the area alone does not open the door.
3. E inside the area smoothly opens it exactly 90 degrees around the hinge.
4. Holding/repeatedly pressing E does not accumulate rotation or repeatedly restart the animation.
5. E after leaving the area does nothing.
6. Restart returns the door to its closed state.
7. Capture the actual door closed/open in Play, compile/save affected assets, and check attributable log errors.

Result: PASS through native Enhanced Input action injection. Distant input and approach alone leave the door closed; nearby input opens it to 90 degrees; repeated input does not accumulate rotation. Fresh Play starts closed. E mapping is verified in the saved input asset; no physical keyboard automation was used. Actual closed/open Play captures are retained.

## Part 3: full rubric verification and quality review

- Verify exactly 100 objects at initial spawn, with no loop or collision-rejection count error.
- Check all spawned actor X/Y values against the required world bounds and Z against manager Z.
- Check each assigned score is an integer from 10 to 100 and all three classes are selectable across fresh runs. Random choice need not produce all three in every possible run.
- Confirm non-player overlap does not award score; repeated component overlap cannot duplicate collection.
- Inspect mesh scale, collision usability and floor placement. Offset mesh components if necessary while preserving required actor Z.
- Confirm adding another collectible child class only requires a class-array entry, not spawn-graph rewrites.
- Review adjustable variables, meaningful names, shared base behavior, clear functions/events, unused Tick, dispatcher cleanup and input references.
- Run one final fresh Play through collection and door interaction using the saved final assets. Inspect logs and changed package paths.
- Record remaining limitations honestly. Do not mark complete until required checks pass.

Result: PASS. All 100 positions, integer scores and grounded mesh bottoms checked; all three types collected correctly; non-player overlap leaves items/score unchanged. Grounding runs once in the base class and moves mesh/collision children while preserving actor Z. Nine Blueprints compile without warnings; final packages saved, fixtures removed and logs checked. See `docs/progress.md` for measurements and evidence.

## Delivery record

- Changed assets/files: collectible base/children, score HUD, player/controller, input action/mapping, hinged-door Blueprint and placed external actor, editor-only MCP plugin configuration, local editor client and workflow/evidence documentation. Spawn logic and professor-corrected ranges retained.
- Evidence and check results: record in `docs/progress.md`; deliberate captures under `docs/evidence/` if retained.
- Commit/push: not performed; use only authorization for this Unreal repository.
- User walkthrough: fresh Play, collect objects and watch score/Print String; approach door and press E; repeat outside the area to verify gating.
- Publishing/submission: outside this task.
