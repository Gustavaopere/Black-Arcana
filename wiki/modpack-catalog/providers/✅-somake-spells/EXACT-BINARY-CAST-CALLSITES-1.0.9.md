# Somake Spells 1.0.9 — exact cast/effect callsite discovery

**State: 🟡 PROBE_PENDING_CI.** This is a static JVM discovery, not runtime QA or a perk adapter.

## Authority and artifact

Sibling RPG Skill Tree physical modlist: Somake Spells 1.0.9 for Minecraft 1.21.1 / NeoForge. Installed/publisher JAR: somakespells-1.0.9-1.21.1.jar, CurseForge File 8867079, SHA-1 171841ac9f802be9309ecc166c1d972ac6d404c0.

The previous [exact crafting method report](EXACT-BINARY-CRAFTING-METHOD-SEAMS-1.0.9.md) fixed these seven class identities, now reused for compiled cast/effect symbol discovery.

[Read-only verifier](../../../../docs/qa/somake_109_cast_refs.py), [synthetic tests](../../../../docs/qa/somake_109_cast_refs_test.py), and [Java 21 workflow](../../../../.github/workflows/somake-109-cast-refs.yml) require the exact SHA-1 before inspecting method names, JVM descriptors, and symbolic calls/field references. No compiled classes, third-party JAR, source bodies, constant tables, localization or assets are committed/exported.

## Class cohort

| Spell ID | Previous exact class identity |
|---|---|
| somakespells:fragmented_requiem | com.somake.somakespells.spells.blood.FragmentedRequiemSpell |
| somakespells:rose_secret | com.somake.somakespells.spells.blood.RoseSecretSpell |
| somakespells:comforting_lullaby | com.somake.somakespells.spells.sound.ComfortingLullabySpell |
| somakespells:funeral_bloom | com.somake.somakespells.spells.blood.FuneralBloomSpell |
| somakespells:withered_rose_vortex | com.somake.somakespells.spells.blood.WitheredRoseVortexSpell |
| somakespells:custodia_caeli | com.somake.somakespells.spells.holy.CustodiaCaeliSpell |
| somakespells:jingle_bell | com.somake.somakespells.spells.sound.JingleBellSpell |

## Strict evidence boundaries

The presence of a JVM invocation or method name does NOT prove effective execution, control-flow reachability, damage formula, unit scale, targeting, range, AoE, projectile size, cooldown, scaling, loot, or a player-specific perk hook. A spell may delegate downstream behavior to entities, effects and tick lifecycles that require independent audits.

- ✅ Prior exact registry and crafting-method class identity.
- 🟡 Cast/effect method signatures and references pending new workflow evidence.
- ⚠️ Numeric targeting, geometry, damage, durations and resource values remain unverified at this gate.
- ⛔ Any geometry/damage/cost mutation adapter remains fail-closed without explicit version-matched API/event proof.

Somake owns its specific content execution; Iron's owns native host casting/resources; RPG Skill Tree owns progression/attributes/Mastery/perks; Black Arcana owns only its native magical runtime. Do not double-charge or double-process effects.

**Promotion gate:** update this report and any spell cards only after inspecting the final exact-SHA Java 21 workflow and confirming method references. The 83-ID registry and global semantic object counts do not change by discovering callsites.
