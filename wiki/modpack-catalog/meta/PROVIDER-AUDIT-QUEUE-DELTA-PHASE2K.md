# Provider Audit Queue — Phase 2K delta

Date: `2026-09-07`

Closure update: `2026-09-17`

This is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It prevails for `mobstein` until the next integral regeneration of the 103-provider queue. Existing earlier deltas remain authoritative for their own named rows.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `mobstein` | `mobstein-5.4.4-neoforge-1.21.1.jar` / runtime `5.4.4` | `✅ CATALOG CLOSED / EXACT INSTALLED ARTIFACT + EXACT PUBLIC RELEASE FILE 8040734 / PUBLISHER FULL GAMEPLAY GUIDE AUDITED / EXACT HASH-MATCHED RESOURCE-ONLY CLEAN-ROOM AUDIT / ZERO INDEPENDENT SEMANTIC MAGIC ACTIONS (+0) / 5.4.4 SABLE COMPAT DECLARED BUT SEMANTICS UNVERIFIED / ARR / NO SOURCE OR BYTECODE DECOMPILATION / SUPPORTED API+RUNTIME QA PENDING SEPARATELY / FAIL-CLOSED` |

## Evidence

Installed artifact from the current physical modlist:

- JAR `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id `mobstein`;
- runtime `5.4.4`;
- SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- package fingerprint `3386302902`.

Exact publisher release:

- CurseForge project `1193873`;
- File ID `8040734`;
- NeoForge/Minecraft 1.21.1;
- released `2026-05-04`;
- exact filename matches installed artifact;
- project license All Rights Reserved;
- exact 5.4.4 changelog declares compatibility with Sable Mod.

## Public semantic coverage

The current publisher guide is sufficient to establish the following provider-owned surfaces without decompilation:

- Clinical Stretch body resurrection, ordinary night gate and approximately 15-second public timing description;
- Lightningbolt Syringe daytime resurrection path;
- ten named resurrected creature families with provider tame/utility/bodyguard roles;
- anatomical parts and Organ Extractor;
- Full Body Support;
- Surgery Stretch;
- four internal surgery modifiers: Attack, Health, Speed, Template;
- six documented surgery creature families;
- Subject Assembly Machine and player-head creation workflow;
- Igor, Igor Table/Station, Suspicious Syringe and failed experiments;
- seven named failed-experiment families in the current guide;
- Reviver, Mobstenio Blood, Lightningbolt and Suspicious Syringe roles;
- Frankenstein Castle, Witherstein Ruins and Old Ruins;
- Dr. Mobstenio resurrection/taming progression;
- three-stage Witherstein awakening/boss path.

## Important QA/documentation deltas

- Exact 5.4.4 says only `compatible with Sable Mod`; the compatibility mechanism is not public, so it remains fail-closed.
- Current guide lists **Strawberries** for Experiment 091 taming, while an older official 5.2.0 changelog listed **Sweet Berries**. Exact 5.4.4 runtime decides; no silent reconciliation.
- Current guide describes Frankenstein's `Blacksmithstrength` presentation as granting speed; the catalog preserves publisher behavior rather than inferring Strength from the name/icon.
- Public qualitative timing/stat descriptions are not promoted to internal constants or API contracts.

## 2026-09-17 semantic closure

Temporary non-merge PR #316 audited exact HEAD `138441e4cd70896378d30287b3283ec07aaed43b`. Dedicated workflow **Mobstein 5.4.4 Clean-room Resource Audit** run `35285950286` completed successfully after requiring the canonical SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`.

The permitted resource-only inventory exposed no independent Mobstein spell/ritual/rite/ability/action resource family. The only action-like keybind identities surfaced are controls for resurrected creatures/mounts already represented by the publisher-facing entity catalog. Under the global semantic metric, Mobstein therefore contributes **+0** independent semantic magic objects and its catalog scope is closed.

This does not establish supported runtime hooks, API contracts, Sable integration semantics or Black Arcana adapter safety.

## Authority consequence

Mobstein owns corporeal reconstruction, bodies/organs, its resurrection machines/syringes, reconstructed creature lifecycle, surgery parameters, Igor experiments and its structure/boss progression.

It does **not** become authority for:

- Black Arcana Souls & Death state;
- Goety Soul Energy;
- Malum spirits;
- Eidolon soul/research state;
- Black Arcana Corruption/Strain;
- RPG Skill Tree mastery/attributes.

Any future bridge must preserve provider costs and causal identity and must fail closed when no supported hook exists.

## Next provider checkpoint

The historical Apprentice's Codex instruction in the original Phase 2K delta is superseded by later canonical work. Current remaining conditional-provider routing is maintained in `CONDITIONAL-PROVIDER-CLOSURE.md`; do not select the next target from this older Phase 2K checkpoint.