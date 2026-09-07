# More Relics 1.7.7 — integration rules

## Status

`CONTENT AUTHORITY MAPPED / HOST VERSION UNSUPPORTED BY ADDON PUBLISHER / PROVIDER-SPECIFIC INTEGRATION FAIL-CLOSED`

## 1. Authority split

More Relics is not an independent equipment engine. It extends the **Relics** provider.

Canonical ownership for any future integration:

- Relics — relic data/progression/equipment/evolution framework;
- More Relics — addon relics, addon abilities/statuses/configuration/content;
- Curios — accessory slot framework where used;
- RPG Skill Tree — player progression/mastery/perk authority only when a real bridge exists;
- Black Arcana — its own casting, rituals, Arcane Danger, world policy and magic-domain state.

No layer may silently take over another provider's persistent data.

## 2. Current pack incompatibility posture

The current pack installs:

- More Relics `1.7.7`;
- Relics `0.12.8`;
- Curios `9.5.1+1.21.1`.

The More Relics publisher explicitly states that NeoForge Relics `0.11` and `0.12` are not yet supported and recommends Relics `0.10.7.8`. The exact 1.7.7 changelog still describes a possible **future** mini-beta for Relics `0.12.8`.

Therefore any More-Relics-specific adapter must currently fail closed.

Do not convert “the JAR loads on my machine” into a stable API/support claim. Runtime smoke is necessary but still weaker than a supported provider contract for long-term integration.

## 3. Relic progression

Black Arcana and RPG Skill Tree must not:

- write More Relics/Relics XP directly;
- grant levels because an item is equipped per tick;
- reset/rebuild relic progression state;
- bypass the provider's evolution requirements;
- grant evolved items directly as a generic perk reward unless that is explicitly designed as a provider-compatible acquisition route;
- infer progression completion from client icon state.

If a future RPG progression reward intentionally affects a relic, it must use a supported Relics/More Relics boundary and preserve a single causal mutation.

## 4. Ability settlement

Provider abilities remain provider-owned.

Examples with current publisher evidence include:

- Eject Button threshold behavior;
- Bionic Eye Vulnerability behavior;
- Mass Gauntlet damage-boost cooldown;
- Twin Fangs multi-hit behavior;
- Moodworm status behavior;
- Wonder of U active behavior history;
- provider status/presentation such as Cyberpsychosis.

Black Arcana must not:

- apply a second copy of the provider effect;
- add a second cooldown/charge cost;
- re-run damage from a provider ability;
- consume a Black Arcana resource merely because a provider relic activates;
- map a provider status directly to Corruption/Strain/Backlash by thematic similarity.

## 5. Client indicators are presentation only

More Relics 1.7.6+ exposes status icons above the food bar and 1.7.7 makes per-relic icon indicators individually configurable client-side.

These visuals are not authoritative signals for:

- ability activation;
- damage settlement;
- progression rewards;
- Black Arcana hazard changes;
- server cooldown state.

Any integration must use a server-authoritative provider/host event or query.

## 6. Evolution chains

Publicly documented chains include:

- Tyrant Mask → King Crimson;
- Slumbering Amulet → Whispering Amulet → Made in Heaven;
- Depleted Spool → Weavers Spool;
- Converging Orb → Wonder of U.

Evolution is provider authority. Black Arcana rituals must not independently replace the base item with the evolved item after observing a visual effect or tooltip.

If future lore intentionally links forbidden rituals to relic evolution, the provider evolution must still settle exactly once through a verified boundary.

## 7. Loot and acquisition

More Relics owns addon loot placement through the Relics ecosystem/data used by the provider.

Black Arcana must not duplicate the same acquisition table into its own structures/chests without an intentional design decision and deduplication review.

If a relic appears in both provider loot and a Black Arcana reward pool by design, that is a loot-economy design decision, not an integration requirement.

## 8. Curios slots

More Relics/Relics/Curios own slot eligibility. The publisher specifically documents Eject Button charm/ring eligibility in current-line changelogs.

Black Arcana must not:

- register duplicate slots;
- force-equip provider items outside provider/Curios rules;
- scan every Curios slot globally/per tick when a bounded event/query exists;
- apply a second passive modifier because the item is also visible to Black Arcana.

## 9. RPG Skill Tree progression

A future RPG bridge must observe discrete causal actions, not passive ownership.

Invalid Mastery sources:

- holding a More Relics item;
- having it equipped;
- remaining above/below a health threshold;
- a status icon being visible;
- passive stat uptime;
- relic XP ticking from provider-owned gameplay.

Potential valid sources require a real event and anti-replay identity, for example a verified one-time provider evolution milestone. No such bridge is approved by the current audit.

## 10. Black Arcana artifact overlap

More Relics materially occupies many item-triggered power fantasies. Before adding a Black Arcana artifact/relic-like item, compare the proposed mechanic against the More Relics catalog.

A Black Arcana artifact is still legitimate where its identity depends on Black Arcana-exclusive contracts such as:

- dangerous server-authoritative cast transaction;
- transactional forbidden-magic cost;
- Arcane Danger/Strain/Backlash;
- ritual-bound persistent state;
- bounded world effects through WorldEffectPolicy;
- Mortal Ledger/Soul Anchor semantics;
- an explicitly different interaction model than passive/equipment Relics progression.

Visual/name changes alone do not establish novelty.

## 11. 1.7.0 configuration migration

The publisher documents a persistent-config upgrade hazard for Made in Heaven after the 1.7.0 rework when Relics extended configs retain stale ability data.

Black Arcana must not attempt to repair More Relics config files itself.

The appropriate modpack QA path is:

- inspect actual `relics.yaml` extended-config setting;
- inspect whether stale More Relics Made in Heaven config exists from an older world/profile;
- follow provider-documented regeneration procedure if the issue is present;
- validate both server and client where applicable.

## 12. Fail-closed contract

Until current host compatibility is demonstrated and a supported provider boundary is identified:

- no reflection into More Relics/Relics internals;
- no guessed mixin into addon classes;
- no direct provider NBT/data-component rewrite;
- no source/JAR decompilation to discover private contracts;
- no progression integration based on tooltip/icon state;
- no fallback that gives free Black Arcana effects when More Relics state is unknown.

Provider-neutral Minecraft observations may still be used where they are semantically sufficient, but they do not become a More Relics integration.

## 13. Approval gate

A More Relics-specific implementation requires:

1. successful exact-pack load with More Relics 1.7.7 + Relics 0.12.8;
2. explicit decision whether to keep this unsupported pair or move to an actually supported host/addon combination;
3. supported API/event/query evidence for the chosen versions;
4. progression/evolution persistence validation;
5. Curios equip/unequip validation;
6. dedicated-server validation;
7. save/reload and reconnect validation;
8. no double modifiers/effects/cooldowns;
9. migration check for Made in Heaven configs;
10. re-audit if a dedicated 0.12.8-support More Relics build is published.

Current disposition: `FAIL-CLOSED`.