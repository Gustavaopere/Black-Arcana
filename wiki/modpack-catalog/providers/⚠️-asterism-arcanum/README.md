# Asterism Arcanum

Status: `⚠️ PARTIAL / EXACT PHYSICAL=PUBLISHER 0.1.0 ARTIFACT / 10 COUNTED_EXACT SURVIVAL SPELLS / 1 EXACT REGISTERED CREATIVE-ONLY GATEWAY CONDITIONAL / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@e038568764f0c021f1b83320db2fb0e92a933b71`

Certified physical row:

- order: **#56**;
- JAR: `asterismarcanum-1.21.1-0.1.0.jar`;
- mod id: `asterismarcanum`;
- runtime: `1.21.1-0.1.0`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `4a25ba80116168ddcc812f71467c0598127e774a`.

Exact source pin:

`BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`

The source line was built against Iron's Spells `1.21.1-3.15.6`; the current pack uses Iron's `1.21.1-3.16.3`.

## Exact publisher release

CurseForge:

- project `1456947`;
- exact file `8157080`;
- filename `asterismarcanum-1.21.1-0.1.0.jar`;
- uploaded 2026-05-28;
- Release;
- NeoForge 1.21.1;
- Client & Server;
- Curse Maven coordinate `curse.maven:asterism-arcanum-1456947:8157080`.

The publisher release explicitly lists ten normal spells and lists Astral Gateway separately under **Unfinished/Creative Features**, stating that it cannot be accessed in survival.

## Exact physical/publisher binary equality

NON-MERGE clean-room checkpoint:

- commit `1c27d711f1359075edc403d30e86de9397a38f13`;
- CI run `36252798657`;
- exact binary audit step: SUCCESS;
- verify/GameTest/dedicated-server/Stage 05 companion smoke: SUCCESS.

Audited exact publisher artifact:

- size: `987,245` bytes;
- SHA-1: `4a25ba80116168ddcc812f71467c0598127e774a`;
- SHA-256: `191422cf3096a79e158d3262b52ea98fb1abc745847d4eb356548a5a5f58eebc`.

The SHA-1 exactly matches the physical sibling fingerprint. Installed-pack ↔ publisher-artifact equality is therefore closed for 0.1.0.

See [`EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md`](EXACT-0.1.0-BINARY-REGISTRY-AUDIT.md).

## Exact spell inventory

The exact 0.1.0 artifact contains **11 provider Spell classes** and the exact binary `ASARSpellRegistry` references all 11 expected registered spell classes:

| Spell | ID | Current catalog disposition |
|---|---|---|
| Astral Echo | `asterismarcanum:astral_echo` | `COUNTED_EXACT` |
| Brightburst | `asterismarcanum:brightburst` | `COUNTED_EXACT` |
| Celestial Tether | `asterismarcanum:celestial_tether` | `COUNTED_EXACT` |
| Luminous Beam | `asterismarcanum:luminous_beam` | `COUNTED_EXACT` |
| Piercing Light | `asterismarcanum:piercing_light` | `COUNTED_EXACT` |
| Silvery Barbs | `asterismarcanum:silvery_barbs` | `COUNTED_EXACT` |
| Starcutter | `asterismarcanum:starcutter` | `COUNTED_EXACT` |
| Starfire | `asterismarcanum:starfire` | `COUNTED_EXACT` |
| Star Swarm | `asterismarcanum:star_swarm` | `COUNTED_EXACT` |
| Summon Lunar Moth | `asterismarcanum:summon_lunar_moths` | `COUNTED_EXACT` |
| Astral Gateway | `asterismarcanum:astral_gateway` | `CONDITIONAL / OUTSIDE STRICT COUNT` |

The exact binary registrar contains **0** `TrailblazeSpell` reference. The exact artifact's provider spell-class set also contains only the 11 classes above; Trailblaze is not part of the packaged 0.1.0 Spell-class surface.

## Semantic accounting

Ten publisher-supported survival spells are already part of the strict semantic numerator. This audit upgrades their evidence state from source-pinned to exact-artifact without changing the count.

- ten normal Asterism spells: **10 `COUNTED_EXACT`**;
- Astral Gateway: **1 `CONDITIONAL`**;
- Trailblaze: **not registered / not packaged as a provider Spell class in the exact artifact**.

Current Asterism strict contribution: **10**.

Current semantic delta from this evidence-upgrade checkpoint: **+0**.

At this Asterism evidence-upgrade checkpoint, before the later Ender's Spells and Stuff: Requiem reconciliation, the global strict minimum remained **1443**. The current global total is maintained by the shared semantic ledger rather than frozen in this provider-local checkpoint.

## Astral Gateway boundary

The exact artifact confirms:

- `AstralGatewaySpell` is registered;
- exact provider artifact contains no packaged `irons_spellbooks_spell_config` resources;
- exact provider artifact contains no packaged `astral_gateway` host override resource;
- `AstralGatewaySpell` declares no `allowLooting`, `allowCrafting`, `isEnabled` or `canBeCraftedBy` override;
- exact Astromancer loot resource is packaged.

Exact Iron's 3.16.3 source establishes that the default Astral-school path would be loot-eligible if effective deployed config leaves Gateway enabled/in-school. The publisher simultaneously marks Gateway as unfinished/creative-only and not accessible in survival.

Because the deployed Iron's spell-config/datapack state is not versioned in the repositories, Black Arcana does **not** promote Gateway into the strict survival count.

See:

- [`IRONS-3.16.3-HOST-LOOT-ELIGIBILITY.md`](IRONS-3.16.3-HOST-LOOT-ELIGIBILITY.md);
- [`SURVIVAL-CLOSURE-CHECKLIST.md`](SURVIVAL-CLOSURE-CHECKLIST.md).

## Authority boundary

Asterism/Iron's remain authority for:

- Astral spell registration;
- mana/cooldown/casting;
- projectiles and beams;
- damage cancellation;
- teleport settlement;
- summons;
- scroll/acquisition semantics;
- host spell configuration.

Black Arcana may observe supported final state for progression/perks, but must not recreate spell settlement, synthesize an acquisition route or force-enable Gateway.

## Runtime QA remains fail-closed

Exact catalog identity does not establish assembled-pack runtime PASS for:

- Asterism 3.15.6-build-target → Iron's 3.16.3 behavior;
- deployed spell config/datapacks;
- Astral Gateway unfinished runtime;
- Celestial Tether multi-hit cancellation;
- Silvery Barbs cancellation window;
- Starcutter radius;
- Starfire ricochet/friendly targeting;
- Star Swarm damage activation;
- Luminous Beam ally filtering;
- summon lifecycle;
- multiplayer/protection/restart behavior.

## Result

**⚠️ Partial / conditioned remains correct.**

The ten normal Asterism spell identities are now **COUNTED_EXACT**. The only catalog-level unresolved action identity is the exact registered but publisher-marked creative-only/unfinished **Astral Gateway**, whose effective deployed survival state remains unavailable.

Strict contribution: **10**. Current delta: **+0**.
