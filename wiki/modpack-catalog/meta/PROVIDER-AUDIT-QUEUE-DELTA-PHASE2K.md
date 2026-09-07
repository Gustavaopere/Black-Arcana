# Provider Audit Queue — Phase 2K delta

Date: `2026-09-07`

This is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It prevails for `mobstein` until the next integral regeneration of the 103-provider queue. Existing earlier deltas remain authoritative for their own named rows.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `mobstein` | `mobstein-5.4.4-neoforge-1.21.1.jar` / runtime `5.4.4` | `EXACT INSTALLED ARTIFACT + EXACT PUBLIC RELEASE FILE 8040734 / PUBLISHER FULL GAMEPLAY GUIDE AUDITED / CORPOREAL RESURRECTION + RESURRECTED MOBS + ANATOMY/ORGAN EXTRACTION + SURGERY PERKS + SUBJECT ASSEMBLY + IGOR EXPERIMENTS + SYRINGES + STRUCTURES + MOBSTENIO + WITHERSTEIN CATALOGED / 5.4.4 SABLE COMPAT DECLARED BUT SEMANTICS UNVERIFIED / ARR / NO SOURCE OR BYTECODE DECOMPILATION / REGISTRY IDS+SUPPORTED API+RUNTIME QA PENDING / FAIL-CLOSED` |

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

After Mobstein, the next high-value standalone provider from the still-open exact-inventory group is **Apprentice's Codex `0.9.7.1`**.

It should be revalidated first against the current modlist and exact public release/source evidence. The old queue row `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` is not enough to infer any spell count, registry ID, cost, cooldown or acquisition rule.