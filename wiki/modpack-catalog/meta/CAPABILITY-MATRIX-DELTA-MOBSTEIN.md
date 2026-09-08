# Capability Coverage Matrix — Mobstein 5.4.4 delta

Date: `2026-09-07`

This delta supplements `CAPABILITY-MATRIX.md` with the exact-release/public-guide Mobstein checkpoint. It does not override unrelated provider rows.

| Capability family | Mobstein 5.4.4 evidence | Deduplication consequence | Phase 3 posture |
|---|---|---|---|
| Resurrection / return from death | Clinical Stretch resurrects compatible full bodies; Reviver Syringe provides provider resurrection and activates Witherstein; Lightningbolt Syringe provides daytime stretcher resurrection; Mobstenio Blood Syringe revives Dr. Mobstenio; Warden/Frankenstein have documented Reviver exceptions | **CORPOREAL RESURRECTION PROVIDER PROVEN.** Black Arcana Souls & Death may retain metaphysical bounded resurrection/anchors only where the causal/resource identity is distinct; do not bypass Mobstein body/machine/syringe gates | `BLOCKED / DEDUP REQUIRED` |
| Summons / companions / bodyguards | Resurrected Axolotl, Dolphin, Bat, Putrid Horse, Ocelot, Villager, Silverfish, Warden, Frankenstein and Rabbit have provider-owned tame/utility/bodyguard roles; experiments also expose companion-like behavior | Do not classify Mobstein entities as Black Arcana summons or mirror ownership/lifecycle; no generic summon mastery from their persistent existence | `BLOCKED / PROVIDER OWNERSHIP` |
| Transformation / creature reconstruction | Surgery Stretch creates mixed reconstructed creatures; Subject Assembly creates mannequins/test subjects; Igor produces failed experiments | Existing anatomy/assembly provider coverage is substantial; Black Arcana should not create a parallel corpse-surgery/experiment builder merely for thematic variation | `BLOCKED / OVERLAP PROVEN` |
| Corpse / anatomical material economy | Full bodies, body parts, organ extraction, Brain/Lungs/Heart public organ family, anatomical ingredients and Full Body Support are part of provider progression | Keep physical remains/organs distinct from Black Arcana souls, Goety Soul Energy, Malum spirits and Eidolon soul state | `BLOCKED / RESOURCE IDENTITY DISTINCT` |
| Buff / aura companions | Public guide attributes nearby Regeneration/Night Vision, Water Breathing, mining utility, Jump Boost, `Blacksmithstrength`-described-as-speed and surgery-derived buff packages to specific reconstructed creatures | These are provider-native persistent companion utilities; do not duplicate as generic Black Arcana familiar auras and do not award mastery per aura tick | `BLOCKED / PROVIDER EFFECTS` |
| Mobility / mount utility | Resurrected Dolphin is rideable/aquatic; Putrid Horse has high jump/speed; Spider surgery is rideable and climbs; Enderman surgery/Experiment 067 teleport; Bat/Experiment 077 fly | Broad movement niches already exist inside Mobstein companions. Any Black Arcana familiar/mobility content must remain semantically distinct | `BLOCKED / OVERLAP PARTIAL` |
| World mutation / environmental behavior | Spider surgery may place cobweb when hit; Snow Golem surgery may break Surgery Stretch; resurrection uses lightning presentation; structures gate progression | These are Mobstein-owned world effects. Black Arcana `WorldEffectPolicy` governs Black Arcana mutations and must not double-settle provider changes | `FAIL-CLOSED` |
| Procedural/random experiment creation | Igor + Igor Table/Station + Suspicious Syringe produce random failed experiments; current public guide excludes 062/097 from Igor pool and describes a max-four syringe process | Do not create a second RNG experiment table or infer exact probabilities; provider RNG remains provider authority | `BLOCKED / RUNTIME QA` |
| Boss awakening / necromantic encounter | Reviver Syringe awakens Witherstein from skeleton in Witherstein Ruins; public guide documents 3 stages and Wither Skeleton pressure in later stages | Distinct provider boss progression exists; Black Arcana resurrection/boss effects must not hijack or duplicate awakening settlement | `BLOCKED / PROVIDER PROGRESSION` |
| Structures / world progression | Frankenstein Castle, Witherstein Ruins and Old Ruins are public provider structures tied to Mobstenio/experiments/boss/items | No global scans or force-load convenience bridge; preserve worldgen/provider acquisition | `BLOCKED / WORLD SAFETY` |
| Progression / perks | Mobstein exposes internal Attack, Health, Speed and Template surgery modifiers, with public ranges for first three | These are not RPG Skill Tree perks/mastery and not Black Arcana progression. A future RPG bridge may consume causal provider milestones only through a real server hook | `FAIL-CLOSED / NO HOOK` |
| Sable moving-structure compatibility | Exact 5.4.4 changelog says Mobstein is compatible with Sable; current pack contains Sable 2.0.5 | Compatibility presence is proven; **semantics are not**. Do not infer machine movement, sub-level transfer, persistence or safe hooks | `UNVERIFIED / FAIL-CLOSED` |

## Cross-provider resurrection identity

The catalog must keep at least these distinct semantic channels separate:

- **Mobstein** — physical body/anatomy/machine/syringe reconstruction;
- **Black Arcana** — bounded Souls & Death contracts such as Soul Anchor/Mortal Ledger under Black Arcana authority;
- **Goety** — Soul Energy and provider-owned necromantic Focus/servant progression;
- **Malum** — provider-owned spirits/Spirit Arcana semantics;
- **Eidolon** — provider-owned soul/research/ritual semantics;
- **Toxony** — Necrotic Mutagen conditional self-preservation/resurrection behavior.

A shared player-facing theme is not evidence of interchangeable resources or a universal resurrection pipeline.

## Current gap decision

Mobstein substantially reduces the space for a generic `corpse + machine -> revived pet/experiment` Black Arcana feature. Remaining Black Arcana design space should focus on mechanics that require its own canonical metaphysical contracts, bounded casting/hazard system or cross-provider safe routing, rather than recreating Mobstein reconstruction with different VFX.