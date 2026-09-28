# Simply More — 1.3.0 Alpha 5 physical line

Status: `⚠️ PARTIAL / EXACT PHYSICAL-PUBLISHER FILE RECONCILED / RELEASE-CORRELATED ALPHA5 SOURCE / LOWER_BOUND 22 ACTION ROOTS / LEGACY INVENTORY OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@107ce395d9b37f908ad0ba39ef6ea6a01e5f27b2`;
- physical row: `#502`;
- JAR: `simplymore-forge-1.3.0_alpha.jar`;
- mod id: `simplymore`;
- runtime: `1.3.0_alpha`;
- physical SHA-1: `51636477cd5c378f42d9700e1fe35cd952c8f4f1`;
- sibling physical digest reconciliation: CurseForge File `8736778`, `simplymore-neoforge-1.3.0_alpha5+1.21.1.jar`;
- required host: Simply Swords `1.70.2-1.21.1`.

Official Alpha 5:
`https://www.curseforge.com/minecraft/mc-mods/simply-more/files/8736778`

Official initial 1.3 Alpha changelog:
`https://www.curseforge.com/minecraft/mc-mods/simply-more/files/8721021`

Official source:
`https://github.com/jay-jay0101/Simply-More`

## Release-correlated source checkpoint

The public `v1.21.1` source line is moving and therefore its current head is not used as the installed artifact authority.

For the installed Alpha-5 line, the strongest release-correlated source checkpoint identified is:

`jay-jay0101/Simply-More@55977c5e6a4fdaf4281781d9c4475a52286b3184`

This commit is dated 2026-08-26, immediately after the Alpha 4 dedicated-server registration fix and before the later September development series. Its changes include the client/server separation and entity/HUD cleanup that align with the Alpha-5 crash-fix line, including Soulfracture and Blade of the Grotesque-related surfaces.

At this checkpoint:

- `minecraft_version = 1.21.1`;
- `mod_version = 1.3.0_alpha`;
- NeoForge is an enabled platform.

This is **release-correlated source evidence**, not a claim that the publisher JAR is byte-identical to a locally built artifact from this commit.

## Semantic lower bound: 22 provider-owned roots

The 1.3 Alpha publisher notes explicitly establish a rework boundary: some older uniques marked for rework had functionality removed and could currently do nothing. Therefore the 33-Unique headline is not a safe semantic denominator.

The same release line explicitly identifies nine reworked/current unique families with active/passive ability surfaces. The release-correlated source checkpoint confirms their corresponding causal behavior. Counting one passive root and one active root for each of these nine families yields **18 confirmed unique-ability roots**:

| Unique | Passive root | Active root |
|---|---|---|
| Magmaseep | hit-triggered Hellfire eruption / smoke-knockback behavior | Volcanic Vent |
| Moundshifter | pressure/earthquake and associated carried-block combat state | underground excavation/drill release |
| Grandfrost | hit-triggered freezing | Snow Prison / ice-wall storm |
| Lustrous Moxie | light-orb accumulation/detonation | Heavensent Ray / beam activation |
| Soulfracture | soul-fragment fracture/harvest state | fragment manipulation/execution activation |
| Black Pearl | positive-effect theft on hit | explosive cannonball |
| The Blood Harvester | baseline lifesteal | Harvest state |
| Ruyi Jingu Bang | hit-triggered weapon growth/range state | charged enlarged strike |
| Blade of the Grotesque | hostile aura / held passive state | statue transformation and breakout |

For conservative semantic counting, each active root above is counted once even when its implementation has multiple downstream modes, targets, projectiles or follow-up consequences.

### Four Simply More-owned implicits

At the same source checkpoint, `ImplicitRegistry` defines exactly four provider-owned `WeaponImplicitDefinition` roots:

1. `simplymore:grandsword_sunder` — Grandsword armor-sunder/shield interaction;
2. `simplymore:friendship` — Lance mounted-damage implicit;
3. `simplymore:disarm` — Khopesh attack-speed reduction chance;
4. `simplymore:stun` — Pernach stun chance.

Other Simply More weapon types are mapped to existing Simply Swords weapon-type/implicit definitions. Deer Horns reuses the same Simply More Khopesh implicit identity and is not counted as a fifth root.

Therefore:

- confirmed reworked-Unique roots: **18**;
- confirmed Simply More-owned implicit roots: **4**;
- **semantic lower bound = 22**.

## Why this is not a complete Alpha-5 denominator

The exact complete current action inventory remains open because the Alpha publisher warning and source tree contain a mixed state:

- some older uniques retain implemented behavior;
- some rework placeholders are visibly inert or incomplete;
- some removed/deprecated item IDs redirect to replacements;
- Mimicry exposes many item forms but those forms do not automatically imply distinct causal ability identities;
- partial Iron's Spells compatibility applies only to reworked uniques and may change scaling/integration without creating a new provider-owned action root;
- active/passive downstream entities, effects, cooldowns, particles and state machines are implementation machinery, not extra roots by themselves.

Examples such as Timekeeper and Ruptured Idol demonstrate why item presence/interface declaration cannot be promoted blindly: exact source still contains unfinished/inert surfaces.

The lower bound is intentionally restricted to the 22 roots whose current Alpha-line existence is positively established.

## Config / reachability boundary

The Alpha line is explicitly config-breaking, and the project contains configurable unique-effect values. This audit does not assume that every upstream default equals the deployed pack state.

Because the **complete legacy/rework inventory is already open**, deployed config is not yet the sole blocker. First close all remaining live/inert/removed unique roots object-by-object; then classify any feature/config gates that can suppress surviving roots.

No strict global objects are added in this checkpoint.

## Ownership and deduplication

- Simply Swords owns its base weapon ecosystem and any reused base implicit definitions.
- Simply More owns the four implicits registered under its own namespace and its provider-native Unique active/passive causal roots.
- Effects, summons/projectiles, HUD counters, status effects, transformed item forms and downstream damage are not counted separately from their root ability.
- Reusing Simply Swords APIs does not transfer ownership of Simply More's provider-native roots.
- Black Arcana must not duplicate provider proc execution, active-state lifecycle, projectile/entity settlement, cooldowns, effect application or transformation logic.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates through verified contracts.

## Clean-room note

The upstream project is All Rights Reserved. This catalog records only factual release/version correlation, registry identifiers, public behavior descriptions, source structure and causal ownership needed for interoperability/cataloging. No upstream implementation body or asset is copied into Black Arcana.

## Closure gate

Promote Simply More beyond `LOWER_BOUND 22 / +0 STRICT` only after:

1. every non-deprecated Alpha-5 Unique/current replacement is classified as live, inert/rework, removed/proxy or non-semantic;
2. every live passive/active causal root is deduplicated object-by-object;
3. Mimicry forms are proven either aliases/forms or distinct action roots;
4. partial Iron's Spellbooks integration is separated from provider-owned action identity;
5. any deployed config/feature gate that changes reachability is captured;
6. physical fingerprint remains the cataloged Alpha-5 SHA-1.

Runtime QA for prerelease crashes, multiplayer state, once-per-swing settlement, cleanup and config migration remains separate from semantic inventory closure.

## Result

**⚠️ Partial — release-correlated lower bound 22.**

Confirmed provider-owned semantic roots: **22 = 18 reworked-Unique active/passive roots + 4 Simply More-owned implicits**.

Strict global delta: **+0** until the remaining Alpha-5 legacy/rework inventory and reachability gates are closed.
