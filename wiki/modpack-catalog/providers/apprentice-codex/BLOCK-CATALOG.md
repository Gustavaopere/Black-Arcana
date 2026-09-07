# Apprentice's Codex — exact block registry catalog

## Status

`SOURCE-PINNED 0.9.7.1 / 20/20 BLOCK REGISTRY IDS FROZEN / SPELL-RUNTIME VS PLAYER-PLACED AUTHORITY SEPARATED / BLOCK-ENTITY + RECIPE QA PARTIAL`

Source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

`BlockRegistry.BLOCKS` contains **20 unique registered block IDs** at this exact checkpoint. All IDs use namespace `apprenticecodex:`.

## Spell-created / spell-runtime surfaces — 7

- `mage_light_torch`
- `wizardlamp_lantern`
- `frost_rune_trap`
- `healing_bloom_light`
- `personal_shelf_chest`
- `rift_hole`
- `otherworld_lens_lens`

These blocks are tied to provider spell lifecycles already cataloged in the corresponding school files. Registry presence does not make them generic world primitives for Black Arcana.

Examples of already-audited boundaries:

- Mage Light and Wizardlamp use provider/server-validated placement;
- Frost Rune Trap is downstream state of Frost Rune;
- Personal Shelf belongs to its own provider storage lifecycle;
- Rift Hole belongs to the provider teleport/rift lifecycle;
- Otherworld Lens is part of the provider lens spell execution.

Black Arcana must not place/remove/settle these a second time after observing the provider spell.

## Player infrastructure / stations — 10

- `apprentice_desk`
- `spellcaster_workbench`
- `spellcaster_accessory_case`
- `spell_dispenser`
- `spell_calibration_bench`
- `arcanum_in_a_jar`
- `creative_spell_dispenser`
- `essence_smoker`
- `atelier_station`
- `alchemy_brewer`

These are provider infrastructure surfaces. Their detailed menus, recipes, inventories, automation and supported-spell rules require station-specific audits before being used as integration hooks.

`creative_spell_dispenser` is a distinct registered block using the provider's creative Spell Dispenser constructor; it must not be treated as ordinary survival acquisition merely because it has a registry ID.

## Magnetic anchor — 1

- `magnetic_stability_anchor`

The source registers a dedicated `MagneticStabilityAnchorBlock` plus matching block item. Its precise stabilization/compat behavior remains a separate functional audit; Black Arcana must not infer Sable/contraption semantics from the name alone.

## Flora / decorative variant — 2

- `comfort_berry_bush`
- `potted_comfort_berry_bush`

The potted variant is registered with vanilla flower-pot integration during common setup. Comfort Berries themselves are item-registry content and are cataloged separately.

## Exact registry total

| Family | Count |
|---|---:|
| Spell-created/runtime | 7 |
| Infrastructure/stations | 10 |
| Magnetic anchor | 1 |
| Flora/potted flora | 2 |
| **Total** | **20** |

## Authority / world-safety rules

1. Apprentice's Codex owns the behavior and persistence of these provider blocks.
2. A provider spell creating a block does not authorize Black Arcana to bypass `WorldEffectPolicy` for Black Arcana-originated effects.
3. Black Arcana must not mirror provider block entities, inventories or timers into a second state store.
4. Creative-only/provider-special variants do not become survival acquisition paths by registry existence.
5. Optional compat behavior associated with a block must be verified separately against the exact installed provider versions.

## Next audit

Registry identity is closed at **20/20**. Functional audit remains open for station workflows, Spell Dispenser supported-spell contract, Magnetic Stability Anchor behavior, block-entity persistence/automation and acquisition recipes.