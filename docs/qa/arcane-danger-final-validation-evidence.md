# Arcane Danger — Stage 09 Final Validation Evidence

> **Status:** PENDING / DEFERRED TO STAGE 09 under D035. This file is an executable evidence template, not proof that any physical/manual row passed.

## Closeout baseline

- Stage 05A engineering closeout base: `main@dc98f0fc07a4017309dfeb998572b7d2cf3ef320`.
- Physical-modlist authority checked from sibling `neoforge-rpg-skilltree@6830865ec4d3fc4a778aa99293a8e232d2097981`.
- Minecraft: `1.21.1`.
- NeoForge target: `21.1.248`.
- Java: `21`.
- Curios physical artifact: `curios-neoforge-9.5.1+1.21.1.jar`, mod id `curios`, version `9.5.1+1.21.1`.
- No identifiable top-level RPG Skill Tree artifact is present in the current physical modlist. Stage 09 must recheck the exact release-candidate modlist before classifying the loaded-provider row.

## Stage 09 execution header

Fill these fields only when the physical campaign is actually executed:

- Tested Black Arcana SHA: **PENDING**
- Exact physical modlist snapshot / source SHA: **PENDING**
- Client/server topology: **PENDING**
- Minecraft / NeoForge / Java actually executed: **PENDING**
- Curios artifact/version/mod id actually loaded: **PENDING**
- RPG Skill Tree artifact/version/mod id actually loaded, if any: **PENDING**
- Fixture/config variants: **PENDING**
- Evidence date/operator: **PENDING**

## Result vocabulary

- `PASS` — directly observed on the stated exact release candidate/provider topology.
- `FAIL` — observed behavior contradicts the frozen contract.
- `BLOCKED` — the scenario cannot be legitimately exercised in the exact physical/provider topology.
- `PENDING / DEFERRED TO STAGE 09` — mandatory release evidence not yet executed.
- `NOT APPLICABLE` — only when the scenario genuinely does not apply to the exact release topology.

Automation may support setup but never converts a physical/manual row to PASS.

## Transferred Arcane Danger rows

| ID | Origin | Stage 09 scenario | Current topology note | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| 05A-P01 | 05A.08 / 05A.11 | Dangerous-profile datapack reload, static preflight convergence and stale in-flight forecast rejection | Use the exact candidate and removable QA fixture only | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P02 | 05A.06 / 05A.02 | Baseline/equipment Arcane Resistance contribution and frozen root-cast snapshot across post-activation equipment change | Core Black Arcana provider applicable | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P03 | 05A.07 | Real Curios resistance contribution, post-activation swap safety and client forecast convergence | Curios is present; if no legitimate registered contributing Curio exists, classify the concrete row BLOCKED | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P04 | 05A.10 | Real RPG Skill Tree Arcane/Corruption Resistance contribution through the Black Arcana boundary | Current physical modlist has no top-level RPG Skill Tree artifact; recheck at execution and classify BLOCKED if still absent | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P05 | 05A.03 / 05A.04 | Corruption and Arcane Strain persistence across reconnect, death/respawn and server restart plus normal Strain recovery | Use production-supported acquisition; no debug cleanse/bypass | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P06 | 05A.05 / 05A.12 | Representative zero-resistance 1:1 Backlash, reduced Backlash with legitimate resistance, delayed/root attribution and terminal non-recursion | Sample the deterministic matrix; do not recreate all automated rows manually | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P07 | 05A.11 | Real-client forecast thresholds, predictable gate categories, stale reconnect/reload behavior, tooltip/HUD readability and accessibility | Shared with Stage 05 real-client runbook/matrix | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P08 | 05A.07 / 05A.09 / 05A.10 | Optional-provider presence/absence/incompatibility ledger and dedicated-server isolation | Distinguish real-provider evidence from test doubles; optional absence must fail closed | PENDING / DEFERRED TO STAGE 09 | PENDING |
| 05A-P09 | 05A.05 / 05A.12 | Representative real-modpack interaction with ordinary offensive lifesteal/on-hit/mastery/proc surfaces to confirm Backlash receives no Black Arcana offensive credit | Third-party generic damage reactions are integration findings, not authority to invent suppression hooks | PENDING / DEFERRED TO STAGE 09 | PENDING |

## Failure loop

For every `FAIL`:

1. reproduce on the same exact SHA and topology;
2. identify the smallest frozen contract violated;
3. add a deterministic regression test where representable;
4. observe RED before the fix;
5. implement the minimum authority-preserving correction;
6. run the focused test GREEN and the applicable broader gates;
7. repeat only the affected physical row on the new exact candidate;
8. update evidence only for rows actually rerun.

If a fix would change hazard identity, resistance-channel separation, D030 coefficient semantics, cast transaction ordering, provider authority or Backlash exclusions, stop and register an architectural blocker/decision before implementation.
