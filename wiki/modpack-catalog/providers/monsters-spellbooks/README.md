# Monsters & Spellbooks — provider catalog

## Installed identity

- Minecraft: `1.21.1`
- Loader: NeoForge
- physical artifact: `monstersspellbooks-0.0.16.3.jar`
- mod id: `monstersspellbooks`
- runtime/version reported by the physical modlist: `0.0.16.3`
- physical JAR SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`
- CurseForge project: `1428928`
- exact release file: `8788560`
- exact release date: `2026-09-01`

## Provider role and authority

Monsters & Spellbooks is an Iron's Spells 'n Spellbooks addon. The addon owns its spell implementations, its own registered schools/attributes/effects/equipment/mobs and the gameplay semantics implemented behind those registrations. Iron's remains the casting framework/resource/cooldown/spell-registry authority used by those spells.

Black Arcana must not create a second Iron's cast path, second mana debit, mirrored cooldown ledger, duplicate summon lifecycle or duplicate provider world mutation merely because a Monsters & Spellbooks spell overlaps a Black Arcana fantasy.

## Current semantic spell inventory

The current public source head registers **98 spell objects** through `ModSpellRegistry`. The registry itself is unchanged across the public source interval that contains the 0.0.16.2/0.0.16.3 release work, and the exact 0.0.16.3 release notes do not add or remove spells.

Source-family distribution:

| Source family | Registered spell objects |
|---|---:|
| blood | 5 |
| ender | 12 |
| evocation | 3 |
| fire | 10 |
| holy | 4 |
| hydro | 8 |
| ice | 8 |
| lightning | 14 |
| nature | 7 |
| necro | 25 |
| technomancy | 2 |
| **Total** | **98** |

These family names are package/registry organization from the provider source. They are **not automatically equivalent to 11 independent SchoolType registrations**.

See [`SPELL-CATALOG.md`](./SPELL-CATALOG.md) for the complete 98-entry source inventory.

## School surface

The current public source registers two provider-owned `SchoolType` objects:

- `monstersspellbooks:necro`
- `monstersspellbooks:aero`

The exact 0.0.16.2 release explicitly says Aero was soft-deleted in favor of Snackpirate's Aeromancy. The current `ModSpellRegistry` contains no Aero spell registrations. Therefore Aero is recorded as a retained/compatibility school surface, not as an active spell family for the 98-spell inventory.

See [`SCHOOLS-AND-AUTHORITY.md`](./SCHOOLS-AND-AUTHORITY.md).

## Evidence boundary

The exact installed/release identity is `0.0.16.3`, but the current public repository's `gradle.properties` still declares `mod_version=0.0.14`, NeoForge `21.1.216` and Iron's `3.15.4`. The source head is contemporaneous with the September 1 release and its release-interval diff supports the current inventory, but it is **not promoted as an exact 0.0.16.3 build pin**.

Accordingly:

- exact physical/release identity: verified;
- 98 registration inventory at the current public source head: verified;
- stability of `ModSpellRegistry` across the public 0.0.16.2/0.0.16.3 work interval: verified;
- exact 0.0.16.3 binary registry paths, constructor signatures, mana values, cooldowns, tiers, scaling formulas and config values: `NÃO VERIFICADO` unless separately proven;
- no source field is silently upgraded to exact-JAR authority.

See [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md).

## Black Arcana boundary

- Provider-native casting stays in the Iron's pipeline.
- Provider-native spell costs/cooldowns remain provider/Iron's-owned.
- Provider summons/forms/effects are not reproduced by a second Black Arcana runtime.
- Destructive Black Arcana-owned effects still pass through `WorldEffectPolicy`; invoking a provider spell does not authorize Black Arcana to replay the same mutation.
- Thematic similarity is only a deduplication signal, never an integration hook.
- `necro` or other provider terminology does not automatically map to Black Arcana Corruption, Strain, Arcane Danger, Souls & Death state, or RPG Mastery.
- Optional bridges require a verified server-safe hook and fail closed otherwise.

## Catalog state

Phase 2AH closes the provider at the strongest evidence currently available: exact artifact/release identity plus a complete 98-registration semantic inventory from the contemporaneous official source line, with exact 0.0.16.3 internals kept fail-closed.
