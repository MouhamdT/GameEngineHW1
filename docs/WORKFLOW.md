# Feature development protocol

Adapted on 14 November 2026 at the user's request. The source was the Roblox project's `.claude/settings.json`, root `AGENTS.md` and `CLAUDE.md`, with examples from its task records, progress log and verification reports. No source project files were modified.

## What carries over

| Roblox practice | Unreal adaptation |
| --- | --- |
| Read task file and progress before starting | Read `tasks/<feature>.md`, `docs/progress.md`, current status and recent history. Resume unfinished work. |
| Complete features in observable parts | Score UI, door interaction and final rubric verification are separate parts with their own checks. |
| Review performance/security, UI, visuals and gameplay | Review correctness, Blueprint architecture, presentation, lifecycle/performance and rubric compliance. No multiplayer/security infrastructure unless the scope needs it. |
| Gameplay/config has one owner | Character owns score; collectible base owns pickup; manager owns spawn configuration; door owns animation. |
| Repo scripts are authoritative; verify Rojo sync | Saved Unreal assets are authoritative. Compile and save the real graphs, then test a fresh Play session. No Rojo or Luau byte-count check. |
| Only one Studio Play at a time | Coordinate one writer per binary asset and do not interrupt another user's editor session. A Roblox lock file is not an Unreal editor lock. |
| Disconnect event connections and clean player state | Own and unbind dispatcher listeners, clear actor references and timers, and prevent duplicate pickup/input effects. |
| No unnecessary per-frame work | Use overlap events, Enhanced Input and Timelines. Keep idle collectibles and score UI free of avoidable Tick logic. |
| Evidence-first PASS/FAIL reports | Separate static evidence, compile success, actual gameplay tests and visual inspection. Store exact observations. |
| Performance compared with a baseline | If performance is in scope, measure the same map/view/settings and workload. Do not reuse Roblox millisecond budgets as Unreal targets. |
| Small independent commits and explicit staging | When authorized here, commit a tested feature part and its intended assets by explicit paths. Record commit IDs only after they exist. |
| Report what the user should see | Give a short reproducible Play-mode walkthrough, not only a list of edited packages. |

## What is project-specific

The Roblox task's branch names, protected commits, admin-file exceptions, remote validation, save/purchase rules, lore names, graphics palette, plugin IDs, screenshot scale factors and automatic GitHub delivery are specific to that game. They are not imported into this project. The `.claude` JSON describes Claude tool permissions, not a portable feature implementation protocol.

For this assignment, keep the lecture's Blueprint style and the rubric's values. Use Unreal assets and Play in Editor. The approved engine is 5.8.4 because the Launcher offered that 5.8 hotfix; the lecture named 5.8.3 and the project associates with 5.8.

## Feature loop

1. **Inspect:** Read the request and task, current progress, saved implementation and relevant lecture/rubric evidence. Identify what already works and what is still unknown.
2. **Specify:** State the player-visible result, scope, touched assets, ownership, adjustable values and acceptance checks. Flag conflicts with the rubric before changing it.
3. **Baseline:** Record current relevant errors and behavior. If the editor is unavailable, do useful independent work and leave runtime checks unverified.
4. **Implement:** Make one cohesive part using shared classes and existing input/state paths. Keep debug probes temporary and editor-only where possible.
5. **Verify:** Compile, save, run the named gameplay checks, inspect Output Log and capture the actual visual result when needed. Fix attributable failures and retest the affected checks.
6. **Record:** Update the task and `docs/progress.md` with evidence, changed paths, unfinished checks and the next action. Review the diff/changed packages. Commit or push only if authorized for this repository.
7. **Deliver:** State the observed behavior and test results, any limitation and what the user can try. Resume the next authorized part without another routine permission request.

## Installation gate

The editor-dependent parts are ready to begin only after all of these are true:

- The Launcher reports installation complete rather than queued, downloading, installing or verifying.
- `E:\Epic Games\UE_5.8\Engine\Build\Build.version` identifies the intended 5.8.4 build and `Engine\Binaries\Win64\UnrealEditor.exe` exists.
- `GameEngineHW1.uproject` opens in that editor and the default map loads. First-launch shader compilation may take longer than a normal test.
- Record any blocking dialog, missing plugin, crash or baseline Blueprint error. Do not silently migrate to another engine or change renderer settings to hide it.

Finding an executable on disk alone is not proof that installation or project startup succeeded. The user's previous Escape stopped computer use; preparing these files does not claim that editor interaction has resumed or that a background watcher has been scheduled.

## Reusable task template

```markdown
# Feature: <name>

Status: READY / IN PROGRESS / WAITING-ENGINE / COMPLETE
Request: <what the user authorized>
Baseline: <revision and relevant existing behavior>

## Expected result
<What the player sees and does.>

## Scope and ownership
- Assets to edit/create:
- State owner and communication:
- Adjustable parameters and defaults:
- Out of scope:

## Parts
### Part 1: <observable result>
- Implementation:
- Acceptance checks:
- Result: NOT RUN
- Evidence:

## Delivery
- Changed assets/files:
- Checks: PASS / FAIL / NOT RUN / BLOCKED, with observations
- Commit/push: actual ID/status or not performed
- User walkthrough:
- Remaining work and next action:
```

## Definition of done

A gameplay part is complete when the actual saved assets implement its behavior, affected Blueprints compile, named Play-mode checks pass, attributable runtime errors are resolved, relevant visual evidence has been inspected, and progress is recorded. Documentation-only changes need document/link consistency checks, not a fabricated editor test.

When a required check cannot run, say which one and why. A useful implementation with unverified runtime behavior is still unfinished verification. Do not invent performance measurements, screenshots, commits, or tests.

## Source references

- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\.claude\settings.json`
- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\AGENTS.md`
- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\CLAUDE.md`
- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\docs\loop\progress.md` (opening baseline and how-to sections)
- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\tasks\aaa_magic_feel_overhaul.md` (scoped changes, evidence, explicit remaining verification)
- `C:\Users\Mjdis\OneDrive\Documents\ROBLOXPROJECT\docs\bugs\tree-size-normalization.md` and its results JSON (measured checks and user walkthrough)
