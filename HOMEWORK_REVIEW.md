# Assignment 01: remaining work and implementation

Completion update: the gaps identified in this original audit have been implemented, tested and saved. Current results are in [progress](docs/progress.md), the [completed task](tasks/homework01.md) and [lecture alignment](docs/lecture-alignment.md). The assessment and implementation proposals below are historical.

Reviewed on 14 November 2026 against project commit `9c410ec`.

The assignment gives a submission date of **16 November 2026** and divides grading equally between functionality and code quality. This review treats the assignment as the rubric and the lectures as implementation guidance.

## Professor correction

The user clarified on 14 November 2026 that the professor changed the spawn ranges to X [-1000,1000] and Y [-2000,2000] without updating the PDF. These corrected ranges supersede the PDF values for implementation and final tests. The original placed manager already used the corrected ranges; preserve those overrides. References to the smaller ranges below describe the original PDF/static audit, not the final acceptance bounds.

## Original static assessment

The collectible system is substantially present. The main missing features are **a UI listener for score changes with Print String output** and **a nearby-player, E-controlled door that rotates 90 degrees using a Timeline**. Runtime verification is still required before declaring the existing collectible behavior complete.

| Requirement | Evidence in the saved project | Remaining work |
| --- | --- | --- |
| Three different object types with different Fab meshes | `BP_Collectible_Coin`, `BP_Collectible_Gem`, and `BP_Collectible_Potion` inherit from `BP_CollectibleBase`; each references a different mesh under `/Game/Fab` | Verify mesh scale, visibility, and usable collision in Play mode. The folder supports the intended provenance but does not independently prove acquisition history. |
| SpawnManager in the level | `BP_SpawnManager` and one corresponding external actor are present in `Lvl_ThirdPerson` | Check its placed instance has no unintended default overrides. Label it `SpawnManager` to match the wording of the assignment. |
| Spawn 100 random objects | Saved `SpawnCount = 100`, a ForLoop with FirstIndex default 1, random selection from `CollectibleClasses`, and Spawn Actor nodes are present | Verify the loop's LastIndex connection and confirm exactly 100 objects and that all three types can appear. |
| X in [-100,100], Y in [-200,200] | Saved defaults are exactly `MinX=-100`, `MaxX=100`, `MinY=-200`, `MaxY=200`, with Random Float in Range nodes | Verify final world coordinates use these ranges directly. |
| Z equals SpawnManager Z | Graph references Get Actor Location and its Z component | Confirm the final spawn-transform Z is connected to manager Z without an added offset. |
| Random integer score in [10,100] | Saved defaults `MinScore=10`, `MaxScore=100`; Random Integer in Range and exposed spawn Score are present | Verify each spawned instance receives the generated score. |
| Player overlap collects and destroys object | Base collectible references the player cast, `AddScore`, `Score`, and `K2_DestroyActor` | Play-test successful collection and confirm other actors do not collect. |
| Score stored in player | Character contains `TotalScore`, `AddScore`, addition, and `OnScoreChanged(NewTotalScore)` | Verify update order and that each item awards points once. |
| Notify UI using event dispatcher | Dispatcher and broadcast node exist in the character, but `OnScoreChanged` occurs in no other project asset and no delegate-binding node was found | Add and bind a score UI listener. |
| Print updated total using Print String | No `PrintString` reference found in project assets | Call Print String from the score listener for every collection. |
| Door opens 90 degrees while nearby and pressing E | No `IA_Interact` asset, relative-rotation call, or custom homework door found | Implement and place a hinged door with a proximity trigger and Enhanced Input. |
| Door animation uses Timeline | Template `BP_DoorFrame` has a Timeline but uses overlap events and relative-location changes | Create the required rotating door. A sliding/automatic template door does not satisfy the requested behavior. |
| Modularity, inheritance, functions, naming, scalability, adjustable parameters | Shared collectible base, three child classes, `SpawnRandomCollectible`, `AddScore`, class array and spawn-range variables already exist | Preserve this architecture. Expose settings and verify class-reference types, validation and graph comments. |

This is a static review of saved assets, including package name tables, serialized numeric properties and references. The presence of nodes does not prove their execution wiring or runtime behavior. No gameplay assets were changed for this review.

## Implementation order

### 1. Finish the score UI

Keep score ownership in `BP_ThirdPersonCharacter`.

```text
AddScore(Amount : Integer)
    Set TotalScore = TotalScore + Amount
    Call OnScoreChanged(TotalScore)
```

Create a Widget Blueprint `WBP_ScoreHUD` with a Text Block `ScoreText`. Give it a `PlayerRef` variable of type `BP_ThirdPersonCharacter` Object Reference, marked Expose on Spawn.

Create the widget once from the existing player controller when its pawn is available:

```text
Get Controlled Pawn
    Cast to BP_ThirdPersonCharacter
    Create Widget WBP_ScoreHUD (Owning Player = Self, PlayerRef = cast result)
    Store ScoreHUD reference
    Add to Viewport
```

Preserve the controller's existing input and touch-interface setup. Initialize after possession if the pawn is unavailable during BeginPlay. Bind before the player can collect items.

Inside the widget, create `InitializeScoreDisplay` and a custom event `HandleScoreChanged(NewTotalScore : Integer)`:

```text
InitializeScoreDisplay
    IsValid(PlayerRef)
    Bind Event to PlayerRef.OnScoreChanged -> HandleScoreChanged
    Set ScoreText from PlayerRef.TotalScore

HandleScoreChanged(NewTotalScore)
    Format Text "Score: {Score}" -> SetText(ScoreText)
    Convert NewTotalScore to String -> Print String
```

Call `InitializeScoreDisplay` once after creating the widget. Avoid repeated binding from Tick or repeated Construct calls. On teardown, unbind this listener if the player can outlive the widget. Initialize text directly so displaying the starting score does not simulate a collection event.

The essential grading point is that the UI receives each change through the dispatcher. A dispatcher with no bound UI event is incomplete. A polling text binding also does not demonstrate the requested event-dispatcher communication.

### 2. Add the required door

Create `BP_InteractiveDoor` under `/Game/Hw1/Blueprints` with this component hierarchy:

```text
DefaultSceneRoot
    DoorFrame (Static Mesh, optional)
    HingePivot (Scene Component, positioned at one edge of the door)
        DoorMesh (Static Mesh, Movable)
    InteractionArea (Box Collision, Query Only, overlaps Pawn)
```

Offset `DoorMesh` under `HingePivot` so the edge stays fixed when the pivot rotates. A centered pivot makes the door spin around its middle.

Add configurable variables:

| Variable | Type | Default |
| --- | --- | --- |
| OpenAngle | Float | 90 |
| OpenDuration | Float | 1.0 seconds |
| ClosedRotation | Rotator | Captured at BeginPlay |
| NearbyPlayer | BP_ThirdPersonCharacter Object Reference | None |
| bIsOpen | Boolean | false |

Create `IA_Interact` as a Digital/Boolean Input Action. Map **E** in the existing `IMC_Default`. Handle the action in the character using `Started` so holding E does not repeatedly restart the animation.

For the minimum assignment, track the one door whose area contains the player:

```text
InteractionArea BeginOverlap
    Cast OtherActor to BP_ThirdPersonCharacter
    Set NearbyPlayer
    Set character.NearbyDoor = Self

InteractionArea EndOverlap
    If OtherActor == NearbyPlayer
        Clear character.NearbyDoor only if it still equals Self
        Clear NearbyPlayer

Character IA_Interact Started
    IsValid(NearbyDoor)
    NearbyDoor.TryOpen(Self)

Door TryOpen(RequestingPlayer)
    RequestingPlayer == NearbyPlayer
    InteractionArea.IsOverlappingActor(RequestingPlayer)
    If not already open, Play door Timeline
```

If door interaction areas can overlap, keep an array of nearby doors and select the nearest valid one when E is pressed. For this homework, placing a single door avoids that extra selection logic. An interaction interface can replace the direct door reference if you want to extend interaction to other actor types later; it is optional.

Add a Timeline named `TL_OpenDoor`, with a Float track `Alpha`, keys `(0,0)` and `(1,1)`, and length 1 second. At BeginPlay, save `HingePivot` relative rotation as `ClosedRotation`; set the Timeline play rate to `1 / Max(OpenDuration, 0.01)`.

```text
Timeline Update(Alpha)
    SetRelativeRotation on HingePivot:
        ClosedRotation + MakeRotator(Yaw = Alpha * OpenAngle)

Timeline Finished
    Set bIsOpen = true
```

Use absolute interpolation from the saved closed rotation. Applying an additional rotation every Update accumulates error and can turn farther than 90 degrees. Closing the door is optional; the assignment only requires opening. If added, use Timeline Reverse with appropriate state handling.

Place the door in the current level where the player can approach it. Make its proximity box large enough to interact before the blocking door mesh stops the player. Confirm E does nothing outside that area.

### 3. Verify the existing collectible system

Keep one base class for collection logic and use the child classes primarily for mesh/scale configuration.

Recommended base-collectible overlap flow:

```text
ActorBeginOverlap(OtherActor)
    Cast OtherActor to BP_ThirdPersonCharacter
    Guard against repeated collection
    Disable collectible overlap/collision
    Player.AddScore(Score)
    Destroy Actor(Self)
```

A `bCollected` guard or DoOnce is a small defensive improvement when the player has several overlapping components. Destroy Actor must execute after awarding the score, and only after identifying the player.

Check `BP_SpawnManager`:

```text
BeginPlay
    Validate SpawnCount > 0 and CollectibleClasses is not empty
    ForLoop FirstIndex = 1, LastIndex = SpawnCount
        SpawnRandomCollectible()

SpawnRandomCollectible
    Choose random entry in CollectibleClasses
    Validate selected class
    X = RandomFloatInRange(MinX, MaxX)
    Y = RandomFloatInRange(MinY, MaxY)
    Z = GetActorLocation(Self).Z
    Score = RandomIntegerInRange(MinScore, MaxScore)
    Spawn Actor from selected class at (X,Y,Z), passing Score
```

ForLoop includes both endpoints. A loop from 0 through SpawnCount produces 101 iterations for SpawnCount=100. An alternative correct loop uses 0 through SpawnCount-1.

Use a `BP_CollectibleBase` **Class Reference array** for `CollectibleClasses` and initialize it with Coin, Gem and Potion. This lets you add another child class without editing the spawn graph. Expose the count, ranges, score limits and class array as instance-editable variables.

The assignment states X and Y ranges directly and only ties Z to the manager position. The strict implementation therefore uses absolute world X/Y from those ranges, without adding manager X/Y. Keep manager X/Y at zero unless the instructor has clarified a different interpretation. Preserve Z exactly. Correct a mesh's visual height with its component offset instead of changing spawn Z.

The specified area is small in Unreal units. Shrink meshes and collision appropriately rather than increasing the required ranges. `Always Spawn` is already referenced by the saved spawn graph; confirm the collision-handling setting so collision rejection does not silently reduce the object count.

## Acceptance checks

- Compile the changed Blueprints and save all modified assets.
- Start a fresh Play session with the player outside the spawn area so immediate collection does not hide the starting count.
- Observe exactly 100 spawned collectible actors before collecting any.
- Check every object's X/Y bounds and that its actor Z equals the manager actor Z.
- Inspect several scores and confirm all are integers from 10 through 100.
- Confirm each of the three child classes can be selected across repeated sessions; random selection does not mathematically guarantee all types in every run.
- Collect one known-score object: it disappears, TotalScore increases by that exact value, the widget updates, and Print String shows the new total once.
- Repeat with several objects and check the accumulated sum.
- Make a non-player actor overlap a collectible and confirm it awards no score.
- Press E far from the door: no movement.
- Enter the door area without pressing E: no movement.
- Press E nearby: the door rotates smoothly by exactly 90 degrees around its hinge.
- Hold E or press it repeatedly: no accumulated rotation or animation restart loop.
- Exit the area: E no longer controls the door.
- Restart Play: score and door state initialize correctly, with no duplicate UI listeners.
- Check the Output Log for Blueprint runtime errors, especially Accessed None.

## Engine setup

`GameEngineHW1.uproject` has `EngineAssociation: "5.8"`. The introduction lecture explicitly names **5.8.3**. Your Epic Games Launcher offers **5.8.4**, the subsequent 5.8 hotfix, and you approved installing it after the patch-version difference was explained.

Selected installation path: `E:\Epic Games\UE_5.8`.

Selected components include the editor core, templates/feature packs and engine source. Optional platform packages, MetaHuman core data and editor debug symbols were not selected. The Launcher reports about 11.647 GB download and 29.506 GB required storage.

Installation completion and project launch must be verified separately. Do not change the project's association to an older engine. No C++ module is declared by this project, so a full Visual Studio C++ setup is not needed for the current Blueprint work.

## Course references

- [Assignment 01](<C:/Users/Mjdis/Downloads/Assignment #01.docx.pdf>), pages 1-2: required functionality, grading, date.
- [Unreal Introduction](<C:/Users/Mjdis/Downloads/Unreal Introduction.pptx>), slide 11: engine version 5.8.3.
- [Blueprints Introduction](<C:/Users/Mjdis/Downloads/Blueprints Introduction.pptx>), slides 5-8: Blueprint structure, inheritance and class roles.
- [Interactions in Blueprints](<C:/Users/Mjdis/Downloads/Interactions in Blueprints.pptx>), slides 3 and 14: functions, trigger boxes, casting and event dispatchers.
- [Character, Physics & Input](<C:/Users/Mjdis/Downloads/Character, Physics & Input.pptx>), slides 5-13, 20-28: Enhanced Input, Expose on Spawn and collisions.
- [AI for NPCs & Dynamic Animations](<C:/Users/Mjdis/Downloads/AI for NPCs & Dynamic Animations.pptx>), slides 20-24: Timeline animation, including doors.
- [Data Structure, Blueprint Animations Intro](<C:/Users/Mjdis/Downloads/Data Structure, Blueprint Animations Intro.pptx>), slides 5-13 and 18-19: arrays and object/class references.
- [Epic installation guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/install-unreal-engine).
- [Epic 5.8.4 hotfix announcement](https://forums.unrealengine.com/t/5-8-4-hotfix-released/2842775).

NPC pathfinding, weapons, shooting, additional character animation systems, and physics impulses appear in the lectures but are not requirements of Assignment 01.
