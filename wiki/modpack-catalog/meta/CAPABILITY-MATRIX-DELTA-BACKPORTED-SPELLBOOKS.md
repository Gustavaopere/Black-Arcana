# Capability Matrix Delta — Backported Spellbooks

Phase 2AR candidate provider: `backportedspellbooks`.

## Evidence layers

- Physical artifact: `backportedspellbooks-0.1.2.jar` in the current 595-entry modlist.
- Runtime metadata reported by the physical inventory: `backportedspellbooks` version `0.1.0`.
- Publisher release: CurseForge file `8158731`, released 2026-05-28 for NeoForge/Minecraft 1.21.1, filename `backportedspellbooks-0.1.2.jar`.
- Official release-day source: `RedReaper28/BackportedSpellbooks-1.21.1@07cb65efca0c264762a21c2d6bce0f83e3947226`.
- Release-day source `gradle.properties` still declares `mod_version=0.1.0`; this agrees with physical runtime metadata but not with the public file/release label `0.1.2`.

No source↔physical-JAR byte equivalence is asserted.

## Capability delta

| Capability family | Provider surface | Black Arcana action |
|---|---|---|
| active spells | 6 Iron's `AbstractSpell` registrations under `backportedspellbooks` | treat as provider-owned spell identities; do not clone into BA |
| school/domain | 1 provider school/sub-school surface, Pale Flora | preserve provider namespace; no automatic BA domain/Mastery mapping |
| cast resource | consumes Iron's spell framework; no separate provider mana system observed | Iron's remains mana/cast/cooldown authority for these provider spells |
| spell effects/entities | provider projectiles, clouds, visual entities and four provider effects | provider-owned; no second BA settlement/proc path |
| spellbooks/equipment | Quicksilver and Pale Guide spellbooks plus staffs/weapon/armor content | equipment remains provider content; RPG Skill Tree gains no runtime authority |
| combat procs | Miasma Staff and Garden Rapier post-damage logic | do not double-process equivalent damage/proc causality in BA adapters |
| fall handling | Slime Boots cancels `LivingFallEvent` while equipped | do not add a second fall-negation pass; cooldown semantics remain QA-sensitive |
| worldgen | Corroded Fossil + Quicksilver ore features in `minecraft:sulfur_caves` | provider owns acquisition/worldgen; BA `WorldEffectPolicy` does not take ownership of provider generation |
| recipes/materials | 19 recipe JSONs observed in release-day source | not spells; no magic-catalog inflation |
| networking | no provider custom payload surface observed in inspected source tree | do not infer absence from physical bytecode; fail-closed for unverified binary internals |
| persistence | no provider SavedData/attachment/data-component persistence surface observed in inspected source tree | do not fabricate persistence hooks |
| mixins | no mixin configuration observed in release-day source tree | physical binary parity still unverified |

## Spell identity result

Release-day `ModSpellRegistry` contains exactly six provider registrations:

1. `backportedspellbooks:slime_aspect`
2. `backportedspellbooks:sulfur_bomb`
3. `backportedspellbooks:sulfur_clouds`
4. `backportedspellbooks:sulfur_release`
5. `backportedspellbooks:pale_thorn`
6. `backportedspellbooks:resin_spray`

The exact publisher 0.1.2 changelog names the first four as newly added in that release. Pale Thorn and Resin Spray therefore belong to the prior provider surface and are not counted again as release-delta identities.

## Authority boundary

- Iron's Spellbooks owns the host casting, mana, spell-container/cooldown and host runtime used by these `AbstractSpell` registrations.
- Backported Spellbooks owns its six spell identities, Pale Flora surface, provider effects/entities/content, equipment procs and worldgen/data.
- Vanilla Backport owns the backported vanilla content/attributes/sounds that the addon consumes.
- Ace's Spell Utils owns its own shared attributes/rarities/utilities where consumed.
- Black Arcana retains canonical BA casting, transactional costs, targeting, BA cooldowns/charges, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- RPG Skill Tree receives no provider spell/effect/proc/worldgen runtime authority.

## Fail-closed boundaries

- physical JAR SHA/reproducibility has not been matched to the official source build;
- public release label `0.1.2` versus embedded/source `0.1.0` remains an explicit packaging/metadata discrepancy, not something to normalize away;
- release-day source baseline targets NeoForge `21.1.216` and Iron's `1.21.1-3.15.4`, while the current pack uses NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`;
- direct source imports of Iron's, Vanilla Backport and Ace's are stronger than the generated metadata dependency table, which only formally declares NeoForge and Minecraft in the inspected template; runtime dependency/loader parity remains QA;
- Slime Boots exposes cooldown-related presentation/constants while the inspected fall hook cancels the event without an observed cooldown check; live behavior remains runtime QA;
- full-modpack event ordering, duplicate procs, spell config values, network synchronization and dedicated-server behavior remain runtime QA.
