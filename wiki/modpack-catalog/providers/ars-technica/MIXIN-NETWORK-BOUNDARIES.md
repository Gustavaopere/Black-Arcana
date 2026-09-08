# Ars Technica 2.7.6 — mixin and network boundaries

Status: `18/18 DECLARED MIXINS + 5 REGISTERED PAYLOAD TYPES CLASSIFIED`

Exact source checkpoint: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`.

## Declared mixins — 18/18

`ars_technica.mixins.json` is required, Java 21 compatible, and declares **12 common mixins + 6 client mixins**.

### Common — 12

| Mixin | Target / source role | Authority consequence |
|---|---|---|
| `SchematicannonMixin` | Create `SchematicannonBlockEntity`; detects nearby full Ars Technica armor/tagged Curio and accelerates `printerCooldown` while running. | Create remains machine/material authority; provider only modifies cadence. Local ServerPlayer AABB query occurs from the cannon tick path when enabled. |
| `RuneBlockMixin` | Ars `RuneBlock`; Arcane Wrench opens provider cooldown UI client-side. | UX/configuration entry point; rune remains Ars-owned. |
| `RuneTileMixin` | Ars `RuneTile`; persists and applies custom post-cast charge ticks and adds Create-goggle information. | Alters host rune cadence, not cast authority. |
| `RelayBlockMixin` | Ars `Relay`; Arcane Wrench converts exact base Relay to provider Precise Relay, preserving NBT server-side. | Source remains Ars-owned; conversion creates provider scheduling surface only. |
| `AnimatedMagicArmorMixin` | Ars `AnimatedMagicArmor`; server regenerates/consumes provider `air` for Pressure Thread, client mirrors visual air. | Provider Pressure reserve is authoritative; do not mirror it externally. |
| `BacktankUtilMixin` | Create `BacktankUtil`; returns Pressure-bearing Ars armor as an air source. | Bridges provider air state into Create instead of creating a new reserve. |
| `TurretMixin` | Ars `BasicSpellTurret`; adds Arcane-Wrench sneak behavior/drop path. | Host turret/cast semantics remain Ars-owned. |
| `ContainmentJarMixin` | Ars `MobJar`; adds Arcane-Wrench sneak/drop handling. | Wrench interoperability only. |
| `PedestalMixin` | Ars `ArcanePedestal`; adds Arcane-Wrench sneak/drop handling. | Wrench interoperability only. |
| `EffectCrushMixin` | Ars `EffectCrush`; tracks resolver, and with Transmutation Focus doubles sub-100%-chance CrushRecipe output stack counts, capped to max stack. | Modifies the same Ars crush settlement; no external second Fortune/yield proc. |
| `ArcaneWrenchItemStackMixin` | Minecraft `ItemStack`; migrates saved `ars_technica:runic_spanner` stacks to Create wrench + persistent provider component and changes display name. | Compatibility/migration seam; old wrench ID is not separate current equipment authority. |
| `ArcaneWrenchEnchantingApparatusRecipeMixin` | Ars `EnchantingApparatusRecipe`; ensures Create-wrench apparatus result receives provider Arcane-Wrench component. | Recipe-result normalization only; Ars apparatus remains acquisition authority. |

### Client — 6

| Mixin | Client role | Gameplay authority |
|---|---|---|
| `CrushingCategoryMixin` | Rebuilds Create crushing JEI output layout and shows Obliterate/Fortune chance details. | none; presentation only |
| `ArcaneWrenchPartialItemModelRendererMixin` | Replaces Create wrench rendering for Arcane-Wrench-component stacks. | none; rendering only |
| `CraftingButtonMixin` | Adds active Create-processing mode to Ars spell-strip tooltip. | none; UI only |
| `GlyphButtonMixin` | Highlights valid subsequent-effect glyphs and provides composite/processing tooltips. | none; UI only |
| `GlyphItemMixin` | Adds possible provider processing modes to glyph item tooltip. | none; UI only |
| `GuiSpellBookMixin` | Maintains/clears client spell-composition context used by those tooltips. | none; UI context only |

Black Arcana must not consume client presentation state as cast/resource/targeting authority.

## Registered payload types — 5

Ars Technica has two registration surfaces at this pin.

### Create/Catnip packet registry — 1

`ATPackets` registers protocol 1:

- `ars_technica:configure_source_motor` — client→server `ConfigureSourceMotorPacket`, derived from Create `BlockEntityConfigurationPacket`; carries block position and requested stress-capacity ratio, then calls `SourceMotorBlockEntity.setGeneratedStressUnitsRatio(...)` on the server-side block entity.

The normal Source Motor screen constrains the ratio to **0..100** before sending. Phase 2V has not separately audited every validation performed inside the exact Create 6.0.8 `BlockEntityConfigurationPacket` superclass; therefore server distance/interaction validation inherited from that framework is not asserted here.

### NeoForge/Ars-style payload registrar — 4

Protocol version `1`:

- `ars_technica:particle_effect` — server→client; creates supported particles only; no gameplay authority;
- `ars_technica:ticks_until_charge` — client→server; carries integer ticks + block position and, if target is an Ars `RuneTile` implementing provider `IRuneTileModifier`, directly writes the custom charge count;
- `ars_technica:custom_cooldown` — client→server; carries integer ticks + block position and, if the target BE implements `IModifiableCooldown`, directly writes the custom cooldown;
- `ars_technica:technomancer_nearby` — server→client; mirrors the Schematicannon proximity boolean into a client block entity implementing `ITechnomancerAware`.

## Server-validation observation

Normal Rune/Relay UIs constrain values to configured ranges; source defaults are 5–600 ticks. In the exact source handlers for `ticks_until_charge` and `custom_cooldown`, Phase 2V does **not** observe an explicit server-side range clamp, player-distance check or ownership/permission check before the integer is applied to a matching block entity in the player's current level.

This is recorded as:

`SOURCE-RISK / RUNTIME-SECURITY-QA REQUIRED`

It is **not** a claim that the installed pack is exploitable: enclosing network/framework behavior, chunk reachability and current host-version behavior still require runtime validation. Black Arcana must not copy this trust model; its own client requests remain intent-only and server-validated per `plans/DECISIONS.md`.

## Version-drift sensitivity

The highest-risk mixins are those targeting concrete Ars/Create internals rather than stable provider interfaces: Schematicannon, Rune/Relay, Backtank, EffectCrush, Ars GUI/recipe classes and Create wrench renderer. Ars Technica 2.7.6 was built against Ars 5.11.0.1267/Create 6.0.8 while the pack uses Ars 5.13.1/Create 6.0.10. Declared dependency ranges alone do not promote these mixins to runtime PASS.