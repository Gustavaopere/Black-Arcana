# Discerning The Eldritch

Status: `CURRENT 1.4.4 IDENTITY VERIFIED; PUBLIC SPELL PAGE HAS AN INTERNAL COUNT DISCREPANCY`

- Current JAR: `discerning_the_eldritch-1.4.4-1.21.jar`
- Mod id: `discerning_the_eldritch`
- Runtime version: `1.4.4-1.21`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary casting authority: Iron's Spells 'n Spellbooks.
- Current license: PolyForm Shield License 1.0.0.

## Current-version note

Version **1.4.4** was published on 2026-09-05. Its public changelog records only:

- crash fix for the latest Ace's Spell Utils;
- config issue fix.

No new 1.4.4 spell is claimed by that changelog, so the public project spell list is used as the current feature baseline unless the installed JAR proves otherwise.

## Public spell list

The current project page says the mod contains **15 new spells**. However, the same page's `Current Spells` text explicitly enumerates only **14 named entries** in the material currently published. Phase 2 records that discrepancy instead of inventing a fifteenth spell.

| Spell | School | Public semantic behavior |
|---|---|---|
| `Silence` | Eldritch | Prevent target from casting spells |
| `Esoteric Edge` | Eldritch | Large slash; additional damage while holding a weapon |
| `Boogie Woogie` | Evocation | Swap caster and target positions |
| `Guardian's Gaze` | Evocation | Ray-like attack that applies Mining Fatigue |
| `Otherworldly Presence` | Eldritch | Teleport plus temporary state preventing taking/dealing damage and preventing casting |
| `Abracadabra` | Eldritch | Buff with incoming-damage cap and negative-potion-effect prevention; configurable |
| `Conjure: Forsaken Aid` | Eldritch | Summon one of multiple eldritch allied entities |
| `Conjure: Gaoler` | Eldritch | Summon Gaoler; hostile targeting can include the caster |
| `Esoteric Strike` | Eldritch | Forward punch; damage scales from attack damage |
| `Mend Flesh` | Eldritch | Small heal plus configurable lifesteal/healing interaction when gaining XP orbs |
| `Rift Walker` | Eldritch | Forward teleport leaving unstable rifts at origin/destination that explode later |
| `Exorcism` | Holy | Removes insanity stacks; only enabled if the insanity system is enabled |
| `Crystalline Carver` | Ice | Multi-slash, Chilled/Frostbite buildup, final hit gains bonus from Frostbite stacks |
| `Glacial Cleave` | Ice | Low-damage icy slash that encases targets in an icy tomb |

### Public count discrepancy

- Page claim: **15 spells**.
- Names explicitly listed in current page text: **14**.
- Resolution: `PENDING CURRENT JAR RESOURCE / UPDATED OFFICIAL PAGE EVIDENCE`.

The catalog must not silently turn a planned, removed or omitted entry into a current spell.

## Deduplication impact

### Order / anti-casting

`Silence` directly covers spellcasting denial. `Abracadabra` covers a defensive damage cap and debuff prevention. `Otherworldly Presence` applies a more complex temporary no-damage/no-offense/no-casting state. A Black Arcana Order spell cannot claim generic “seal casting”, “cap incoming damage” or “enter invulnerable neutral state” as untouched space without a real systems delta.

### Space / Chaos

`Boogie Woogie`, `Otherworldly Presence` and `Rift Walker` provide transposition, teleport and delayed rift explosions. Doctor Strange/Scarlet-Witch-inspired spatial visuals do not create a new mechanic by themselves.

### Summoning / Binding

`Conjure: Forsaken Aid` and `Conjure: Gaoler` occupy eldritch summon space. They do not implement Black Arcana's persistent typed resource links, but they must be included in summon/familiar deduplication.

### Holy / cleansing

`Exorcism` is a conditional cleansing spell linked to an insanity system. Divine/Order cleansing must deduplicate against it and Iron's base Cleanse.

## Provenance / confidence

- Presence/version: current modlist + current 1.4.4 file page — HIGH.
- Current public spell names/semantic descriptions: current project page — HIGH for the 14 names above.
- Claimed total 15 vs enumerated 14: unresolved public-source inconsistency, explicitly retained.
- Exact mana/cooldown/level/value formulas: `PENDING` unless separately confirmed.
- No Java bytecode was decompiled.
