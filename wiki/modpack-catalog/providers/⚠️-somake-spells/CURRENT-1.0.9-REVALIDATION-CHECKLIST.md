# Somake Spells 1.0.9 — Current Physical Revalidation Checklist

Status: `⚠️ CURRENT PHYSICAL 1.0.9 / EXACT PUBLISHER-RELEASE REGISTRY 83 CLOSED / PHYSICAL EQUALITY + DEPLOYED ACTIVE SUBSET + REACHABILITY OPEN`

## Authority reset

The current sibling modlist at `Gustavaopere/neoforge-rpg-skilltree@e54536b2c875d7b60edc27669473d1d8a71eaf84` identifies the installed provider as:

- JAR: `somakespells-1.0.9-1.21.1.jar`;
- mod id: `somakespells`;
- runtime: `1.0.9`;
- Minecraft / loader: `1.21.1` / NeoForge;
- physical-line update recorded by the sibling modlist on 2026-09-16.

The exact CurseForge release for this line is:

- project ID: `1461634`;
- file ID: `8867079`;
- filename: `somakespells-1.0.9-1.21.1.jar`;
- uploaded: 2026-09-12;
- loader/game: NeoForge / Minecraft 1.21.1;
- license: All Rights Reserved;
- Curse Maven coordinate: `curse.maven:somake-spells-irons-spells-addon-1461634:8867079`.

No current Black Arcana evidence checkpoint has yet captured a physical SHA-1 for the installed 1.0.9 artifact. Do not reuse the 1.0.8-fix SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`.

## Supersession rule

The 1.0.8-fix exact audits remain valid as historical evidence for that artifact only. They no longer prove the current 1.0.9 registry, optional gates, class-level host-default eligibility, config surface, focus membership or survival reachability.

In particular, these former current claims are now historical until revalidated against 1.0.9:

- `67/67` current registry identities;
- `61 unconditional + 6 optional-provider-gated`;
- absence of provider-level `allowCrafting` / `isEnabled` overrides across all current spell classes;
- exact `.guide` key parity for all current registry IDs;
- exact Aqua focus-tag membership;
- exact `enableSpellLockSystem` path/default behavior.

Do not delete those 1.0.8 records; relabel them as historical checkpoint evidence.

## Public 1.0.9 delta that invalidates direct carry-forward

The official 1.0.9 release adds a material content/progression delta, including:

- Red Soul System and Red Soul progression;
- Legendary Monsters Spirit content behind optional-provider presence;
- new Red Soul Lantern and Corrupted Red Soul items;
- additional Spirit/Evocation, Holy, Sound, Aqua and Blood spells;
- `Summon Zombie` replaced by `Summon Drowned`;
- Cataclysm compatibility updated for 3.33;
- optional-mod registration/progression fallback changes.

Therefore 1.0.8 registry identity and optional-gate conclusions cannot be treated as complete for 1.0.9.

The current 1.21.1 publisher changelog's **16 explicitly named spells** are cataloged in [`CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md`](CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md). That file closes naming/school/semantic provenance for those public entries only and deliberately does not convert them into registry IDs.

## Current optional-provider presence already confirmed

The current sibling modlist confirms these relevant providers are physically installed:

- Legendary Monsters: `legendary_monsters-2.2.2 MC 1.21.1.jar`, mod id `legendary_monsters`;
- Born in Chaos: `born_in_chaos_[Neoforge]_1.21.1_1.7.6.jar`, mod id `born_in_chaos_v1`;
- L_Ender's Cataclysm: `L_Ender's Cataclysm 1.21.1-3.33.jar`, mod id `cataclysm`.

Presence alone does **not** prove which 1.0.9 Somake registrations are enabled. For a generalized provider contract, exact predicates still require provider-authoritative evidence. For the **current physical pack catalog**, however, deterministic observation of the exact assembled server registry is higher-authority evidence for the registration outcome actually present in that pack and does not require reconstructing proprietary predicate internals.

## Publisher-confirmed Legendary Monsters gate — partial closure only

The official 1.0.9 File `8867079` changelog explicitly states that **Legendary Monsters is optional** and that its Spirit spells, Red Soul content and items are loaded only when Legendary Monsters is installed. The same changelog says optional-mod progression fallbacks/content registration were improved when supported mods are absent.

Official file page:

`https://www.curseforge.com/minecraft/mc-mods/somake-spells-irons-spells-addon/files/8867079`

This closes the **broad provider-presence condition** for the Legendary Monsters content tranche at publisher level. The latest explicit provider-specific physical checkpoint preserved for this pack identifies `legendary_monsters` 2.2.2 as installed, so that broad condition is satisfied at that checkpoint. The sibling's current reorganized certification index is still partial and has not yet reached that physical entry; its omission from that partial index is therefore not treated as evidence of absence.

The publisher changelog by itself did **not** close the 1.0.9 registry or map every named/localized Spirit spell to a specific conditional registration. The later exact structural audit now closes the release-level registry at **83 declared IDs**; exact ID↔optional-predicate mapping and deployed active subset remain fail-closed.

## Exact 1.0.9 resource-only audit now closed

A temporary non-merge clean-room audit has now materialized exact CurseForge file `8867079`:

- audit HEAD: `ed37ab8ffb0fba23ab68c3810d94fdf0c1da579c`;
- workflow run: `35298734758`;
- text artifact: `10529435038`;
- artifact digest: `sha256:6c21e00982ac5a5c91fb15089dffc6c4b904414cc4b7957346fb71d3a0727955`;
- exact release SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- physical-pack SHA-1 equality: **not yet proven**.

Resource-only findings:

- 83 base `spell.somakespells.<id>` localization keys plus 83 matching `.guide` keys;
- 196 JSON resources under `data/somakespells/`;
- Aqua school-focus tag resource still present;
- exact dependency metadata declares Legendary Monsters and several other integrations optional;
- localization delta versus the historical 67-ID 1.0.8-fix registry is +17 candidate roots / -1 historical root (`summon_zombie`), but this remains localization evidence rather than registry proof.

See [`EXACT-1.0.9-RESOURCE-AUDIT.md`](EXACT-1.0.9-RESOURCE-AUDIT.md).

## Exact 1.0.9 registry structural audit now closed

A second temporary NON-MERGE clean-room checkpoint audited the exact File `8867079` registry structure without retaining implementation bodies.

Evidence:

- refined audit HEAD: `fcd6ce8c59cf5d7a153198fc45eff4761c274ba5`;
- audit-only run: `36092269302`;
- audit job: `107936996913`;
- exact release SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- exact release SHA-256: `1f48dfb93e290b45b628b280d902b2b6471b9d80c2c1b70a4980f14dbe85d48a`.

Closed facts:

- 83 `DeferredHolder` spell fields;
- 83 `DeferredRegister.register` call sites;
- 83 unique registry IDs;
- 83 top-level provider `*Spell` classes;
- 83 base localization roots and 83 matching `.guide` roots, exactly equal to the registry ID set;
- exact delta from historical 1.0.8-fix: +17 registrations / -1 `summon_zombie`;
- zero provider `isEnabled()` overrides across the 83 spell classes;
- seven provider `allowCrafting()` overrides: three structurally constant-false and four non-constant;
- current artifact still contains `enableSpellLockSystem` and `somakespells/general/common.toml` symbols;
- current provider code contains compatibility presence checks for Mowzie's Mobs, Magic From the East, Legendary Monsters, Born in Chaos, Tunes 'n Tomes and Geomancy Plus.

This closes the exact publisher-release **declared registry inventory**. It does not close the active registry subset for the deployed mod composition or generalized ID↔predicate mapping.

See [`EXACT-1.0.9-REGISTRY-AUDIT.md`](EXACT-1.0.9-REGISTRY-AUDIT.md) and [`SPELL-CATALOG-1.0.9.md`](SPELL-CATALOG-1.0.9.md).

## Required current-line closure evidence

Before Somake can leave `⚠️ Parcial / condicionado`, capture authoritative 1.0.9 evidence for all of the following:

1. **Physical identity**
   - publisher-release SHA-1 is now closed at `171841ac9f802be9309ecc166c1d972ac6d404c0`;
   - still capture the installed physical 1.0.9 JAR fingerprint/hash and prove equality to that release artifact.

2. **Current registry declaration — CLOSED AT RELEASE LEVEL**
   - exact File 8867079 declared inventory: **83 unique spell IDs**;
   - exact delta vs 1.0.8-fix: **+17 / -1 (`summon_zombie`)**;
   - current spell cards are consolidated in `SPELL-CATALOG-1.0.9.md`;
   - **still open:** which conditional registrations are active in the assembled pack; runtime observation remains accepted current-pack authority for that outcome.

3. **Optional-provider gates / deployed registration outcome**
   - for any generalized claim about how Somake behaves across different mod compositions, exact predicates must come from permitted provider-authoritative evidence;
   - for **this current pack catalog**, an exact assembled-pack registry snapshot may close which optional registrations are actually present when paired with current physical mod presence/absence;
   - such runtime evidence proves the deployed outcome only and must not be rewritten as a universal predicate rule.

4. **Somake global progression/config**
   - `enableSpellLockSystem` existence in 1.0.9: **CLOSED**;
   - `somakespells/general/common.toml` path symbol in 1.0.9: **CLOSED**;
   - exact current default/control-flow semantics: still bounded unless separately proven;
   - effective deployed value from the actual pack when reachability depends on it: **OPEN**.

5. **Iron's host gates**
   - current per-spell/global/datapack `enabled` / `allow_crafting` behavior for 1.0.9 identities;
   - usable school-focus/acquisition paths in the assembled pack.

### Existing runtime probe path

The isolated `black_arcana_catalog_qa` companion now emits the exact observed Iron's spell registry rows for namespace `somakespells`, including effective school, `enabled`, and `allow_crafting`, on `ServerStartedEvent` of the assembled server.

Canonical runbook: [`docs/qa/provider-catalog-runtime-registry-probe.md`](../../../../docs/qa/provider-catalog-runtime-registry-probe.md).

When paired with the filesystem collector and current physical modlist, those rows may satisfy the **current-pack registration outcome** portions of items 2 and 3 above. They do not by themselves establish survival reachability, `enableSpellLockSystem`, generalized optional-registration predicates, or Aqua authority.

6. **Aqua / T.O coexistence**
   - current Somake Aqua authority and focus/acquisition behavior with installed Traveloptics 4.4.0.1;
   - no authority migration inferred from historical publisher statements.

7. **Survival reachability**
   - object-level or bounded-set acquisition/use proof sufficient for the semantic ledger.

## Clean-room boundary

Somake is All Rights Reserved. Do not decompile the 1.0.9 artifact merely to force catalog closure.

Permitted evidence may include exact hash/metadata, resource paths and structured data, public publisher changelog/release material, supported provider APIs, and deterministic runtime observation. Any deeper inspection must remain within the project's clean-room rules and may not copy or reconstruct proprietary implementation.

## Current disposition

Somake remains **⚠️ Parcial / condicionado**.

The historical 1.0.8-fix semantic contribution remains **+0** and is not reused as current evidence. The current 1.0.9 release total is now **83 declared registry identities**, but no strict semantic-count or technical-component promotion is declared until deployed active-subset/host/config/reachability gates close.
