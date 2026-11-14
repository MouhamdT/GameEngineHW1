# Unreal homework project workflow

These are this repository's working rules. They adapt the user's Roblox feature workflow to Unreal Engine and Assignment 01. The source Roblox repository is reference material; its task-specific exceptions and permissions do not apply here.

## Start and resume

1. Read `docs/progress.md`, the active task file, and `git status --short` / `git log --oneline -20`.
2. Current task: `tasks/homework01.md`. Detailed implementation reference: `HOMEWORK_REVIEW.md`.
3. Resume at the first unfinished part. Preserve the user's existing assets and unrelated changes. Never rebuild completed systems just to impose a different architecture.
4. Use the assignment as the acceptance rubric and the supplied lectures as implementation guidance. All gameplay work, including completed changes, must be reviewed against the supplied lectures; record the mapping in `docs/lecture-alignment.md`. Do not add NPCs, combat, multiplayer or other lecture demonstrations without a separate request.
5. Progress within the user's authorized scope without asking for approval again. A new substantive scope decision or external action needs its own basis in the user's instructions.

## Feature protocol

- Write the expected player behavior, affected assets, owner of each state, configurable parameters and acceptance checks in the task file before implementation.
- Work in small parts, each producing an observable result. Keep the implementation, its evidence and its progress entry together.
- Review each part for correctness, Blueprint structure, presentation, performance/lifecycle and assignment compliance. These are review perspectives, not an instruction to spawn agents.
- Label findings `VERIFIED`, `LIKELY` or `UNKNOWN`. Record check results as `PASS`, `FAIL`, `NOT RUN` or `BLOCKED`, with evidence or the exact blocking reason. Never report an inferred behavior as a successful playtest.
- Fix failures introduced by the current part before marking it complete. Record unrelated baseline issues separately.

## Unreal source of truth

- The saved `.uproject`, `Config/`, `.uasset` and `.umap` files are the project source of truth. Unlike the Roblox Rojo workflow, Blueprint and level changes normally happen in Unreal Editor and must be saved to disk.
- Use the approved Unreal 5.8.4 installation at `E:\Epic Games\UE_5.8`; project association remains `5.8`. Confirm installation and project launch before starting editor-dependent work.
- Do not hex-edit binary assets or substitute text descriptions for real Blueprint graphs. Static package inspection can support an audit but cannot prove runtime behavior.
- Prefer existing purpose-built editor tools when available, otherwise use supported editor automation or the UI. Verify uncertain APIs against official Epic documentation.
- Stop Play/Simulate before editing or saving gameplay assets. Do not interrupt a Play session owned by the user or another chat; coordinate first.
- One writer per Blueprint or map, including World Partition external actor packages. Coordinate shared assets explicitly if concurrent work is requested. Do not attempt text merges of binary packages.
- Keep gameplay in modular Blueprint classes and functions, not a large Level Blueprint. Preserve the existing collectible base and child inheritance.

## Ownership and lifecycle

- Player character owns `TotalScore`; `AddScore` is the single score-update path. The UI observes `OnScoreChanged` and never owns a second total.
- `BP_CollectibleBase` owns pickup behavior; child classes configure their meshes. `BP_SpawnManager` owns spawning and its configurable class array and bounds.
- Player input uses Enhanced Input. A door owns its trigger, hinge, Timeline and open state; the player requests interaction.
- Bind each dispatcher listener once and give it a clear owner and teardown. Clear stale interaction references; guard repeated pickups and repeated door input.
- Prefer events, Timelines and bounded timers to unnecessary Tick polling. Disable unused Tick where appropriate. Do not add object pools, global managers or networking to this small assignment without a demonstrated need.
- Keep required values adjustable through clearly named Blueprint variables. Preserve the professor-corrected defaults (user clarification, 14 November 2026, supersedes the PDF ranges): 100 objects; X [-1000,1000]; Y [-2000,2000]; Z = manager Z; integer score [10,100]; E interaction; door opening 90 degrees.
- Do not lower graphics quality or alter collision rules merely to make a check pass. Identify the cause before proposing a tradeoff.

## Verification and delivery

- Compile affected Blueprints, save the assets, then test the saved implementation in a fresh Play in Editor session. A compiled graph alone is not a gameplay PASS.
- Follow the active task's acceptance checks. Record map, engine version, settings relevant to the result, observations and evidence paths in `docs/progress.md`.
- Check Output Log errors/warnings attributable to the change. Test user input, edge cases, repeated interaction and reset behavior as relevant.
- Capture the actual UI/door result when visual evidence matters; identify Edit versus Play and the real capture dimensions. Missing evidence stays `NOT RUN` or `BLOCKED`.
- A normal smoke Play should fit in two minutes after loading/shader compilation. Do not apply that limit to engine installation or first-launch shader compilation. Retry an unchanged environment failure at most once, then record it and continue independent work; implementation fixes justify another focused check.
- The user's later test is separate and never replaces agent verification. Do not mark a task complete while required checks remain unverified.
- Before delivery, inspect changed paths and update the task/progress records. Report what changed, what passed, what remains, and concrete steps the user can try.

## Git and project boundaries

- Work on the current branch unless instructed otherwise. Preserve unrelated work; do not reset, restore, clean, stash, rewrite history or perform branch operations as routine cleanup.
- When committing is authorized, use explicit file paths and one focused, tested part per commit. Include the relevant saved external actor packages. Never stage the whole workspace indiscriminately.
- Never commit generated caches, `Saved/`, `Intermediate/`, engine installs, downloaded course files, temporary probes or unrelated Fab assets. Small intentional review evidence may live under `docs/evidence/`.
- The Roblox project's standing commit/push authorization does not transfer to this repository. Commit/push only within authorization for this Unreal project. Do not automatically pull into a dirty workspace, publish, upload, package for distribution or submit the homework.
- Do not copy `.claude` permission settings or tool IDs from another project and present them as effective permissions here.

See `docs/WORKFLOW.md` for the source-to-Unreal mapping and reusable feature template.
