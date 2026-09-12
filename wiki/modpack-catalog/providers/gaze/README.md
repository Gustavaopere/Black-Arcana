# Gaze 1.1.7.1 — exact-artifact partial semantic closure

## Status

`EXACT PHYSICAL 1.1.7.1 / EXACT HASH-MATCHED MODRINTH ARTIFACT / ARR / 1 COUNTED IRON'S SPELL / 26 CONFIG-CONDITIONAL SPIRIT RITES / 2 GEAS + 8 RUNES METRIC-EXCLUDED / COMPONENT OPEN / RUNTIME FAIL-CLOSED`

## Installed authority

- provider: **Gaze — A Malum Addon**
- mod id: `gaze`
- installed JAR: `gaze-1.1.7.1.jar`
- runtime version: `1.1.7.1`
- Minecraft / loader: NeoForge 1.21.1
- physical SHA-1: `a8cb3190bde157f78160ce65c202ce2d47fb2041`
- CurseForge project / exact file: `1273454 / 7261638`
- Modrinth project / exact version: `NlvaJ5WE / od4ltbRo`
- publisher license: **All Rights Reserved**
- Modrinth required content: Malum `1.8.2`, Lodestone `1.8.2`
- optional provider: Iron's Spells 'n Spellbooks; physically present in this pack as `1.21.1-3.16.3`

The physical modlist remains authority for installed identity. Phase 2BJ additionally materialized Modrinth version `od4ltbRo` in an isolated audit and required SHA-1 equality with the physical JAR before structural inspection. The exact-artifact audit is recorded in [`EXACT-1.1.7.1-ARTIFACT-AUDIT.md`](EXACT-1.1.7.1-ARTIFACT-AUDIT.md); publisher history remains in [`PUBLISHER-EVIDENCE.md`](PUBLISHER-EVIDENCE.md).

## Classification and authority

Gaze extends **Malum** and optionally integrates with **Iron's Spells 'n Spellbooks**. Authority remains split:

- Malum owns Spirit Rite/Geas substrate semantics and spirit-resource settlement;
- Gaze owns only its addon-specific identities and behavior;
- Iron's owns its spell framework, casting and host settlement;
- Black Arcana owns its own casting, spell domains, rituals, hazards, Corruption, Strain, Arcane Danger, costs, cooldowns, targeting and world-safety runtime.

No Gaze surface authorizes a second spirit ledger, second Malum rite execution path or duplicate Iron's cast settlement inside Black Arcana.

## Exact current semantic surfaces

### Spirit Rites

The exact 1.1.7.1 artifact contains **26 distinct Gaze `RiteHolder<SpiritRiteType>` identities**. The provider progression setup references all 26 and uses Malum Spirit Rite codex page types, establishing them as intended player-facing rite identities rather than spare technical slots.

They are metric-relevant rites, but the exact artifact also proves a provider configuration gate: Gaze's COMMON boolean `disableGazeRites` suppresses registration/initialization of the rite surfaces when its resolved value is true. The source/default value is false, but no authoritative deployed Gaze COMMON config is present in the project evidence. The default is therefore not substituted for current-pack state.

Result: **26 Rites remain `CONDITIONAL`** until the effective deployed `disableGazeRites` value is obtained.

### Geas

The exact artifact exposes two Gaze `GeasEffectType` identities:

- `pact_of_encroaching`;
- `domain_of_swords`.

The current semantic-action metric already excludes base-Malum Geas effect types because effect/status-type identities are not discrete spell/rite actions. Gaze follows the same rule. These two add **0** to the numerator.

### Runes

The exact artifact/progression surface closes eight Gaze rune items. They are item/equipment/passive identities, not standalone spells, glyphs, rites or equivalent action-registry identities under the current metric. They add **0**.

### Iron's compatibility spell

The exact artifact contains one Gaze-owned `Supplier<AbstractSpell>`: **Soulward Shield**. Gaze's `IronsCompat.init` registers its spell registry only when `irons_spellbooks` is loaded. That gate is satisfied in the physical pack:

- JAR: `irons_spellbooks-1.21.1-3.16.3.jar`;
- mod id: `irons_spellbooks`;
- SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

No Gaze-specific disable gate was observed for this spell registration. Generic Iron's host runtime/config remains separate QA, consistent with other exact Iron's spell-content providers.

Result: **Soulward Shield contributes +1 `COUNTED_EXACT` semantic object**.

## Semantic accounting

Phase 2BJ disposition:

- Soulward Shield: **+1 `COUNTED_EXACT`**;
- 26 Spirit Rites: **`CONDITIONAL`** on deployed COMMON config evidence;
- 2 Geas types: **`EXCLUDED`** by metric definition;
- 8 rune items: **`EXCLUDED`** by metric definition.

The strict reconstructible semantic minimum therefore moves from **1249 to 1250**. Gaze does **not** close another provider component because the 26 rite identities remain configuration-conditional, so provider-component closure stays **57/100**. The global semantic denominator remains incomplete and no final magic-coverage percentage is declared.

## Publisher lineage retained for context

The immediately preceding 1.1.7 changelog names Domain of Swords, Pact of Encroaching Malice and multiple Rite/rune/item changes while moving Rites to deferred registration. The 1.1.7.1 publisher delta is narrow: book-entry movement, Fafnir/Malignant-set behavior, Anima Bestiary fixes and localization. These publisher statements remain useful lineage evidence, but exact registry/accounting claims now come from the hash-matched 1.1.7.1 artifact rather than from extrapolation across changelogs.

## Runtime / integration boundary

No Gaze-specific Black Arcana runtime adapter is approved by this catalog checkpoint. Still fail-closed:

- deployed `disableGazeRites` COMMON-config value;
- rite costs/inputs/outputs and resource mutation;
- Geas activation/settlement;
- numerical mechanics/balance;
- complete-modpack runtime behavior;
- any stable provider-native API/hook required for a future adapter.

A future integration must preserve Malum/Gaze/Iron's causal ownership and avoid double processing.

## Clean-room boundary

Gaze is **All Rights Reserved**. Phase 2BJ performed factual exact-binary inspection only after cryptographic identity matched the physical pack. Retained evidence is limited to hashes, metadata, registry/member/type relationships, resource identities/paths and targeted control-flow gate facts required for compatibility/cataloging.

No implementation bodies, recipe ingredient lists, numerical balance data, localization prose, source reconstruction, assets, models or sounds are copied or adapted. Exact-artifact inspection is not a derivation grant.

## Remaining gates

1. obtain the effective deployed Gaze COMMON config and reconcile `disableGazeRites`;
2. if Rites are enabled, promote only the proven-enabled 26 rite identities and then reassess whether the Gaze component can close;
3. validate Gaze `1.1.7.1` + Malum `1.8.2` + Lodestone `1.8.2` + Iron's `3.16.3` in the actual pack runtime;
4. verify provider-native API/hook boundaries before any Black Arcana integration work.

## Sources

- current physical `modlist.txt`, 595 top-level entries, NeoForge `21.1.248`
- CurseForge exact file `7261638`
- Modrinth exact version `NlvaJ5WE / od4ltbRo`
- isolated NON-MERGE evidence PR #201, audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`, run `34676660467`, artifact `10292013626`
