# Simply More — 1.3.0 Alpha 5 physical line

Status: `⚠️ PARTIAL / EXACT PHYSICAL-PUBLISHER FILE RECONCILED / RELEASE-CORRELATED ALPHA5 SOURCE / LOWER_BOUND 9 PLAYER-INVOKED ACTION ROOTS / LEGACY INVENTORY OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@51d590653d927538f23ba6f1643576dc6cc49859`;
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

This commit is dated 2026-08-26, immediately after the Alpha 4 dedicated-server registration fix and before the later September development series. Its changes include client/server separation and entity/HUD cleanup aligned with the Alpha-5 crash-fix line, including Soulfracture and Blade of the Grotesque-adjacent surfaces.

At this checkpoint:

- `minecraft_version = 1.21.1`;
- `mod_version = 1.3.0_alpha`;
- NeoForge is an enabled platform.

This is **release-correlated source evidence**, not a claim that the publisher JAR is byte-identical to a locally built artifact from this commit.

## Semantic lower bound: 9 player-invoked actions

The canonical semantic-magic metric counts discrete provider-owned supernatural **player actions**. It does not count gear/passive proc frameworks, status effects or ordinary downstream consequences.

The initial 1.3 Alpha publisher notes explicitly establish a rework boundary: some older uniques marked for rework had functionality removed and could currently do nothing. Therefore the 33-Unique headline is not a safe semantic denominator.

The same release line explicitly identifies nine reworked/current unique families with active ability surfaces, and the release-correlated source confirms those player-invoked roots:

| Unique | Player-invoked active root |
|---|---|
| Magmaseep | Volcanic Vent |
| Moundshifter | underground excavation/drill release |
| Grandfrost | Snow Prison / ice-wall storm |
| Lustrous Moxie | Heavensent Ray / beam activation |
| Soulfracture | fragment-control activation |
| Black Pearl | explosive cannonball |
| The Blood Harvester | Harvest state |
| Ruyi Jingu Bang | charged enlarged strike |
| Blade of the Grotesque | statue transformation and breakout |

Each row contributes **one conservative player-invoked action root**. Multiple downstream modes, targets, entities or follow-up consequences inside one activation are not counted separately.

Therefore the current semantic lower bound is **9**.

## Documented provider surfaces excluded from the semantic count

The same evidence also establishes passive/proc mechanics and weapon implicits. They remain important for provider ownership and interoperability, but they are **not semantic-magic objects under the current ledger metric**.

### Nine reworked-Unique passive/proc surfaces

- Magmaseep hit-triggered Hellfire eruption / smoke-knockback behavior;
- Moundshifter pressure/earthquake and carried-block combat state;
- Grandfrost hit-triggered freezing;
- Lustrous Moxie light-orb accumulation/detonation;
- Soulfracture soul-fragment fracture/harvest state;
- Black Pearl positive-effect theft on hit;
- The Blood Harvester baseline lifesteal;
- Ruyi Jingu Bang hit-triggered weapon growth/range state;
- Blade of the Grotesque hostile aura / held passive state.

These are equipment/passive proc behavior rather than player-selected casts/actions and contribute **+0 semantic objects**.

### Four Simply More-owned implicits

At the same source checkpoint, `ImplicitRegistry` defines four provider-owned `WeaponImplicitDefinition` roots:

1. `simplymore:grandsword_sunder`;
2. `simplymore:friendship`;
3. `simplymore:disarm`;
4. `simplymore:stun`.

Other Simply More weapon types are mapped to existing Simply Swords weapon-type/implicit definitions. Deer Horns reuses the same Simply More Khopesh implicit identity.

These four are weapon/equipment proc mechanics, not discrete player-invoked supernatural actions under the canonical semantic-magic metric, and contribute **+0**.

## Why this is not a complete Alpha-5 denominator

The exact complete current action inventory remains open because the Alpha publisher warning and source tree contain a mixed state:

- some older uniques retain implemented behavior;
- some rework placeholders are visibly inert or incomplete;
- some removed/deprecated item IDs redirect to replacements;
- Mimicry exposes many item forms but those forms do not automatically imply distinct causal action identities;
- partial Iron's Spells compatibility applies only to reworked uniques and may change scaling/integration without creating a new provider-owned action root.

Examples such as Timekeeper and Ruptured Idol demonstrate why item presence/interface declaration cannot be promoted blindly.

The lower bound is intentionally restricted to the **nine positively established player-invoked active roots**.

## Config / reachability boundary

The Alpha line is explicitly config-breaking, and the project contains configurable unique-effect values. This audit does not assume that every upstream default equals the deployed pack state.

Because the **complete legacy/rework inventory is already open**, deployed config is not yet the sole blocker. First close all remaining live/inert/removed unique roots object-by-object; then classify any feature/config gates that can suppress surviving player-invoked roots.

No strict global objects are added in this checkpoint.

## Ownership and deduplication

- Simply Swords owns its base weapon ecosystem and any reused base implicit definitions.
- Simply More owns its provider-native active roots and equipment/passive mechanics, but only player-invoked supernatural actions enter the semantic ledger.
- Effects, summons/projectiles, HUD counters, status effects, transformed item forms and downstream damage are not counted separately from their root action.
- Reusing Simply Swords APIs does not transfer ownership of Simply More's provider-native actions.
- Black Arcana must not duplicate provider activation, active-state lifecycle, projectile/entity settlement, cooldowns, effect application or transformation logic.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates through verified contracts.

## Clean-room note

The upstream project is All Rights Reserved. This catalog records only factual release/version correlation, registry identifiers, public behavior descriptions, source structure and causal ownership needed for interoperability/cataloging. No upstream implementation body or asset is copied into Black Arcana.

## Closure gate

Promote Simply More beyond `LOWER_BOUND 9 / +0 STRICT` only after:

1. every non-deprecated Alpha-5 Unique/current replacement is classified as live, inert/rework, removed/proxy or non-semantic;
2. every live **player-invoked** active root is deduplicated object-by-object;
3. passive/proc and implicit surfaces remain excluded unless the semantic metric itself is explicitly changed;
4. Mimicry forms are proven either aliases/forms or distinct player-invoked action roots;
5. partial Iron's Spellbooks integration is separated from provider-owned action identity;
6. any deployed config/feature gate that changes active-action reachability is captured;
7. physical fingerprint remains the cataloged Alpha-5 SHA-1.

Runtime QA for prerelease crashes, multiplayer state, once-per-swing settlement, cleanup and config migration remains separate from semantic inventory closure.

## Result

**⚠️ Partial — release-correlated lower bound 9.**

Confirmed provider-owned semantic objects under the current ledger metric: **9 player-invoked active Unique roots**.

Documented but excluded: **9 passive/proc Unique surfaces + 4 weapon implicits**.

Strict global delta: **+0** until the remaining Alpha-5 legacy/rework active-action inventory and reachability gates are closed.
