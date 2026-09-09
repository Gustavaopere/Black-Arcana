# Not Enough Glyphs 4.6.1 — Spell Binder and Perks

## Binder storage vs caster contract

Exact source exposes a split surface:

- `Events.attachCaps`: ItemHandler capability with **25 slots** using `DataComponents.CONTAINER`;
- `SpellBinderContainer`: exposes 10 slots on the first page and 15 more on the second page = **25 storage slots**;
- `SpellBinder` data component: `new BinderCasterData(10)`;
- radial menu iterates `spellCaster.getMaxSlots()` = **10 caster slots**;
- `SpellBinder.getBinderCaster`: synchronizes only inventory slots 0–9 into the Ars caster.

`Events.attachCaps` calls `binderCaster.setSpell(spell, slot)` for any changed ItemHandler slot. Exact behavior for storage slots 10–24 against a caster declared with maxSlots 10 depends on the Ars base caster implementation and runtime behavior. Phase 2AF therefore records this as a **25-storage / 10-caster mismatch requiring QA**, not as 25 castable spells and not as a proven defect.

## Casting authority

`SpellBinder.use` resolves the Binder caster and calls the Ars caster's `castSpell`. `BinderCasterData.getSpellResolver` creates `ThreadwiseSpellResolver`, a subclass of Ars `SpellResolver` that extends focus recognition for Binder focus perks.

Black Arcana must not introduce a second Binder cast path or a second mana debit. A future observer must use a causal provider boundary.

## Acquisition

Enchanting Apparatus recipe:

- reagent: Ars Nouveau Novice Spellbook;
- pedestal: 8 Leather;
- result: NEG Spell Binder.

## Networking

NEG registers two C2S payloads:

- `OpenSpellBinderPacket` — server re-resolves the item in the declared hand and requires `SpellBinder` before opening its menu;
- `PacketSetBinderSlot` — server re-resolves a `SpellBinder` in the declared hand before changing the current caster slot.

No local explicit slot-range guard was observed in `PacketSetBinderSlot`; range enforcement may belong to the Ars base caster contract. Do not label this exploitable or safe without the base/runtime evidence.

## Perk provider

With Ars Elemental installed, current source registers **13 Binder perks/threads**:

### Focus perks — 6

- Manipulation Focus;
- Summoning Focus;
- Elemental Fire Focus;
- Elemental Water Focus;
- Elemental Earth Focus;
- Elemental Air Focus.

`ThreadwiseSpellResolver.hasFocus` accepts Shaper's/Summoning focus through the matching Binder perk and delegates elemental focus checks through `ElementalCompat` when Ars Elemental is loaded. `SummoningFocusMixin` also treats the Summoning Binder perk as satisfying the Ars Summoning Focus containment check.

### Gameplay threads — 7

| Registry key | Source contract |
|---|---|
| `thread_wild_magic` | each resolve has probability `0.35 × slotValue` to apply one random spell-stat transform: +AOE, ±duration, split/pierce/randomize/sensitive, +damage modifier, or +acceleration |
| `thread_cheap_damage` | adds Sauce mana-discount attribute `+50 × slotValue`; adds Ars spell-damage bonus `-3 × slotValue` |
| `thread_slow_power` | adds spell-damage bonus `+1 × slotValue`; Binder item modifier also adds acceleration modifier `-1.5 × (slotValue + 1)` |
| `thread_sharp_paper` | main-hand attack damage `+4 × slotValue` |
| `thread_knockback` | main-hand attack knockback `+1.5 × slotValue`, attack speed `-0.5 × slotValue`, attack damage `+1 × slotValue` |
| `thread_scritchance` | Sauce spell-crit chance `+0.10 × slotValue` |
| `thread_scritdamage` | Sauce spell-crit-damage `+0.25 × slotValue` |

The names “Cheap Damage”, “Slow Power”, “Sharp Pages”, etc. are presentation-level labels; registry keys/formulas above are the exact source contracts used here.

## Perk acquisition

All use an Ars Blank Thread reagent in the Enchanting Apparatus.

- Manipulation Focus: Shaper's Focus + 2 Manipulation Essence.
- Summoning Focus: Summoning Focus + 2 Conjuration Essence.
- Wild Magic: Ender Pearl + Rabbit Foot + Bone.
- Cheap Damage: Ghast Tear + Feather + Emerald.
- Slow Power: Iron Block + Blaze Powder + Netherite Scrap.
- Sharp Paper: Diamond Sword + Manipulation Essence + Flint.
- Knockback: Piston + Air Essence + Iron Block.
- Spell Crit Chance: Bow + Rabbit Foot + Quartz.
- Spell Crit Damage: Golden Sword + Dragon Breath + Blaze Powder.
- Elemental Fire/Water/Earth/Air Focus: corresponding Ars Elemental Lesser Focus + 2 matching Ars Essence; recipes are conditionally generated when Ars Elemental is loaded.

## Deduplication boundary

These are Binder/provider stats, not RPG Skill Tree attributes and not Black Arcana resources. A future cross-system progression adapter must not copy the modifiers into a second attribute authority or settle the same cast twice.
