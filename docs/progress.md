# Progress and handoff

## Current state

- Date: 14 November 2026.
- Active task: `tasks/homework01.md`; baseline `main` at `9c410ec`.
- Unreal 5.8.4 is installed and the tracked project `E:\Unreal Engine HW\HW1\GameEngineHW1.uproject` has been opened and tested. The separate `HW1 5.8` conversion copy was not edited.
- Connected to Epic's native local MCP endpoint at `http://127.0.0.1:8000/mcp`. Editor-only MCP, Blueprint and UMG toolsets are enabled. `tools/unreal_mcp.py` is the local client.
- Per the user's preference, implementation and tests after their instruction use MCP and files on disk, with no mouse/keyboard automation.
- All gameplay work is reviewed against the lectures in `docs/lecture-alignment.md`.
- Score UI is complete. Coin, Gem and Potion pickups each removed one object and produced matching player/HUD totals of 82, 151 and 205.
- Door is implemented and passed far-input, approach-without-input, nearby interaction and repeated input checks. Final relative yaw is 90.00000000000001 degrees.
- Grounding is implemented in the shared base. All 100 actor positions and integer scores passed; all mesh bottoms were measured 0.999-1.318 cm above independently traced surfaces. Actor Z remains manager Z.
- Final regression passed; all nine relevant Blueprints compiled with warnings treated as errors. Temporary test assets were removed, all dirty packages saved and Play stopped. No commit, push or homework submission has been performed.

## Existing implementation evidence

Static audit at `9c410ec`, recorded in `HOMEWORK_REVIEW.md`:

- VERIFIED: three child collectible assets and a shared base are saved, referencing different meshes under `/Game/Fab`.
- VERIFIED: manager defaults are 100 objects, X [-100,100], Y [-200,200], score [10,100]. A manager actor is saved in the default map.
- VERIFIED: the character asset contains `TotalScore`, `AddScore` and `OnScoreChanged` with a broadcast node.
- VERIFIED: no score dispatcher listener or Print String reference was found across the saved project assets in the audit.
- VERIFIED: the template door references overlap and sliding-location logic. The required custom rotating door and `IA_Interact` were absent in the audit.
- UNKNOWN: correct execution wiring, actual spawn count/coordinates, collision usability, score accumulation and runtime errors. These need Play-mode verification.

## Task status

| Part | Implementation | Required runtime checks |
| --- | --- | --- |
| 0. Installation and baseline | COMPLETE | PASS |
| 1. Score HUD and Print String | COMPLETE | PASS |
| 2. E-controlled Timeline door | COMPLETE | PASS through Enhanced Input injection |
| 3. Collectible verification and final regression | COMPLETE | PASS |

## Protocol adaptation record

Reviewed the Roblox `.claude` permissions and root workflow instructions, plus targeted task/evidence examples. Added this project's canonical `AGENTS.md`, the `CLAUDE.md` pointer, workflow mapping/template, this progress file and the active homework task. Preserved the task/part/test/report approach and adapted source-of-truth, input, lifecycle and binary-asset handling for Unreal.

At the protocol-adaptation stage, only documentation was changed. Gameplay implementation and engine tests were completed afterward as recorded above. Roblox files, permissions, Git history and remote services were not changed.

Documentation validation: PASS for local Markdown link targets, code-fence pairing and Git whitespace checks. The README links to the working rules, workflow, progress, active task and audit. No Play-mode check was run for this documentation change.

## Future evidence entries

Append one compact entry per completed part or material failure:

```text
Date / part / baseline revision:
Changed assets and behavior:
Environment: engine, map, relevant settings
Checks: result, expected versus observed, evidence paths
Existing issues versus new failures:
Commit/push status, if applicable:
What the user should see:
Remaining work / next action:
```

## Professor correction, 14 November 2026

The user confirmed the professor changed spawn X to [-1000,1000] and Y to [-2000,2000] without updating the PDF. The original manager instance already had those overrides. The temporary change to the PDF bounds was reversed; final acceptance uses the professor-corrected ranges.

## Final verification, 14 November 2026

Unreal 5.8.4, `Lvl_ThirdPerson`, saved tracked project:

- PASS: 100 collectibles; all positions within corrected X/Y bounds, actor Z equal to manager Z, integer scores 10-100. All visible mesh bottoms measured 0.999-1.318 cm above traced surfaces; clearance defaults to 1 cm.
- PASS: each of Coin, Gem and Potion collected once with correct accumulated score and matching HUD. A fresh Play initializes score to zero. Non-player overlap leaves 100 items and zero score.
- PASS: door remains closed for distant input and approach alone; nearby input opens to 90 degrees; repeated input does not accumulate rotation. Tests inject the mapped Enhanced Input action, without operating the physical E key.
- PASS: nine Blueprints compile without warnings; final runtime log scan found no Blueprint runtime errors or Accessed None messages. All packages saved, probes removed, editor left in Edit mode.
- Evidence: `docs/evidence/grounding-and-score-checks.json`, `pickup-regression.json`, `nonplayer-check.json`, `door-checks.json`, `final-save.json`.
- Actual Play captures: `docs/evidence/final-play.png` and `open-door-play.png`, both 1280 x 730. `grounded-collectibles-and-hud.png` is an Edit viewport capture, not a HUD verification image.
- Lecture mapping: `docs/lecture-alignment.md`. Initial fixture limitations and corrected measurements remain documented in the evidence JSON.

Remaining: optional user walkthrough with physical controls and submission preparation according to the course's delivery instructions. No known required gameplay implementation remains.
