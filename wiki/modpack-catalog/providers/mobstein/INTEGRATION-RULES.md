# Mobstein 5.4.4 — Black Arcana integration rules

## Status

`PROVIDER AUTHORITY MAPPED / SUPPORTED API NOT PROVEN / PROVIDER-SPECIFIC ADAPTER FAIL-CLOSED`

This document records authority and deduplication constraints only. It does not authorize a Mobstein adapter.

## 1. Provider-native first

Mobstein remains authority for its own:

- full-body and body-part gameplay;
- organ acquisition/storage loop;
- Clinical Stretch resurrection;
- Surgery Stretch construction;
- Mobstein `Attack`, `Health`, `Speed`, `Template` construction perks;
- Subject Assembly Machine mannequin flow;
- resurrected-creature taming/utility/bodyguard behavior;
- failed-experiment creation and behavior;
- Dr. Mobstenio / Igor progression;
- syringe actions;
- Witherstein awakening/encounter semantics;
- structures and provider loot/progression attached to them.

Black Arcana must not mirror any of those states into a second persistent ledger merely to observe them.

## 2. No implicit resource conversion

Mobstein body/organs/resurrection concepts do not automatically become Black Arcana resources.

Forbidden implicit mappings include:

- Mobstein organ/body -> Black Arcana Corruption;
- Mobstein resurrected entity -> Arcane Strain;
- Mobstein resurrection -> Arcane Backlash event;
- Mobstein organ/body -> Malum spirit;
- Mobstein organ/body -> Goety Soul Energy;
- Mobstein organ/body -> Eidolon Soul Shard;
- Mobstein undead/experiment -> Enshrouded Shroud corruption.

Any future exchange requires an explicit design plus a verified provider boundary and transactional ownership. Similar fantasy does not create a bridge.

## 3. Resurrection deduplication

A Mobstein resurrection must settle once under Mobstein's authority.

Black Arcana must not:

- re-spawn a second entity because a resurrection was observed;
- refund/charge a second Mobstein material path without an explicit provider transaction contract;
- bypass provider exclusions for Resurrected Warden or Frankenstein;
- convert Witherstein awakening into a generic resurrection event and then run the provider encounter a second time;
- infer successful resurrection from a lightning visual alone.

If a future Black Arcana ritual intentionally invokes Mobstein resurrection, the adapter must establish a causal completion signal or fail closed. Block/entity polling that cannot distinguish preparation from successful settlement is insufficient for exactly-once behavior.

## 4. Companion/familiar authority

Resurrected pets and failed experiments are provider-owned companions, but that does not make every one of them a Black Arcana familiar.

A future familiar bridge must separately prove:

- real owner identity;
- tame/ownership lifecycle;
- alive/removed/death semantics;
- dimension/sublevel behavior;
- friendly-fire/team treatment;
- loaded-only lookup or another bounded query path;
- whether a provider entity is eligible for a particular Black Arcana familiar mechanic.

Until then, Mobstein entities are **not** inserted into the Black Arcana familiar registry by heuristic class/name/tag matching.

No Mastery is awarded because a companion is alive, loaded, following or inside an aura. Progression needs a discrete causal action with deduplication.

## 5. RPG Skill Tree separation

Mobstein's publisher-facing construction `perks` are inputs for constructed-creature stats:

- Health `20–40`;
- Attack `0.8–2`;
- Speed `0.3–0.5`;
- Template as crafting basis.

They are not RPG Skill Tree perk nodes, character attributes or mastery ranks.

If RPG progression later modifies a Mobstein outcome, it must do so through a real extension point. It must not rewrite Mobstein storage, duplicate the provider stat roll or treat Mobstein's `perk` vocabulary as evidence of shared progression authority.

## 6. Technology boundary

Clinical Stretch, Surgery Stretch, Organ Extractor, Igor's table and Subject Assembly Machine visually resemble laboratory machinery. The audited public material does not establish that they consume:

- Create Stress Units;
- FE;
- AE2 power/network state;
- Oritech power;
- another pack technology resource.

Therefore they remain Mobstein-owned gameplay blocks, not technology-provider capabilities.

A future Create/AE2/Oritech bridge requires an actual supported integration seam. Do not infer one from presentation.

## 7. Sable compatibility

The exact 5.4.4 release notes say Mobstein is compatible with **Sable Mod**.

That statement is preserved narrowly:

- it is a publisher compatibility claim for Mobstein 5.4.4;
- the release does not publish the Sable version in that note;
- the current pack uses Sable 2.0.5;
- exact 5.4.4↔2.0.5 entity/block/sublevel behavior remains runtime QA pending.

Black Arcana must not add a second Sable transform, movement, teleport or physics settlement for Mobstein entities. Where Black Arcana observes a Mobstein companion on a Sable sublevel, coordinate authority remains with the verified Sable boundary.

## 8. Black Arcana Souls & Death overlap

Mobstein occupies **physical reconstruction/resurrection of bodies**. Black Arcana Souls & Death may still own distinct mechanics such as its canonical Soul Anchor/Mortal Ledger contracts, but must not silently hijack Mobstein resurrection identity.

Potential future interaction is allowed only if all of the following are true:

1. the intended mechanic has a semantic purpose beyond duplicating Mobstein;
2. a supported Mobstein boundary exists;
3. causal ownership is unambiguous;
4. exactly-once settlement is preserved;
5. Black Arcana hazard/cost/progression rules remain server-authoritative for the Black Arcana action;
6. Mobstein remains authority for the provider action it performs.

## 9. Black Arcana Familiars & Divination overlap

Mobstein companions can be future observation targets under generic loaded-entity rules, but provider-private data must not be exposed by reflection or arbitrary NBT/capability reads.

Borrowed Sight or other observation mechanics may consume only Black Arcana's canonical whitelisted observation surface. A Mobstein entity does not grant permission to expose its inventories, tame internals, experiment state or other provider-private data.

Pact/familiar mechanics require proven ownership. Entity display name, model, species or proximity is not ownership evidence.

## 10. Structures, encounters and milestones

Frankenstein Castle, Witherstein Ruins and Old Ruins are provider structures. Witherstein is a provider encounter awakened by the Reviver Syringe.

Black Arcana may eventually use a provider milestone only if it can prove a discrete event/identity that cannot be farmed by reload/re-entry/repeated polling.

Do not award Mastery for:

- standing near a structure;
- keeping Witherstein loaded;
- repeated boss-health polling;
- repeated discovery callbacks without a persistent claim key.

## 11. Failure policy

Without a supported Mobstein API/event boundary, provider-specific integration remains disabled.

Fail-closed means:

- no reflection into Mobstein internals;
- no JAR decompilation to discover private implementation;
- no class-name guessing in optional adapters;
- no duplicate resurrection fallback;
- no free Black Arcana benefit when Mobstein state cannot be proven;
- no assumption that the 5.4.4 Sable compatibility claim guarantees current-pack integration.

Generic Minecraft/NeoForge facts may still apply where semantically sufficient—for example, a loaded Mobstein `LivingEntity` can be observed as a living entity by a provider-neutral Black Arcana system without treating that as a Mobstein integration.

## 12. Approval gate for a future adapter

A Mobstein-specific adapter requires evidence for the exact installed version covering:

- a supported public API/event/tag/data contract, or publisher-documented equivalent;
- license/provenance posture for any code-level dependency;
- exact current-pack compatibility;
- owner and lifecycle semantics where companions are involved;
- exactly-once causal settlement where resurrection/organ/boss outcomes are involved;
- dedicated-server behavior;
- Sable/sublevel behavior if the adapter can run there;
- regression tests demonstrating no double-processing.

Until those gates are met: `FAIL-CLOSED`.