# Ars Technica 2.7.6 — spell-part catalog

Status: `11/11 PRODUCTION SPELL PARTS SOURCE-PINNED`

Physical provider authority:

- JAR: `ars_technica-1.21.1-2.7.6.jar`
- mod id: `ars_technica`
- runtime version: `2.7.6`
- physical SHA-1: `adb2641d538375f6eff6a22f0196bb330ab0b171`

Exact provider source checkpoint: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3` (`1.21.X`). Its production `GlyphRegistry.registerGlyphs()` registers exactly the eleven rows below.

Ars dependency used by that source: `ars_nouveau 5.11.0.1267`. The publication corresponding to that build runs from `baileyholl/Ars-Nouveau@f89dacc5d7467aae8497d98e95dad8347a8d7d21`; its `AbstractSpellPart.defaultTier()` is Tier I. This matters for `Insert`, which does not override `defaultTier()`.

The current pack instead contains Ars Nouveau 5.13.1. Phase 2V records the source contract of Ars Technica 2.7.6 and keeps binary/runtime compatibility with the newer host version as a separate QA gate.

## Production inventory

| Registry ID | Kind | Source tier | Source-default mana | School(s) | Compatible augments | Exact source behavior / limits |
|---|---|---:|---:|---|---|---|
| `ars_technica:glyph_carve` | Effect | I | 10 | Manipulation | Amplify, AOE, Dampen | Converts valid identical item entities through stonecutting/Create cutting: default stairs, Amplify walls, Dampen slabs. Amplify and Dampen are each limited to 1. AOE expands item collection. |
| `ars_technica:glyph_pack` | Effect | I | 10 | Manipulation | Amplify, AOE, Dampen | Crafts identical item entities through a square recipe grid. Default 2×2; Amplify 3×3; Dampen 1×1. Grid is hard-clamped to 1–3. Amplify and Dampen are each limited to 1. |
| `ars_technica:glyph_polish` | Effect | II | 120 | Manipulation | AOE | Uses Create sandpaper-polishing recipes. Base processing speed is 2.0; capacity is `4 × (1 + AOE)` rounded by the provider. With Transmutation Focus, capacity doubles and speed becomes 2.5× base. Supports Create Depot binding. |
| `ars_technica:glyph_obliterate` | Effect | III | 100 | Manipulation | Sensitive, Amplify, Fortune | Spawns the provider-owned Arcane Hammer using a child Ars spell context and cancels the parent continuation at that point. Sensitive switches to item crushing instead of destructive hammer behavior; Amplify increases hammer size/damage; Fortune affects extra crushing outputs with provider-side diminishing returns. Fortune is limited to 4. Supports Depot binding. |
| `ars_technica:glyph_press` | Effect | II | 100 | Manipulation | AOE, Extract, Sensitive, Superheat | Default Create pressing. Sensitive changes the cluster to Packing. Extract changes it to Compacting and gathers nearby fluids around impact and caster within provider radius 8. Extract + following Ars Smelt supplies HEATED; Extract + Superheat supplies SUPERHEATED. Base speed 4.0; focus makes speed 2.5× and doubles the normal `4 × (1 + AOE)` processing capacity. |
| `ars_technica:glyph_superheat` | Augment | III | 150 | Fire | none | Provider augment used by Fuse and Press compacting paths for superheated Create processing. It has no compatible augments of its own. |
| `ars_technica:glyph_fuse` | Effect | I | 75 | Manipulation | AOE, Superheat | Spawns provider-owned Arcane Fusion with a child Ars context. Default Mixing; following Ars Smelt selects Heated Mixing; Superheat selects Superheated Mixing. AOE increases processing amount. |
| `ars_technica:glyph_whirl` | Effect | II | 40 | Manipulation, Air | AOE, Extend Time | Creates a provider-owned processing whirlwind. Base radius 1.5 blocks and base duration 360 ticks; radius is `1.5 + AOE × 0.33`, duration is `360 + round(durationMultiplier × 40)`. Following effects select Create fan processing: Conjure Water→Washing/Splashing, Flare→Smoking, Smelt→Blasting, Hex→Haunting. Supports Depot binding and RuneCaster-position handling. |
| `ars_technica:glyph_insert` | Effect | I inherited | 15 | Manipulation | AOE, Split | Scans a bounded cube around impact with expansion `2 + AOE` for container block entities. Default inserts each stack into a provider-selected valid storage target; Split distributes items across valid targets. Tier I is inherited from Ars 5.11.0.1267 `AbstractSpellPart.defaultTier()`. |
| `ars_technica:glyph_telefeast` | Effect | II | 10 | Manipulation | Sensitive, Pierce | Consumes/uses the first eligible consumable from a target item inventory or drink-compatible fluid from a target tank, preserving returned containers. Sensitive permits attempts to use non-food/drink consumables; Pierce forwards the produced consumable in a provider ItemProjectileEntity instead of consuming it on the caster. A non-forwarded lava fluid path drains 250 fluid units and applies 50 lava damage to the caster. |
| `ars_technica:glyph_apply` | Effect | I | 80 | Manipulation | AOE, Pierce | Applies the PlayerCaster offhand item, or the first extractable wrapped-caster inventory item, through Create item-application/deployer recipes. AOE/Pierce drive block-area selection; item-entity processing is capped by the provider at `4 × (1 + AOE)` applications before item-availability limits. Provider code may replace blocks directly with recipe outputs or spawn result items. |

## Causality and authority

All eleven entries are Ars spell parts, not Black Arcana casts. Ars Nouveau remains authority for spell recipe/context, caster identity, mana settlement and provider glyph configuration. Ars Technica owns the processing entities, recipe interpretation, item/fluid transfers and the concrete Ars↔Create conversion behavior it creates. Create remains authority for Create recipe families and kinetic/processing semantics.

Consequences for Black Arcana:

- never debit Ars mana a second time around an Ars Technica spell;
- never reproduce Create processing outputs, chance rolls, item transfers or fluid settlement as a second effect;
- child contexts/entities created by Obliterate and Fuse remain descendants of the same provider cast, not new offensive casts;
- provider-created block changes from Apply are not routed retroactively through Black Arcana `WorldEffectPolicy`; only Black Arcana-owned destructive/world-mutating effects use that policy;
- visual similarity to technomancy is not a gap. Any future Black Arcana capability overlapping Press/Whirl/Fuse/Apply/Insert must prove a distinct mechanical identity before Phase 3.

## Runtime/version-drift gate

The 2.7.6 source was compiled against Ars Nouveau 5.11.0.1267 and Create 6.0.8, while the physical pack uses Ars Nouveau 5.13.1 and Create 6.0.10. This source catalog does not claim that every mixin, recipe hook, wrapped-caster path or Create integration has been runtime-validated against those newer hosts.