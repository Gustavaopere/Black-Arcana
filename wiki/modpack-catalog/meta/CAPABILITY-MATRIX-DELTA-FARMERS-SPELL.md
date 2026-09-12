# Capability Matrix Delta — Farmer's Spell 'n Spellbooks 1.0.5.1

Status: `EXACT SOURCE-PINNED MIXED SPELL/CONTENT PROVIDER / 6 SEMANTIC SPELLS / CURRENT-HOST RUNTIME QA OPEN`

| Capability | Exact 1.0.5.1 evidence | Black Arcana consequence |
|---|---|---|
| Provider-owned spell school | `farmers_spell:gluttony` is registered as an Iron's `SchoolType` with provider-owned Gluttony spell-power attribute and damage family | Farmer's Spell owns Gluttony-school identity/content; Black Arcana must not create a parallel Gluttony school or rewrite provider spell ownership |
| Provider-owned spells | one unconditional `DeferredRegister<AbstractSpell>` registers exactly six IDs: `goodberry`, `phantom_loot`, `seal_coat`, `bad_apple`, `chaos_slash`, `preserve_circle` | semantic delta candidate `+6`; spell cost/cooldown/cast lifecycle remains Iron's/provider-native authority |
| Survival scroll reachability | Gluttony school exposes `data/farmers_spell/tags/item/gluttony_focus.json`; the tag includes `#minecraft:foods` and `farmers_spell:foodgeist_seasoning`. Iron's 3.16.3 source-line Scroll Forge contract enumerates enabled/craftable school spells from a matching focus | use provider/host-native acquisition; Black Arcana must not synthesize a second scroll-learning path |
| Generic random-loot path | Gluttony `SchoolType` sets `allowLooting=false` | do not claim generic Iron's random scroll-loot reachability for these six spells |
| Foodgeist / focus support | Foodgeist spawn helper, Foodgeist interaction reward and Foodgeist loot expose provider-owned seasoning/focus progression | provider owns this progression/content loop; Black Arcana does not duplicate spawn/reward state |
| Magical cooking / food / gear | provider registers cooking blocks, foods, equipment, effects and support content in addition to spells | classify as `MIXED`; only discrete semantic spell/action identities enter the current semantic numerator unless separately qualified by the metric |
| Required mixins | 4 common + 3 client required mixins, Java 21 compatibility, default require 1 | loader/dependency ranges are not runtime PASS; current-host mixin application remains a separate fail-closed QA gate |
| Provider network surface | `NetworkHandler.registerPackets()` is empty; no provider-owned payload registration is observed at the exact source pin | no second gameplay network authority is established by this source audit |
| Current build/runtime drift | source uses NeoForge `21.1.238` and GeckoLib `4.9.2`; physical pack uses NeoForge `21.1.248` and GeckoLib `4.7.6` | current client/dedicated-server behavior cannot be inferred from metadata ranges |

## Authority boundary

Iron's Spells 'n Spellbooks owns the host spell/mana/cast/scroll substrate. Farmer's Spell owns its Gluttony school, six registered spells, magical-cooking/content progression and provider-specific support state. Farmer's Delight remains authority for its base cooking/food substrate.

Black Arcana retains authority only over Black Arcana casting, hazards, Corruption, Strain, Arcane Danger, persistence and world-safety contracts. A future adapter must consume a verified provider/host seam without creating a second mana pool, duplicate cooldown/cast settlement, duplicate scroll-learning path or duplicate provider projectile/effect outcome.

## Runtime-risk disposition

The exact source version matches the physical provider version string and closes registry identity. That does not establish assembled-pack runtime compatibility. Seven required mixins, NeoForge build drift and GeckoLib build/runtime drift keep client boot, dedicated-server boot, mixin application and representative spell execution fail-closed until directly tested on the current physical pack.
