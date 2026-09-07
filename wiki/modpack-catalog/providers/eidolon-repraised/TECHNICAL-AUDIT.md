# Eidolon: Repraised 0.5.0.2 — Technical Audit

Status: `SOURCE-PINNED / IN PROGRESS`

Source authority: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Audit scope

This file tracks integration-sensitive behavior that must be proven before Black Arcana consumes Eidolon state/events.

### Confirmed provider-owned state

- mana capability;
- reputation/devotion capability;
- soul capability;
- knowledge/research capability;
- Sign registry and SignSequence resolution;
- spell registry/cache;
- ritual registry;
- chant / command-chant / chant-conversion recipes;
- deity and altar state;
- server configs per registered spell.

### Confirmed event surface

`StaticSpell.canCast(...)` posts a cancelable `SpellCastEvent.Pre` before mana/target validation returns true. `StaticSpell.cast(...)` invokes the concrete effect and then posts `SpellCastEvent.Post`.

Integration rule: Black Arcana observations must use one causal id/guard per provider cast and must not combine event observation with world-delta observation without deduplication.

## Cost/settlement anomaly queue

The base class verifies that sufficient mana exists but does not centrally settle the cost. Concrete spell implementations normally call `IMana.expendMana(...)` when their action commits.

At source level, at least these paths require runtime verification:

- `SmiteSpell`: declares cost 40 but the concrete `cast()` shown in 0.5.0.2 does not directly expend mana;
- `ApplyPotionSpell`: generic effect application path does not directly expend mana;
- `SunderArmorSpell`: inherits the above and declares cost 50.

These are not classified as confirmed bugs without runtime evidence. Black Arcana must not compensate by charging mana externally.

## Authority constraints

1. Mana settlement: Eidolon only.
2. Reputation/devotion mutation: Eidolon only.
3. Research grants: Eidolon only.
4. Soul mutation: Eidolon only unless a documented external API path exists.
5. Chant conversion selection and per-item conversion cost: Eidolon recipe manager only.
6. Prayer cooldown, altar power/capacity and effigy readiness: Eidolon only.
7. `NECROTIC`/`CONSECRATED` charge mutation: Eidolon only.
8. SignSequence matching: Eidolon only.

## Runtime QA required

- verify actual mana delta for every spell class, with special focus on Smite and ApplyPotion-derived spells;
- verify Pre/Post event count and side on dedicated server;
- verify no duplicate cast event when a data-driven ChantRecipe materializes a cached Spell;
- verify prayer cooldown/reputation/mana updates are server authoritative;
- verify `NECROTIC` and `CONSECRATED` charges under Epic Fight/other combat transforms in the actual pack;
- verify exact research survival unlock chain;
- verify soul production/consumption lifecycle;
- verify all ritual requirements, sacrifices and cleanup paths;
- verify data-driven chant recipes present in the installed JAR/resources.

## Current conclusion

Eidolon is a high-authority provider. It is safe to classify its capabilities for deduplication, but unsafe to implement resource/progression interception until the remaining runtime checks are closed.