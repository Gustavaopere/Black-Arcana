# Capability Matrix Delta — Apothic Compat 2.0.2

Phase: **2AQ preparation** — component ordinal and coverage delta intentionally deferred until concurrent Phase 2AP is reconciled.

| Capability | Provider authority | Exact 2.0.2 evidence | Black Arcana disposition |
|---|---|---|---|
| Loot-category classification | Apotheosis | provider contributes 13 entries to Apotheosis-owned `loot_category_overrides` data map | consume/dedup only; do not create BA category pipeline |
| Projectile-style category overrides | Apothic Compat data | 13 exact item IDs -> `apotheosis:bow` | no BA spell identity created |
| Affix identity/registry | Apotheosis / addon namespace | provider reads `AffixRegistry.INSTANCE` | no ownership transfer |
| Affix blacklist policy | Apothic Compat | one `affix_blacklist` config key | separate provider policy; not BA proc/cast gate |
| Affix pool reconstruction | Apothic Compat over Apotheosis internal | reflection writes private `AffixRegistry.byType` | **do not copy as BA integration seam**; fail-closed |
| Provider reload command | Apothic Compat | `/apothiccompat reload`, `/ac reload`, permission 2 | operational only |
| Datapack reload reconciliation | Apotheosis + Apothic Compat | host rebuild + provider reapply on full datapack sync | preserve single host category/affix authority |
| Standalone spells | none | exact source inventory = 0 | zero spell delta |
| Glyphs / rituals | none | exact source inventory = 0 | zero semantic magic-object delta |
| Mana / casting | none | no provider cast/resource pipeline | BA remains authority |
| Mixins | none | exact tree has 0 mixins | no mixin bridge to reuse |
| World mutation | none observed in exact provider surface | category/config compatibility only | BA `WorldEffectPolicy` unchanged |
| Corruption / Strain / Arcane Danger | Black Arcana | provider has no such state | no mapping by similarity |
| Progression / Mastery | RPG Skill Tree only through contract | provider has no progression system | no authority transfer |

## Deduplication conclusion

Apothic Compat does not fill a Black Arcana spell-domain gap. Its unique value is bounded Apotheosis compatibility: category data and affix-blacklist filtering. A future BA integration must not reproduce the 13 category mappings, create a second affix pool, or treat this provider's private reflection implementation as a supported extension API.

## QA-sensitive observation

Changing a non-empty blacklist to empty through the provider-only reload command does not itself reconstruct the already-filtered host pool because `AffixBlacklist.apply()` exits early on an empty set. Treat live removal semantics as runtime-QA pending; normal Apotheosis pool rebuild lifecycle is distinct.
