# Capability Matrix Delta — Ace's Spell Utils 1.2.7.2

Scope: exact physical identity plus exact official source-version pin `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.

Ace's Spell Utils is a shared Iron's utility/runtime provider. It contributes **0 standalone registered spells**, but it materially occupies cross-domain school, attribute, proc, domain-helper, item-helper and VFX/runtime space.

| Capability / surface | Exact provider evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Ritual/Occult school identity | registry ID `aces_spell_utils:ritual`; publisher display language Occult | Ace's + Iron's school registry | preserve provider ID; do not create BA alias/second school ledger |
| Hydro school identity | registry ID `aces_spell_utils:hydro`; Java supplier is misleadingly named `ABYSSAL` | Ace's + Iron's | Hydro is canonical provider identity; do not infer `abyssal` |
| Technomancy school identity | `aces_spell_utils:technomancy` | Ace's + Iron's | provider-owned cross-addon school identity |
| School power/resistance | 6 registered attributes | Ace's/Iron's | do not mirror into BA attribute ledger |
| Mana Steal | registered attribute + post-damage handler + whitelist/config | Ace's event runtime over Iron's mana | `DO NOT DOUBLE PROCESS`; no second mana drain/gain path |
| Mana Rend | registered attribute + incoming-damage handler | Ace's event runtime | no duplicate max-mana damage scaling |
| Hunger Steal | registered attribute + melee handler | Ace's | no parallel hunger-transfer proc |
| Goliath Slayer | boss-tag damage bonus | Ace's | compare against other boss-damage providers; no duplicate listener |
| Spell-res penetration | Iron's spell-damage event adjustment | Ace's/Iron's | provider-native first; no second resistance rewrite |
| Evasive / iframe changes | attribute + NeoForge event + required `LivingEntity` mixin | Ace's | high double-processing risk; BA must not add provider iframe layer |
| Magic crits | generic magic + projectile crit chance/damage handlers | Ace's | preserve event priorities/causal owner; no mirrored crit engine |
| Magic projectile bonus | low-priority projectile modifier | Ace's | no duplicate projectile damage multiplier |
| Life Recovery | max-health percentage post-hit heal | Ace's | overlap with lifesteal/recovery providers; no duplicate proc |
| Vigor Reap | missing-health percentage post-hit heal | Ace's | same; provider-owned state/proc |
| Keep-inventory helper | attachment + events + `PlayerMixin` + `IKeepInventoryEntity` | Ace's | no duplicate death/drop/clone pipeline |
| Magic-gun cast helper | calls selected Iron's spell `attemptInitiateCast` | Iron's cast authority, Ace's item helper | BA must not cast same provider spell again |
| Passive ability item helpers | reusable classes + registered examples | Ace's/consumer addon | consumer owns concrete proc; BA/RPG may not hijack authority |
| Summon helper | `AbstractSummonSpell` | consuming addon + Iron's | helper is not standalone Ace's spell |
| Domain helper | `AbstractDomainEntity` | consuming addon/Ace's helper | `REFERENCE/PROVIDER SURFACE ONLY`; never becomes BA canonical domain runtime |
| Domain clash/refinement | source helper + config factor | Ace's helper / consumer | do not connect to BA domain semantics without explicit adapter contract |
| Client VFX transport | 8 S2C optional payloads | Ace's presentation runtime | visual only; not cast authority |
| Rarity extension | 8 `Rarity` enum extensions | Ace's item metadata | names such as `forbidden` carry no BA semantic authority |
| Example objects | 27 unconditional item registrations, creative tab dev-only | Ace's examples | registry objects, not 27 spells or 27 BA gaps |
| Spell tags | `stomp_like_spell`, `slash_like_spell` | shared tag contracts | tags classify consumer spells; do not create spell identities |

## Domain-specific implications

### Black Arcana domains

Ace's `AbstractDomainEntity` is a reusable addon helper with clash/refinement/open/closed/sure-hit conventions. Similar terminology does not create a bridge to Black Arcana spell domains. BA remains authority for its own domains, hazards, world safety and canonical casting pipeline.

A future integration may at most recognize a foreign domain through a bounded adapter if a real contract exists. It must not subclass or route BA domain execution through Ace's as a shortcut.

### Corruption / Strain / Arcane Danger

None of Ace's general attributes or school types are Black Arcana Corruption, Strain or Arcane Danger. No automatic conversion is authorized.

### RPG Skill Tree

RPG may expose progression/mastery/perks around a proven integration contract, but cannot become authority for Ace's proc runtime or Black Arcana casting/runtime.

## Double-processing hotspots

Highest-risk surfaces for future interop:

- Evasive iframe changes because both event and mixin paths exist in provider source;
- Mana Steal/Mana Rend because they mutate Iron's mana/damage state;
- crit/projectile modifiers because event priority affects final damage;
- Life Recovery/Vigor Reap because multiple installed heal/lifesteal providers may share damage events;
- passive ability helpers because consumer addons can attach their own event procs;
- keep-inventory because drop, clone, XP and Curios paths are coordinated;
- magic gun because it directly initiates the underlying Iron's spell.

## Gap-analysis consequence

Ace's Spell Utils must not be counted as a source of player spells. Its semantic contribution is infrastructure/shared runtime. Phase 3 gap analysis should reserve its registered schools/attributes/proc families as provider-occupied space while keeping concrete consuming-addon spells under those addons' own namespaces and authority.
