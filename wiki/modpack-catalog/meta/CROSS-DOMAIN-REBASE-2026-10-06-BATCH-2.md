# Cross-Domain Rebase — 2026-10-06 — Zero-Semantic Batch 2

Status: `CURRENT PHYSICAL CROSS-DOMAIN TRIAGE / 3 NEW ✅ ZERO-SEMANTIC PROVIDERS / PROVIDER TREE 164 = 162 ✅ + 2 ⚠️ / STRICT SEMANTIC MINIMUM UNCHANGED 1849`

## Authority

- Black Arcana base: `main@4d6ff1f63bda925836af0b1b1c0a2702c7cbdf3a`;
- sibling physical/modlist authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`;
- physical-`Magic` subtotal remains **97/97 mapped**;
- prior cross-domain batch: [CROSS-DOMAIN-REBASE-2026-10-06-BATCH-1.md](./CROSS-DOMAIN-REBASE-2026-10-06-BATCH-1.md).

## New provider closures

| Provider | Mod id | Physical evidence | Disposition | Strict delta |
|---|---|---|---|---:|
| Sky Aesthetics 2.0.13-beta | `sky_aesthetics` | current physical JAR/SHA-1 + official project/API/release docs | `ZERO_SEMANTIC_CLIENT_SKY_RENDER_API` | +0 |
| Northstar Redux 0.6.5+1.21.1 | `northstar` | current physical JAR/SHA-1 + official project/source/release scope | `ZERO_SEMANTIC_CREATE_SPACE_TECH_TRAVEL` | +0 |
| YUNG's Better End Island 3.1.2 | `betterendisland` | current physical JAR/SHA-1 + official project/release scope | `ZERO_SEMANTIC_END_WORLDGEN_DRAGON_FIGHT_OVERLAY` | +0 |

## Why these are cross-domain

### Sky Aesthetics

Stars, shooting stars, constellations, unusual skies and dimension-conditioned visuals can look magical, but the provider is a client rendering/resource-pack API. It produces no server gameplay action roster.

### Northstar Redux

Northstar has dimension transfer, Return Ticket teleportation, planets and atmosphere systems. These are Create/space-technology travel mechanics, not provider-owned spells or rituals. The catalog therefore records the ownership boundary explicitly instead of counting teleportation by appearance alone.

### YUNG's Better End Island

The provider changes the central End island and dragon-fight flow. The automatic/proximity initial fight is world state, and the resummon path remains Minecraft's End Crystal lifecycle. Arena/position/flow changes do not create a second addon-owned ritual identity.

## Explicit non-additions from this triage

The same heuristic pass surfaced additional non-Magic-category rows that are **not** materialized as provider directories in this batch:

- **Cold Sweat: Altitude 0.7.0** — sibling dossier explicitly says the user-added version has not yet been physically revalidated in a post-install snapshot; do not promote current physical presence/version without new evidence.
- **Amplified Nether 1.2.16** — pure Nether terrain/worldgen geometry; no semantic ambiguity requiring a magic-provider directory in this pass.
- **Chunky 1.4.23** — world pregeneration utility; executes existing worldgen and owns no content roster.
- **Destroy / NeoForge** — heuristic false positives caused by the category text `Sem projeto CurseForge confirmado`, not magic-related candidates.

Existing aliases found in the same pass — Ignis Soulfires, Reliquified Cataclysm Fix, EMF Iron's compat, Ars Two-Way Portals, Dragon Care, Soul Fire'd and EFIS compat — already resolve to canonical provider directories and are not duplicated.

## Structural consequence

Before this batch:

- 161 directories;
- 159 ✅;
- 2 ⚠️.

After this batch:

- **164** directories;
- **162 ✅**;
- **2 ⚠️**;
- **0 ❌**;
- **0 🟡**;
- **0 ⛔**.

The two ⚠️ providers remain Traveloptics and Deeper and Darker.

## Semantic consequence

No semantic object is added.

- strict reconstructible semantic minimum: **1849**;
- physical-`Magic` mapping: **97/97**;
- final semantic denominator: open;
- technical cross-domain denominator: still `PENDING REBASE`.

This batch advances structural ownership reconciliation without converting technological travel, client rendering, worldgen or vanilla fight lifecycle into magic identities.
