# Prismatic Portal

- Provider: **Crystal Chronicles** (`crystal_chronicles`)
- Version: `0.1.3-alpha`
- Registry id: `crystal_chronicles:prismatic_portal`
- Concrete class: `PrismaticPortalSpell`
- Provider school: `crystal_chronicles:prismatic`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Source-pinned signature

- cast type: `LONG`;
- cast time: `60 ticks`;
- base mana: `150`;
- rarity: `LEGENDARY`;
- max level: `1`;
- default cooldown: `60 seconds`;
- base spell power: `0`;
- spell-power-per-level: `0`.

These are source-pinned defaults/signature facts, not deployed-pack measurements.

## Semantic action

Outside the provider's `crystal_chronicles:alpha` dimension, the spell targets a formed, inactive Bismuth portal frame and activates the provider portal state.

Inside Alpha, the same spell returns the server player to their respawn position, falling back to the Overworld shared spawn when no player respawn position exists.

These two context-dependent outcomes belong to one registered spell identity; they do not create separate portal-activation and return-teleport spells.

## Registration closure

Pinned `CCSpells` registers `PrismaticPortalSpell` once through `PrismaticPortalSpell.SPELL_ID` and then registers the provider `DeferredRegister<AbstractSpell>` on the mod event bus.

No provider config branch, mod-presence branch or optional registration path wraps this identity at the pinned source revision.

## School and acquisition boundary

The spell belongs to provider school `crystal_chronicles:prismatic`.

The provider supplies:

- focus tag `crystal_chronicles:prismatic_focus`;
- focus item `crystal_chronicles:rainbow_bismuth_crystal`;
- an extension adding that focus tag to Iron's `irons_spellbooks:school_focus`;
- a provider smelting recipe producing the focus item from the provider Bismuth full-block tag.

This closes the provider side of the catalog-level focus route. Deployed Iron's config and live Scroll Forge behavior remain runtime QA.

## Deduplication and authority

Portal blocks, portal-frame formation, chisel interaction and Alpha dimension state are parts of the provider travel system, not extra spell identities.

Iron's-owned spells embedded in Crystal Chronicles gear remain Iron's identities and are not counted again here.

Crystal Chronicles remains authority for Prismatic Portal behavior and portal/dimension state. Black Arcana must not replay portal activation, teleport settlement or host mana/cooldown settlement.

## Alpha/WIP and QA boundary

The provider is explicitly alpha/WIP. This card closes the catalog identity/signature only. Live registry parity, deployed config, portal persistence, dimension restart/reconnect, protection behavior, multiplayer attribution and dependency coexistence remain fail-closed runtime QA.

Source: `../SOURCE-0.1.3-ALPHA-SPELL-INVENTORY.md`.
