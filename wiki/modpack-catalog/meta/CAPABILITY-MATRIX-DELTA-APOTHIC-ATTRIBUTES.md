# Capability Matrix Delta — Apothic Attributes 2.10.1

Scope: physical `apothic_attributes` 2.10.1 + exact official source revision `686361b2c7b0e76bf4158890bb8a2e42ef805622`.

| Capability / surface | Exact provider evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Standalone spells/glyphs/rituals | 0 registration surface observed | none | do not inflate spell catalog |
| Attributes | 22 central registrations | Apothic Attributes | consume only through proven contracts; do not duplicate formulas |
| Armor/protection | `ALCombatRules` + mixins replace/redirect vanilla calculations | Apothic Attributes | do not post-process a second time |
| Crits | crit chance/damage + multi-crit event runtime | Apothic Attributes | BA Backlash must not enter offensive crit pipeline |
| Auxiliary hit damage | current-HP/fire/cold paths with own tracker/recursion guard | Apothic Attributes | preserve provider damage identities; no thematic BA remap |
| Life steal/overheal | physical post-damage handlers | Apothic Attributes | no duplicate healing/absorption proc |
| Dodge | melee/projectile cancellation + feedback | Apothic Attributes | respect provider cancellation/result |
| Projectile/arrow scaling | arrow damage/velocity + generic projectile damage | Apothic Attributes | no duplicate multiplier |
| Healing/XP/mining | provider attributes/events | Apothic Attributes | not RPG or BA authority by similarity |
| Effects | 7 mob effects | Apothic Attributes | provider-owned content, not BA spells |
| Potions/brewing | 31 potions + 37 generated mixes | Apothic Attributes | do not clone as BA ritual content |
| Damage taxonomy | 5 damage types + physical/magic/bypass/crit tags | Apothic Attributes/NeoForge tags | preserve source classification; BA Backlash remains own family |
| Cooldowns | server-side `AbilityCooldowns` + `cooldown_reduction` | Apothic Attributes for that API | do not apply CDR to BA cooldowns without explicit contract |
| Network | 2 PLAY CLIENTBOUND payloads | Apothic presentation/config | never BA cast authority |
| Config | GUI/effect/combat-formula config + reload | Apothic Attributes | provider config authority |
| Equipment slots | 2 synced registries, 7 slots, 11 groups | Apothic Attributes | attribute composition only |
| Curios compat | conditional modifier-source + StackAttributeModifiers bridge | Curios + Apothic bridge | BA keeps own bounded Curios snapshot path |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no conversion/coupling |
| World mutation policy | no BA world-effect contract | Black Arcana for BA effects | do not infer WorldEffectPolicy hook |
| RPG progression | none | RPG Skill Tree through real contracts | no progression identity created by attributes alone |

## Deduplication result

Apothic Attributes already owns broad generic combat-stat and effect semantics. Black Arcana must not independently recreate provider armor/protection/crit/lifesteal/dodge/projectile calculations as a second global combat layer. BA remains free to own forbidden-magic-specific hazards and spell semantics, but those systems must preserve causal identity and no-proc rules instead of opportunistically entering Apothic offensive handlers.

## Gap-analysis result

This component creates **zero standalone spell gaps**. It closes one current cross-domain provider unit because its own source-visible registry/runtime surface is complete at exact 2.10.1. The catalog result does not imply that Apothic runtime values should be imported into Black Arcana.
