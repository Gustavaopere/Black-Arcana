# Somake Spells 1.0.8-fix — Host-default reachability audit

Status: `67/67 EXACT SPELL CLASSES / HOST DEFAULT ENABLED+CRAFTABLE / DEPLOYED OVERRIDES AND FULL SURVIVAL ROUTE UNVERIFIED`

## Scope

This audit reuses the exact-artifact evidence already produced for Somake `1.0.8-fix` in the isolated Phase 2BJ/PR #191 work. It does not decompile the All Rights Reserved artifact again and does not promote any spell into the strict semantic ledger.

Its purpose is narrower: determine whether the 67 exact Somake spell classes themselves introduce a source-level prohibition against ordinary Iron's Scroll Forge acquisition, and identify which remaining gates are genuinely deployed-state or focus/reachability questions.

## Exact retained evidence

Canonical physical Somake artifact:

- JAR: `somakespells-1.0.8-1.21.1-fix.jar`;
- CurseForge project/file: `1461634 / 8417850`;
- physical/audit SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- retained exact-artifact reachability report: workflow run `34664093646`, artifact `10288333124`;
- retained targeted optional/config report: workflow run `34664411845`, artifact `10288675409`;
- isolated audit HEAD: `397e09e4bfd65f66b82b1b82151915a91c15148d`.

The retained report starts by matching expected and actual SHA-1 to the physical authority above.

## 67/67 class-level default-config result

The retained report contains exactly **67** Somake spell-class sections under `com.somake.somakespells.spells.*`, matching the already-canonical 67/67 registry inventory.

Across all 67 classes, the declared `DefaultConfig` builder calls are exactly:

- `setMinRarity` — 67/67;
- `setSchoolResource` — 67/67;
- `setMaxLevel` — 67/67;
- `setCooldownSeconds` — 67/67.

No one of the 67 retained class sections contains a Somake-level `setAllowCrafting` call or a declared `allowCrafting`, `canBeCraftedBy` or `isEnabled` override.

This proves only the class/default-config surface visible in the already-retained exact evidence. It does **not** prove the effective deployed value after Iron's global/per-spell config or datapack overrides.

## Exact Iron's 3.16.3 host contract

The physical pack line uses Iron's Spells 'n Spellbooks `1.21.1-3.16.3`. The official source checkpoint `iron431/Irons-Spells-n-Spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` identifies itself as Minecraft `1.21.1`, mod version `1.21.1-3.16.3`.

At that checkpoint:

- `SpellConfigParameter.ENABLED` defaults to `true`;
- `SpellConfigParameter.ALLOW_CRAFTING` defaults to `true`;
- `AbstractSpell.allowCrafting()` resolves `ALLOW_CRAFTING` through `SpellConfigManager`;
- Scroll Forge recipe generation requires `spell.isEnabled()` and `spell.allowCrafting()`;
- the actual Scroll Forge menu also requires `spell.allowCrafting()` plus a focus whose school set contains the spell's school.

Therefore the **host source-default** state for a Somake spell that does not replace these gates is enabled and craftable through the Iron's Scroll Forge eligibility layer.

This is not a deployed-state claim. Iron's 3.16.x supports data-driven/global/per-world spell-config overrides, so a pack may change the effective `enabled`/`allow_crafting` values.

## Guide-key coverage

The exact 1.0.8-fix resource inventory contains:

- **67/67** base localization keys `spell.somakespells.<id>`;
- **67/67** corresponding `spell.somakespells.<id>.guide` keys;
- no base spell ID lacking a matching `.guide` key in the retained report.

The retained audit intentionally preserved key identity rather than protected localization prose. Therefore the existence of the guide keys proves provider-authored guide coverage exists in the exact artifact, but it does not by itself reveal or prove the acquisition mechanism encoded in each guide value.

Do not reconstruct or paraphrase missing guide prose from guesses.

## School-focus boundary

The exact retained evidence also proves Somake registers the custom Aqua school with focus tag location `somakespells:school_focus/aqua` and ships the data resource:

`data/somakespells/tags/item/school_focus/aqua.json`

That closes the existence of a provider-defined focus-tag surface, not the deployed usable membership/reachability of a concrete focus item. The retained report does not preserve the tag's complete value set as an acquisition proof.

Spells using Iron's or optional-provider schools likewise still depend on the corresponding focus/acquisition surfaces of those providers.

## Somake spell-lock gate remains independent

Somake's own COMMON config remains:

- file: `somakespells/general/common.toml`;
- key: `enableSpellLockSystem`;
- audited code default: `false`;
- effective deployed value: `NÃO VERIFICADO`.

The retained provider help text states that when enabled, players must learn spells before use; when disabled, spells are unlocked by default for that subsystem. The source default cannot be substituted for the actual assembled-pack value.

This lock/mastery gate is independent from Iron's `enabled`/`allow_crafting` Scroll Forge gates. Both layers must be respected.

## What this audit closes

For all 67 exact Somake spell identities, it is no longer necessary to treat a hidden per-class Somake `allowCrafting` override as an unknown blocker. The exact retained class evidence shows none of the 67 introduces such an override/default-config setter, and the exact Iron's 3.16.3 host defaults are enabled + craftable.

This narrows the remaining reachability problem to effective pack state and actual focus/acquisition surfaces rather than unknown spell-class registration behavior.

## What remains open

A spell row still cannot be promoted solely from host defaults. Authoritative current-pack evidence must establish, as applicable:

1. effective deployed Somake `enableSpellLockSystem`;
2. effective Iron's spell-config/datapack state for `enabled` and `allow_crafting`, or authoritative proof that no override affects the Somake IDs;
3. a usable school focus/acquisition path in the assembled pack, including the custom Aqua focus surface and optional-provider schools;
4. any additional provider-specific progression prerequisite that can prevent ordinary player use.

If those common/deployed gates close uniformly, the 67 rows can then be reconciled in one bounded pass rather than re-auditing each spell class.

## Clean-room / authority discipline

- no new ARR bytecode reconstruction was performed for this tranche; it reuses the already-approved retained PR #191 evidence;
- no protected localization prose is copied;
- no source default is labeled as deployed state;
- Iron's remains authority for Scroll Forge and spell-config semantics;
- Somake remains authority for its spell-lock/mastery/progression behavior;
- Black Arcana does not synthesize unlocks, acquisition, spell settlement or fallback behavior.
