# Infinite Void

- ID: `firesenderexpansion:infinite_void`
- School: `irons_spellbooks:ender`
- Levels: 1
- Rarity: Legendary
- Cast: Long, 60 ticks (3 s)
- Mana: 500
- Neutral spell power / refinement: 30
- Domain radius: 20
- Domain active duration: 15 s, plus transition/clash timing
- Cooldown: 600 s
- Normal crafting: disabled
- Normal looting: disabled

## Contract

A real domain, not a generic black-hole AoE. The spell creates `InfiniteVoid`, an `AbstractDomainEntity` from Ace's Spell Utils. During opening it pulls eligible nearby entities. On transport, affected entities receive Anchored + Iron's Antigravity + `infinite_void_effect`; the caster additionally receives `ascended_caster_effect`.

`InfiniteVoidEffect` records each entity's origin and dimension, moves it to the provider's void dimension at `original position + 500 Y`, and returns it when the effect ends. Drops from entities that die while affected are moved back to the recorded origin. If the origin record is invalid, the audited fallback is Overworld `(0,100,0)`.

Sure-hit executes every 60 ticks in the void dimension against eligible non-Ascended living entities: 5 `VoidSureHitDamageSource` damage and, on successful hurt, `Voidtorn` for 100 ticks. Voidtorn applies −25% Mana Regen and −5 Armor.

Ascended Caster gives +0.25 Mana Regen, +10% Spell Power (base multiplier), +20% Cooldown Reduction (base multiplier) and Creative Flight during the domain.

Domain clashes compare total refinement and owner health percentage; the domain can collapse when the owner's HP ratio falls below the opposing-refinement share.

## Dedup / authority

Domain lifecycle, transport, origin ledger, sure-hit cadence, clash/refinement, Anchored, Ascended Caster and Voidtorn are provider-native. Black Arcana must not implement a shadow domain state machine.

## Acquisition

`allowCrafting=false`, `allowLooting=false`, `canBeCraftedBy=false`. The alternative progression/source that grants the spell is **NÃO VERIFICADO** in this source pass.

## Source

`InfiniteVoidSpell.java`, `InfiniteVoid.java`, `InfiniteVoidEffect.java`, `AscendedCasterEffect.java`, `VoidtornEffect.java` @ pin `5e4067e...`.